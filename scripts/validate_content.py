#!/usr/bin/env python3
"""Validate PRD Astro Markdown frontmatter and per-kind content contracts."""
from __future__ import annotations
import argparse, json, re, sys
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

def load_extension_contracts(path, content_dir):
    if path is None: return {}, {}
    try:
        raw=yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    except (OSError,UnicodeError,yaml.YAMLError) as exc:
        raise ValueError("cannot read contract registry: %s" % exc)
    if not isinstance(raw,dict) or raw.get("version") != 1 or not isinstance(raw.get("collections"),dict):
        raise ValueError("contract registry must have version: 1 and a collections object")
    contracts={}; mapping={}
    core_kinds={"homepage","menu","page","article","service","category"}
    for kind,spec in raw["collections"].items():
        if kind in core_kinds or not re.fullmatch(r"[a-z][a-z0-9_-]*",str(kind)):
            raise ValueError("extension collection kind must be a new lowercase identifier: %r" % kind)
        if not isinstance(spec,dict) or not nonempty(spec.get("directory")):
            raise ValueError("extension '%s' requires a directory" % kind)
        required=spec.get("requiredFields",[])
        field_types=spec.get("fieldTypes",{})
        schema_types=spec.get("schemaTypes",[])
        schema_mappings=spec.get("schemaMappings",{})
        fixed_schema_type=spec.get("schemaType")
        route_prefix=spec.get("routePrefix")
        relations=spec.get("relations",{})
        if not isinstance(required,list) or any(not isinstance(x,str) for x in required):
            raise ValueError("extension '%s'.requiredFields must be an array of strings" % kind)
        allowed_types={"string","positive_int","boolean","object","array","utc_datetime","offset_datetime","iso_date_or_datetime","ulid","string_array","positive_int_array"}
        if not isinstance(field_types,dict) or any(not isinstance(v,str) or v not in allowed_types for v in field_types.values()):
            raise ValueError("extension '%s'.fieldTypes contains an unsupported field type" % kind)
        if not isinstance(schema_types,list) or any(not isinstance(x,str) or not x for x in schema_types):
            raise ValueError("extension '%s'.schemaTypes must be an array of strings" % kind)
        if not isinstance(schema_mappings,dict) or set(schema_types) - set(schema_mappings):
            raise ValueError("extension '%s' must define schemaMappings for every schemaType" % kind)
        if fixed_schema_type is not None and fixed_schema_type not in schema_types:
            raise ValueError("extension '%s'.schemaType must be one of schemaTypes" % kind)
        for schema_type,mapping_spec in schema_mappings.items():
            if schema_type not in schema_types or not isinstance(mapping_spec,dict):
                raise ValueError("extension '%s' has an invalid schemaMappings entry for '%s'" % (kind,schema_type))
            field_mapping=mapping_spec.get("fieldMapping")
            required_mapping_fields=mapping_spec.get("requiredFields",[])
            if not isinstance(field_mapping,dict) or not field_mapping or any(not isinstance(v,str) or not v for v in field_mapping.values()):
                raise ValueError("extension '%s' schema mapping '%s' requires a fieldMapping object" % (kind,schema_type))
            if not isinstance(required_mapping_fields,list) or any(not isinstance(v,str) for v in required_mapping_fields):
                raise ValueError("extension '%s' schema mapping '%s' requiredFields must be an array" % (kind,schema_type))
        if not isinstance(route_prefix,str) or not route_prefix.startswith("/") or "://" in route_prefix:
            raise ValueError("extension '%s'.routePrefix must be an absolute site path" % kind)
        if not isinstance(relations,dict):
            raise ValueError("extension '%s'.relations must be an object" % kind)
        for field,rel in relations.items():
            if not isinstance(rel,dict) or not nonempty(rel.get("target")) or rel.get("cardinality") not in {"one","many"}:
                raise ValueError("extension relation '%s.%s' requires target and cardinality one|many" % (kind,field))
            if "targetField" in rel and not nonempty(rel["targetField"]):
                raise ValueError("extension relation '%s.%s'.targetField must be a non-empty string" % (kind,field))
        directory=Path(spec["directory"])
        if not directory.is_absolute(): directory=(Path(content_dir).resolve()/directory).resolve()
        else: directory=directory.resolve()
        mapping[str(directory)]=kind
        contracts[kind]=dict(spec)
    for kind,spec in contracts.items():
        for field,rel in spec.get("relations",{}).items():
            target=rel["target"]
            if target not in core_kinds and target not in contracts:
                raise ValueError("extension relation '%s.%s' targets undeclared collection '%s'"%(kind,field,target))
            target_field=rel.get("targetField","id")
            if target in contracts and target_field != "id" and target_field not in contracts[target].get("fieldTypes",{}):
                raise ValueError("extension relation '%s.%s' targets undeclared field '%s.%s'"%(kind,field,target,target_field))
            if target in core_kinds and target_field != "id":
                raise ValueError("extension relation '%s.%s' may target only document ID on a core collection"%(kind,field))
            source_type=spec.get("fieldTypes",{}).get(field)
            target_type="positive_int" if target_field=="id" else contracts[target].get("fieldTypes",{}).get(target_field)
            normalized_source={"positive_int_array":"positive_int","string_array":"string"}.get(source_type,source_type)
            if normalized_source and target_type and normalized_source != target_type:
                raise ValueError("extension relation '%s.%s' source and target field types do not match"%(kind,field))
    return contracts,mapping


def _has_timezone(value):
    try:
        parsed=datetime.fromisoformat(value.replace("Z","+00:00"))
        return parsed.tzinfo is not None and parsed.utcoffset() is not None
    except (ValueError,AttributeError):
        return False


def _is_iso_date_or_datetime(value):
    try:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}",value):
            datetime.strptime(value,"%Y-%m-%d")
        else:
            datetime.fromisoformat(value.replace("Z","+00:00"))
        return True
    except (ValueError,AttributeError):
        return False


def validate_extension_document(path,data,kind,spec):
    issues=[]
    def err(message): issues.append(Issue(path,"extension '%s': %s"%(kind,message)))
    if not posint(data.get("id")): err("field 'id' must be a positive integer")
    for field in spec.get("requiredFields",[]):
        if field not in data: err("missing required field '%s'"%field)
    validators={
        "string":lambda v:isinstance(v,str),
        "positive_int":posint,
        "boolean":lambda v:isinstance(v,bool),
        "object":lambda v:isinstance(v,dict),
        "array":lambda v:isinstance(v,list),
        "utc_datetime":lambda v:utc_date(v) is not None,
        "offset_datetime":lambda v:isinstance(v,str) and _has_timezone(v),
        "iso_date_or_datetime":lambda v:isinstance(v,str) and _is_iso_date_or_datetime(v),
        "ulid":lambda v:isinstance(v,str) and bool(re.fullmatch(r"[0-9A-HJKMNP-TV-Z]{26}",v)),
        "string_array":lambda v:isinstance(v,list) and all(isinstance(x,str) for x in v),
        "positive_int_array":lambda v:isinstance(v,list) and all(posint(x) for x in v),
    }
    for field,field_type in spec.get("fieldTypes",{}).items():
        if field in data and not validators[field_type](data[field]):
            err("field '%s' must be %s"%(field,field_type))
    schema=data.get("schema")
    allowed=spec.get("schemaTypes",[])
    schema_type=spec.get("schemaType")
    if schema_type is None:
        schema_type=schema.get("type") if isinstance(schema,dict) else None
        if schema_type not in allowed:
            err("schema.type must be one of the extension's declared schemaTypes: %s"%", ".join(allowed))
    elif schema_type not in allowed:
        err("schemaType must be one of the extension's declared schemaTypes")
    if schema_type in allowed:
        mapping_spec=spec.get("schemaMappings",{}).get(schema_type,{})
        for field in mapping_spec.get("requiredFields",[]):
            if field not in data: err("schema mapping '%s' requires source field '%s'"%(schema_type,field))
        for output_field,source_field in mapping_spec.get("fieldMapping",{}).items():
            if source_field not in data: err("schema mapping '%s.%s' references missing source field '%s'"%(schema_type,output_field,source_field))
    slug=data.get("slug")
    if "slug" in data and (not nonempty(slug) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",slug)):
        err("slug must use lowercase ASCII letters/numbers separated by single hyphens")
    return issues


def validate_extension_relations(documents,contracts):
    issues=[]
    indexes={}
    for path,data,kind in documents:
        for field,value in data.items():
            if isinstance(value,(str,int)) and not isinstance(value,bool):
                indexes.setdefault((kind,field,value),[]).append(path)
    for path,data,kind in documents:
        spec=contracts.get(kind,{})
        for field,rel in spec.get("relations",{}).items():
            value=data.get(field)
            if value is None: continue
            target_field=rel.get("targetField","id")
            source_type=spec.get("fieldTypes",{}).get(field)
            is_many=rel["cardinality"]=="many"
            targets=value if is_many and isinstance(value,list) else [value]
            if is_many and not isinstance(value,list):
                issues.append(Issue(path,"extension relation '%s' must be an array"%field)); continue
            if is_many and len(targets)!=len(set(targets)):
                issues.append(Issue(path,"extension relation '%s' must not contain duplicate values"%field)); continue
            for target_value in targets:
                valid=nonempty(target_value) if source_type in {"string","string_array"} else posint(target_value)
                if not valid:
                    expected="non-empty strings" if source_type=="string" else "positive integer IDs"
                    issues.append(Issue(path,"extension relation '%s' must contain %s"%(field,expected))); continue
                matches=indexes.get((rel["target"],target_field,target_value),[])
                if len(matches)!=1:
                    reason="missing" if not matches else "ambiguous"
                    issues.append(Issue(path,"extension relation '%s' references %s %s.%s value %r"%(field,reason,rel["target"],target_field,target_value)))
    return issues


def parse_collection_args(values):
    result={}
    for value in values:
        if "=" not in value: raise argparse.ArgumentTypeError(f"invalid --collection '{value}'; expected KIND=DIR")
        kind,directory=value.split("=",1)
        if kind not in {"homepage","menu","page","article","service","category"} or not directory:
            raise argparse.ArgumentTypeError(f"invalid --collection '{value}'; --collection maps only the six core kinds")
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

def validate_paths(paths,collection_map=None,extension_contracts=None):
    issues=[]; seen={}; collection_map=collection_map or {}; documents=[]
    for path in sorted(paths):
        data,error=parse_frontmatter(path)
        if error: issues.append(Issue(path,error)); continue
        kind=ALIASES.get(path.parent.name.lower())
        for directory,mapped_kind in collection_map.items():
            try: path.resolve().relative_to(Path(directory)); kind=mapped_kind; break
            except ValueError: pass
        if kind in (extension_contracts or {}):
            issues.extend(validate_extension_document(path,data,kind,extension_contracts[kind]))
        else:
            issues.extend(validate_document(path,data,kind))
        documents.append((path,data,kind))
        docid=data.get("id")
        if posint(docid):
            if docid in seen: issues.append(Issue(path,f"duplicate global document ID {docid}; first used in {seen[docid]}"))
            else: seen[docid]=path
    issues.extend(validate_relations(documents))
    issues.extend(validate_extension_relations(documents,extension_contracts or {}))
    return issues



def validate_seo_uniqueness(documents):
    issues=[]; canonical_seen={}
    for path,data,kind in documents:
        seo=data.get("seo",{}) if isinstance(data,dict) else {}
        if not isinstance(seo,dict): continue
        canonical=seo.get("canonical")
        if nonempty(canonical):
            normalized=canonical.rstrip("/")
            if normalized in canonical_seen:
                issues.append(Issue(path,"[QG-07 DUPLICATE_CANONICAL] canonical URL '%s' is also used by %s"%(canonical,canonical_seen[normalized])))
            else: canonical_seen[normalized]=path
    return issues

def _route_for(kind, slug, prefixes):
    if kind == "homepage": return "/"
    prefix = prefixes.get(kind, {"page":"/", "article":"/articles/", "service":"/services/", "category":"/categories/"}.get(kind, "/"))
    if not isinstance(prefix,str) or not prefix.startswith("/") or "://" in prefix:
        raise ValueError("route prefix for %s must be an absolute site path" % kind)
    return prefix.rstrip("/") + "/" + slug.strip("/") + "/"

def validate_routes(documents, route_prefixes=None):
    issues=[]; seen={}
    prefixes=route_prefixes or {}
    slug_re=re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    routes={}
    for path,data,kind in documents:
        if kind=="menu" or kind is None: continue
        slug=data.get("slug")
        if not nonempty(slug): continue
        if not slug_re.fullmatch(slug):
            issues.append(Issue(path,"[QG-04 INVALID_SLUG] slug must use lowercase ASCII letters/numbers separated by single hyphens"))
            continue
        try: route=_route_for(kind,slug,prefixes)
        except ValueError as exc:
            issues.append(Issue(path,"[QG-04 INVALID_ROUTE_PREFIX] "+str(exc))); continue
        normalized="/" + "/".join(part for part in route.split("/") if part)
        if route.endswith("/") and normalized!="/": normalized+="/"
        if normalized in routes:
            issues.append(Issue(path,"[QG-04 ROUTE_COLLISION] route %s is also generated by %s" % (normalized,routes[normalized])))
        else: routes[normalized]=path
    return issues,routes

def _walk_references(value, prefix=""):
    if isinstance(value,dict):
        for key,item in value.items():
            where=(prefix+"."+str(key)).strip(".")
            if isinstance(item,str) and key in {"url","href"}:
                yield ("link",item,where)
            elif isinstance(item,str) and key in {"src","poster"}:
                yield ("asset",item,where)
            else: yield from _walk_references(item,where)
    elif isinstance(value,list):
        for i,item in enumerate(value): yield from _walk_references(item,"%s[%d]"%(prefix,i))

def _is_external(value):
    parsed=urlparse(value)
    return bool(parsed.scheme or parsed.netloc) or value.startswith(("mailto:","tel:","data:","javascript:","#"))

def _resolve_local_asset(value, source_path, site_root):
    clean=value.split("#",1)[0].split("?",1)[0]
    if not clean: return None
    if clean.startswith("/"):
        candidates=[site_root/"public"/clean.lstrip("/"),site_root/"src"/"assets"/clean.lstrip("/")]
    else:
        candidates=[source_path.parent/clean,site_root/"public"/clean,site_root/clean]
    return next((p for p in candidates if p.is_file()),candidates[0])

def validate_assets_and_links(documents, site_root, routes):
    issues=[]
    if site_root is None: return issues
    root=Path(site_root).resolve()
    for path,data,kind in documents:
        if not isinstance(data,dict): continue
        for ref_type,value,where in _walk_references(data):
            if not nonempty(value) or _is_external(value): continue
            if ref_type=="asset":
                # Only source/poster values that look like media paths are asset references.
                if not re.search(r"\.(?:avif|gif|jpe?g|png|svg|webp|mp4|webm|pdf|woff2?)(?:[?#]|$)",value,re.I): continue
                target=_resolve_local_asset(value,path,root)
                if target is not None and not target.is_file():
                    issues.append(Issue(path,"[QG-09 ASSET_NOT_FOUND] %s references missing asset '%s'"%(where,value)))
            elif ref_type=="link":
                parsed=urlparse(value)
                if parsed.path.startswith("/") and parsed.path not in {"/"}:
                    candidate=parsed.path.rstrip("/")+"/"
                    if candidate not in routes and parsed.path not in routes:
                        # Ignore paths pointing to static assets; those are checked by asset validation.
                        if not re.search(r"\.[a-z0-9]{2,8}$",parsed.path,re.I):
                            issues.append(Issue(path,"[QG-09 INTERNAL_LINK_NOT_FOUND] %s points to unknown route '%s'"%(where,value)))
        # Markdown links in the non-frontmatter body are checked against generated routes.
        try: source=path.read_text(encoding="utf-8")
        except (OSError,UnicodeError): continue
        match=FRONTMATTER_RE.match(source)
        body=source[match.end():] if match else source
        for target in re.findall(r"!??\[[^\]]*\]\(([^)]+)\)",body):
            target=target.strip().split()[0].strip("<>")
            if not target or _is_external(target): continue
            parsed=urlparse(target)
            if parsed.path.startswith("/") and not re.search(r"\.[a-z0-9]{2,8}$",parsed.path,re.I):
                normalized=parsed.path if parsed.path=="/" else parsed.path.rstrip("/")+"/"
                if normalized not in routes:
                    issues.append(Issue(path,"[QG-09 INTERNAL_LINK_NOT_FOUND] Markdown link points to unknown route '%s'"%target))
            elif parsed.path and not parsed.path.startswith("/"):
                if re.search(r"\.(?:avif|gif|jpe?g|png|svg|webp|mp4|webm|pdf)$",parsed.path,re.I):
                    target_file=_resolve_local_asset(parsed.path,path,root)
                    if target_file is not None and not target_file.is_file():
                        issues.append(Issue(path,"[QG-09 ASSET_NOT_FOUND] Markdown media references missing asset '%s'"%target))
    return issues

def validate_route_manifest(manifest_path, site_root, routes):
    issues=[]
    try:
        manifest=yaml.safe_load(Path(manifest_path).read_text(encoding="utf-8"))
    except (OSError,UnicodeError,yaml.YAMLError) as exc:
        return [Issue(Path(manifest_path),"[QG-13 INVALID_MANIFEST] cannot read route manifest: %s"%exc)]
    if not isinstance(manifest,dict) or not isinstance(manifest.get("routes"),list):
        return [Issue(Path(manifest_path),"[QG-13 INVALID_MANIFEST] manifest must contain a routes array")]
    declared=set()
    for i,item in enumerate(manifest["routes"]):
        if not isinstance(item,dict) or not nonempty(item.get("path")) or not item["path"].startswith("/"):
            issues.append(Issue(Path(manifest_path),"[QG-13 INVALID_ROUTE] routes[%d] requires an absolute path"%i)); continue
        route=item["path"]
        if route in declared: issues.append(Issue(Path(manifest_path),"[QG-13 ROUTE_COLLISION] duplicate manifest route '%s'"%route))
        declared.add(route)
        source=item.get("source")
        if source:
            source_path=(Path(site_root)/source).resolve()
            if not source_path.is_file(): issues.append(Issue(Path(manifest_path),"[QG-13 SOURCE_NOT_FOUND] route '%s' source '%s' does not exist"%(route,source)))
        if item.get("indexable") is True and route not in routes and route.rstrip("/")+"/" not in routes:
            # The manifest is authoritative; an explicit source can represent routes outside the content collections.
            if not source: issues.append(Issue(Path(manifest_path),"[QG-13 INDEXABLE_ROUTE_UNMAPPED] indexable route '%s' has no source"%route))
    for route,path in routes.items():
        if route not in declared:
            issues.append(Issue(Path(manifest_path),"[QG-13 ROUTE_NOT_IN_MANIFEST] generated route '%s' from %s is absent from manifest"%(route,path)))
    sitemap=manifest.get("sitemap")
    if sitemap:
        sitemap_path=Path(site_root)/sitemap
        if not sitemap_path.is_file(): issues.append(Issue(Path(manifest_path),"[QG-13 SITEMAP_NOT_FOUND] sitemap '%s' does not exist"%sitemap))
        else:
            xml=sitemap_path.read_text(encoding="utf-8",errors="replace")
            for route,item in ((x["path"],x) for x in manifest["routes"] if isinstance(x,dict) and x.get("indexable") is True):
                if route.rstrip("/")+"/" not in xml and route not in xml:
                    issues.append(Issue(Path(manifest_path),"[QG-13 SITEMAP_ROUTE_MISSING] indexable route '%s' is absent from sitemap"%route))
    redirects=manifest.get("redirects",[])
    if not isinstance(redirects,list): issues.append(Issue(Path(manifest_path),"[QG-13 INVALID_REDIRECTS] redirects must be an array"))
    else:
        for i,item in enumerate(redirects):
            if not isinstance(item,dict) or not nonempty(item.get("from")) or not nonempty(item.get("to")):
                issues.append(Issue(Path(manifest_path),"[QG-13 INVALID_REDIRECT] redirects[%d] requires from and to"%i))
            elif item["from"]==item["to"]:
                issues.append(Issue(Path(manifest_path),"[QG-13 REDIRECT_LOOP] redirect from and to cannot be identical"))
    return issues


def _load_route_prefixes(path):
    if path is None: return {}
    try:
        value=json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError,UnicodeError,json.JSONDecodeError) as exc:
        raise ValueError("cannot read route-prefix JSON: %s" % exc)
    if not isinstance(value,dict) or any(not isinstance(k,str) or not isinstance(v,str) for k,v in value.items()):
        raise ValueError("route-prefix JSON must be an object of string keys and string values")
    return value


def _load_documents(files, collection_map):
    documents=[]
    for path in files:
        data,error=parse_frontmatter(path)
        if error or data is None: continue
        kind=ALIASES.get(path.parent.name.lower())
        for directory,mapped_kind in collection_map.items():
            try:
                path.resolve().relative_to(Path(directory))
                kind=mapped_kind
                break
            except ValueError:
                pass
        documents.append((path,data,kind))
    return documents


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content_dir",type=Path)
    parser.add_argument("--collection",action="append",default=[],metavar="KIND=DIR",
        help="Explicit mapping to one of the six core contract kinds")
    parser.add_argument("--site-root",type=Path,default=None,help="Project root for local asset resolution")
    parser.add_argument("--route-manifest",type=Path,default=None,help="YAML route manifest for QG-13")
    parser.add_argument("--route-prefixes",type=Path,default=None,help="JSON mapping of collection kinds to route prefixes")
    parser.add_argument("--contract-registry",type=Path,default=None,help="YAML registry for project-specific collection contracts (version 1)")
    args=parser.parse_args(argv)
    if not args.content_dir.is_dir():
        print(f"ERROR: content directory does not exist: {args.content_dir}",file=sys.stderr)
        return 2
    try:
        mapping=parse_collection_args(args.collection)
        contracts,extension_mapping=load_extension_contracts(args.contract_registry,args.content_dir)
        mapping.update(extension_mapping)
        prefixes=_load_route_prefixes(args.route_prefixes)
        for kind,spec in contracts.items():
            if kind in prefixes: raise ValueError("route prefix for '%s' is defined in both contract registry and --route-prefixes"%kind)
            prefixes[kind]=spec["routePrefix"]
    except (argparse.ArgumentTypeError,ValueError) as exc:
        parser.error(str(exc))
    if args.route_manifest and not args.site_root:
        parser.error("--route-manifest requires --site-root")
    files=sorted(p for p in args.content_dir.rglob("*.md") if p.is_file())
    if not files:
        print(f"ERROR: no Markdown files found under {args.content_dir}",file=sys.stderr)
        return 2

    issues=validate_paths(files,mapping,contracts)
    documents=_load_documents(files,mapping)
    issues.extend(validate_seo_uniqueness(documents))
    route_issues,routes=validate_routes(documents,prefixes)
    issues.extend(route_issues)
    if args.site_root:
        if not args.site_root.is_dir():
            parser.error(f"--site-root does not exist or is not a directory: {args.site_root}")
        issues.extend(validate_assets_and_links(documents,args.site_root,routes))
    if args.route_manifest:
        issues.extend(validate_route_manifest(args.route_manifest,args.site_root,routes))

    if issues:
        for issue in issues:
            print(f"ERROR: {issue}")
        print(f"\nValidation failed: {len(issues)} issue(s) across {len(files)} Markdown file(s).")
        return 1
    checks=["core and extension contracts","relations","schema/block registry","canonical uniqueness","slug/routes"]
    if args.site_root: checks.append("assets/internal links")
    if args.route_manifest: checks.append("route manifest/sitemap/redirects")
    print("Validation passed: %d Markdown file(s); checks: %s."%(len(files),", ".join(checks)))
    return 0

if __name__=="__main__": raise SystemExit(main())
