#!/usr/bin/env python3
"""Validate PRD Astro Markdown frontmatter and per-kind content contracts."""
from __future__ import annotations
import argparse, re, sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
import yaml
from registries import validate_schema_object, validate_block

FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
ALIASES = {
 "homepage":"homepage","homepages":"homepage","home":"homepage",
 "menu":"menu","menus":"menu","navigation":"menu","navigations":"menu",
 "page":"page","pages":"page","article":"article","articles":"article","post":"article","posts":"article",
 "service":"service","services":"service","category":"category","categories":"category",
}
class DuplicateKeyError(ValueError): pass
class StrictLoader(yaml.SafeLoader): pass
def _mapping(loader, node, deep=False):
    loader.flatten_mapping(node); result={}
    for kn,vn in node.value:
        key=loader.construct_object(kn,deep=deep)
        if key in result: raise DuplicateKeyError(f"duplicate YAML key {key!r} at line {kn.start_mark.line+1}")
        result[key]=loader.construct_object(vn,deep=deep)
    return result
StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,_mapping)

@dataclass(frozen=True)
class Issue:
    path: Path
    message: str
    def __str__(self): return f"{self.path}: {self.message}"

def parse_frontmatter(path):
    try: source=path.read_text(encoding="utf-8")
    except (OSError,UnicodeError) as exc: return None,f"cannot read UTF-8 Markdown: {exc}"
    match=FRONTMATTER_RE.match(source)
    if not match: return None,"missing or malformed YAML frontmatter"
    try: data=yaml.load(match.group(1),Loader=StrictLoader)
    except (yaml.YAMLError,DuplicateKeyError) as exc: return None,f"invalid YAML frontmatter: {exc}"
    if not isinstance(data,dict): return None,"frontmatter must be a YAML mapping/object"
    return data,None

def posint(v): return isinstance(v,int) and not isinstance(v,bool) and v>0
def nonempty(v): return isinstance(v,str) and bool(v.strip())
def absolute_url(v):
    if not isinstance(v,str): return False
    u=urlparse(v.strip())
    return u.scheme in {"http","https"} and bool(u.netloc)
def utc_date(v):
    if isinstance(v,datetime):
        return v if v.tzinfo and v.utcoffset()==timezone.utc.utcoffset(v) and not v.microsecond else None
    if not isinstance(v,str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z",v): return None
    try: return datetime.strptime(v,"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError: return None

def validate_document(path,data,kind=None):
    out=[]
    def err(msg): out.append(Issue(path,msg))
    def required(fields):
        for f in fields:
            if f not in data: err(f"missing required field '{f}'")
    def string_fields(fields):
        for f in fields:
            if f in data and not nonempty(data[f]): err(f"field '{f}' must be a non-empty string")
    if not posint(data.get("id")): err("field 'id' must be a positive integer (boolean is not an integer ID)")
    kind=kind or ALIASES.get(path.parent.name.lower())
    if kind is None:
        err("cannot infer document contract from collection directory; pass --collection KIND=DIR")
        return out
    required_fields={
      "homepage":("slug","title","description","schema","seo","blocks","updatedDate"),
      "menu":("slug","title","schema","location","items","updatedDate"),
      "page":("slug","title","description","intro","schema","seo","blocks","updatedDate"),
      "article":("slug","title","description","intro","schema","seo","featuredImage","publishedDate","updatedDate","blocks"),
      "service":("slug","title","description","intro","schema","seo","blocks","updatedDate"),
      "category":("slug","title","description","schema","seo","blocks","updatedDate"),
    }
    if kind not in required_fields: err(f"unknown document contract kind '{kind}'"); return out
    required(required_fields[kind]); string_fields(("slug","title","description"))
    schema=data.get("schema")
    if not isinstance(schema,dict) or not nonempty(schema.get("type")):
        err("field 'schema' must be an object with a non-empty string 'type'")
    else:
        for message in validate_schema_object(schema, "document", kind=kind): err(message)
    if kind in {"homepage","page","article","service","category"}:
        seo=data.get("seo")
        if not isinstance(seo,dict): err("field 'seo' must be an object")
        else:
            for f in ("title","description"):
                if f in seo and not isinstance(seo[f],str): err(f"field 'seo.{f}' must be a string")
                if not nonempty(seo.get(f)) and not nonempty(data.get(f)): err(f"SEO fallback is empty: provide 'seo.{f}' or document '{f}'")
            if "canonical" in seo and not absolute_url(seo["canonical"]): err("field 'seo.canonical' must be an absolute HTTP(S) URL")
            for f in ("robots","openGraph","twitter"):
                if f in seo and not isinstance(seo[f],dict): err(f"field 'seo.{f}' must be an object")
    if kind in {"page","article","service"}:
        intro=data.get("intro")
        if not nonempty(intro): err("field 'intro' must be a non-empty string")
        else:
            if "\n" in intro.strip() or "\r" in intro: err("field 'intro' must contain exactly one paragraph")
            if re.search(r"<\s*/?\s*[A-Za-z][^>]*>|\*\*|__|\[[^\]]+\]\([^)]*\)",intro) or chr(96) in intro:
                err("field 'intro' must be plain text without HTML/Markdown markup")
            main=schema.get("mainEntity") if isinstance(schema,dict) else None
            if isinstance(main,dict) and main.get("type")=="DefinedTerm":
                if kind!="page": err("schema.mainEntity.type 'DefinedTerm' is only allowed for Page documents")
                else:
                    if schema.get("type")=="DefinedTerm": err("schema.type must remain a page-level type; use schema.mainEntity.type: DefinedTerm")
                    title=re.sub(r"\s+"," ",str(data.get("title","")).strip())
                    normalized=re.sub(r"\s+"," ",intro.strip()); prefix=f"{title} adalah "
                    if not title or not normalized.casefold().startswith(prefix.casefold()):
                        err("DefinedTerm intro must begin with '<title> adalah <definisi substantif>.'")
                    elif not normalized[len(prefix):].strip(" ."): err("DefinedTerm intro must contain a substantive definition after 'adalah'")
    if kind=="article" or "featuredImage" in data:
        image=data.get("featuredImage")
        if not isinstance(image,dict): err("field 'featuredImage' must be an object")
        else:
            for f in ("src","alt"):
                if not nonempty(image.get(f)): err(f"field 'featuredImage.{f}' must be a non-empty string")
            for f in ("width","height"):
                if f in image and not posint(image[f]): err(f"field 'featuredImage.{f}' must be a positive integer")
            for f in ("caption","credit"):
                if f in image and not isinstance(image[f],str): err(f"field 'featuredImage.{f}' must be a string")
    if kind=="menu":
        if data.get("location") not in {"header","footer","mobile","utility"}: err("field 'location' must be one of: header, footer, mobile, utility")
        def menu_items(items,depth=1):
            if not isinstance(items,list): err(f"menu items at depth {depth} must be an array"); return
            for i,item in enumerate(items):
                p=f"items[{i}]" if depth==1 else f"menu child at depth {depth}, index {i}"
                if not isinstance(item,dict): err(f"{p} must be an object"); continue
                if not nonempty(item.get("label")): err(f"{p}.label must be a non-empty string")
                hp="pageId" in item and item["pageId"] is not None
                hu="url" in item and item["url"] is not None
                if hp==hu: err(f"{p} must define exactly one target: pageId or url")
                if hp and not posint(item["pageId"]): err(f"{p}.pageId must be a positive integer")
                if hu and not absolute_url(item["url"]): err(f"{p}.url must be an absolute HTTP(S) URL")
                if "external" in item:
                    if not isinstance(item["external"],bool): err(f"{p}.external must be boolean")
                    elif item["external"] and not hu: err(f"{p}.external: true is only allowed with url")
                if "children" in item:
                    if depth>=3: err(f"{p}.children exceeds maximum menu depth of 3")
                    else: menu_items(item["children"],depth+1)
        menu_items(data.get("items"))
    if "blocks" in data or "blocks" in required_fields[kind]:
        blocks=data.get("blocks")
        if not isinstance(blocks,list): err("field 'blocks' must be an array")
        else:
            ids=set()
            for i,b in enumerate(blocks):
                p=f"blocks[{i}]"
                if not isinstance(b,dict): err(f"{p} must be an object"); continue
                bid=b.get("id")
                if not posint(bid): err(f"{p}.id must be a positive integer")
                elif bid in ids: err(f"duplicate block ID {bid} within this document")
                else: ids.add(bid)
                for message in validate_block(b): err(f"{p}: {message}")
    scalar_rel={"article":("authorId","relatedServiceId"),"service":("providerId",)}.get(kind,())
    for f in scalar_rel:
        if f in data and data[f] is not None and not posint(data[f]): err(f"field '{f}' must be a positive integer")
    array_rel={"article":("categoryIds","relatedArticleIds"),"service":("categoryIds","relatedServiceIds")}.get(kind,())
    for f in array_rel:
        if f in data:
            v=data[f]
            if not isinstance(v,list) or any(not posint(x) for x in v): err(f"field '{f}' must be an array of positive integers")
            elif len(v)!=len(set(v)): err(f"field '{f}' must not contain duplicate IDs")
    if kind=="page" and "parentPageId" in data and data["parentPageId"] is not None and not posint(data["parentPageId"]):
        err("field 'parentPageId' must be a positive integer")
    dates={}
    for f in ("publishedDate","updatedDate"):
        if f in data:
            d=utc_date(data[f])
            if d is None: err(f"field '{f}' must use ISO 8601 UTC seconds: YYYY-MM-DDTHH:mm:ssZ")
            else: dates[f]=d
    if len(dates)==2 and dates["updatedDate"]<dates["publishedDate"]: err("field 'updatedDate' must be equal to or later than 'publishedDate'")
    return out

def parse_collection_args(values):
    result={}
    for value in values:
        if "=" not in value: raise argparse.ArgumentTypeError(f"invalid --collection '{value}'; expected KIND=DIR")
        kind,directory=value.split("=",1)
        if kind not in {"homepage","menu","page","article","service","category"} or not directory:
            raise argparse.ArgumentTypeError(f"invalid --collection '{value}'")
        result[str(Path(directory).resolve())]=kind
    return result

def _relation_issue(issues, path, message):
    issues.append(Issue(path, message))

def validate_relations(documents):
    """Resolve declared foreign keys against the complete, globally indexed corpus."""
    issues=[]
    by_id={}
    for path,data,kind in documents:
        docid=data.get("id")
        if posint(docid): by_id.setdefault(docid,[]).append((path,data,kind))

    def resolve(source_path, source_id, field, target_id, allowed, location):
        if not posint(target_id): return
        matches=by_id.get(target_id,[])
        if not matches:
            _relation_issue(issues,source_path,f"{location} references missing {field} target ID {target_id}")
            return
        if len(matches)>1:
            _relation_issue(issues,source_path,f"{location} references ambiguous {field} target ID {target_id}; document ID is duplicated")
            return
        target_path,target_data,target_kind=matches[0]
        if target_kind not in allowed:
            expected="/".join(sorted(allowed))
            _relation_issue(issues,source_path,f"{location} target ID {target_id} has kind '{target_kind}', expected {expected}")

    parent_edges={}
    for path,data,kind in documents:
        docid=data.get("id")
        if not posint(docid): continue

        if kind=="page" and posint(data.get("parentPageId")):
            target=data["parentPageId"]
            resolve(path,docid,"parentPageId",target,{"page"},"parentPageId")
            if target==docid:
                _relation_issue(issues,path,f"parentPageId cannot reference the same Page ID {docid}")
            else: parent_edges[docid]=target

        if kind=="article":
            for field,target_kind in (("relatedServiceId","service"),):
                value=data.get(field)
                if value is not None: resolve(path,docid,field,value,{target_kind},field)
            for field,target_kind in (("categoryIds","category"),("relatedArticleIds","article")):
                values=data.get(field,[])
                if isinstance(values,list):
                    for target in values: resolve(path,docid,field,target,{target_kind},field)
            if data.get("authorId") is not None:
                _relation_issue(issues,path,"authorId cannot be validated: Author/Person target contract and collection are not defined; omit it until that contract exists")
            if docid in data.get("relatedArticleIds",[]) if isinstance(data.get("relatedArticleIds"),list) else False:
                _relation_issue(issues,path,f"relatedArticleIds cannot reference the source Article itself (ID {docid})")

        if kind=="service":
            for field,target_kind in (("categoryIds","category"),("relatedServiceIds","service")):
                values=data.get(field,[])
                if isinstance(values,list):
                    for target in values: resolve(path,docid,field,target,{target_kind},field)
            if data.get("providerId") is not None:
                _relation_issue(issues,path,"providerId cannot be validated: Organization/Provider target contract and collection are not defined; omit it until that contract exists")
            if docid in data.get("relatedServiceIds",[]) if isinstance(data.get("relatedServiceIds"),list) else False:
                _relation_issue(issues,path,f"relatedServiceIds cannot reference the source Service itself (ID {docid})")

        if kind=="menu":
            def menu_targets(items,where="items"):
                if not isinstance(items,list): return
                for i,item in enumerate(items):
                    if not isinstance(item,dict): continue
                    loc=f"{where}[{i}].pageId"
                    if item.get("pageId") is not None:
                        resolve(path,docid,"pageId",item["pageId"],{"homepage","page"},loc)
                    menu_targets(item.get("children"),f"{where}[{i}].children")
            menu_targets(data.get("items"))

        # Relations declared on block examples in the Content Contract.
        blocks=data.get("blocks",[])
        if isinstance(blocks,list):
            for i,block in enumerate(blocks):
                if not isinstance(block,dict): continue
                component=block.get("component")
                if "serviceIds" in block:
                    values=block["serviceIds"]
                    if not isinstance(values,list) or any(not posint(value) for value in values):
                        _relation_issue(issues,path,f"blocks[{i}].serviceIds must be an array of positive integers")
                    elif len(values)!=len(set(values)):
                        _relation_issue(issues,path,f"blocks[{i}].serviceIds must not contain duplicate IDs")
                    else:
                        for target in values: resolve(path,docid,"serviceIds",target,{"service"},f"blocks[{i}].serviceIds")
                if component=="content-list" and block.get("categoryId") is not None:
                    if not posint(block["categoryId"]):
                        _relation_issue(issues,path,f"blocks[{i}].categoryId must be a positive integer")
                    else:
                        resolve(path,docid,"categoryId",block["categoryId"],{"category"},f"blocks[{i}].categoryId")

    # A page hierarchy must be acyclic. Other related-content links may be reciprocal.
    visiting=set(); visited=set()
    def visit(node,trail):
        if node in visiting:
            cycle=trail[trail.index(node):]+[node] if node in trail else trail+[node]
            for source in cycle[:-1]:
                records=by_id.get(source,[])
                if len(records)==1:
                    _relation_issue(issues,records[0][0],f"parentPageId hierarchy contains a cycle: {' -> '.join(map(str,cycle))}")
            return
        if node in visited: return
        visiting.add(node)
        if node in parent_edges: visit(parent_edges[node],trail+[node])
        visiting.remove(node); visited.add(node)
    for node in parent_edges: visit(node,[])
    return issues

def validate_paths(paths,collection_map=None):
    issues=[]; seen={}; collection_map=collection_map or {}; documents=[]
    for path in sorted(paths):
        data,error=parse_frontmatter(path)
        if error: issues.append(Issue(path,error)); continue
        kind=ALIASES.get(path.parent.name.lower())
        for directory,mapped_kind in collection_map.items():
            try: path.resolve().relative_to(Path(directory)); kind=mapped_kind; break
            except ValueError: pass
        issues.extend(validate_document(path,data,kind))
        documents.append((path,data,kind))
        docid=data.get("id")
        if posint(docid):
            if docid in seen: issues.append(Issue(path,f"duplicate global document ID {docid}; first used in {seen[docid]}"))
            else: seen[docid]=path
    issues.extend(validate_relations(documents))
    return issues

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content_dir",type=Path)
    parser.add_argument("--collection",action="append",default=[],metavar="KIND=DIR",
        help="Explicit collection mapping; repeat for homepage, menu, page, article, service, category")
    args=parser.parse_args(argv)
    if not args.content_dir.is_dir(): print(f"ERROR: content directory does not exist: {args.content_dir}",file=sys.stderr); return 2
    try: mapping=parse_collection_args(args.collection)
    except argparse.ArgumentTypeError as exc: parser.error(str(exc))
    files=sorted(p for p in args.content_dir.rglob("*.md") if p.is_file())
    if not files: print(f"ERROR: no Markdown files found under {args.content_dir}",file=sys.stderr); return 2
    issues=validate_paths(files,mapping)
    if issues:
        for issue in issues: print(f"ERROR: {issue}")
        print(f"\nValidation failed: {len(issues)} issue(s) across {len(files)} Markdown file(s)."); return 1
    print(f"Validation passed: {len(files)} Markdown file(s); core and inferred document contracts are valid."); return 0

if __name__=="__main__": raise SystemExit(main())
