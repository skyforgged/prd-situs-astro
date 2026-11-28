"""Reference Schema and Block registries for the PRD Astro validator."""
SCHEMA_TYPES = {
 "block": {"FAQPage","HowTo","ItemList","VideoObject","ImageObject","Table","Course","Quiz","Question","Claim","Quotation","SpeakableSpecification"},
 "page": {"WebPage","SiteNavigationElement","Service","Article","BlogPosting","TechArticle","NewsArticle","CollectionPage","AboutPage","ContactPage","ProfilePage","SearchResultsPage","QAPage","ItemPage"},
 "entity": {"Service","ProfessionalService","LocalBusiness","Organization","Person","DefinedTerm","Offer","AggregateOffer","Review","AggregateRating","ContactPoint","PostalAddress","GeoCoordinates","Event","JobPosting","Dataset","SoftwareApplication"},
}
PAGE_TYPES = SCHEMA_TYPES["page"]
ENTITY_TYPES = SCHEMA_TYPES["entity"]
BLOCK_COMPONENTS = {
 "card","faq","cta","table","note","steps","stats","glossary","quote","section","process-timeline",
 "checklist-card","comparison-table","document-list","image-panel","feature-card-grid","stats-grid",
 "source-links","contact-panel","multi-step-form","page-header","home-hero","service-list","home-process",
 "article-list","home-cta","not-found","content-section","howto","hero","link-grid","listing",
 "upcoming-schedules","contact","rich-text","image","how-to","item-list","content-list","service-grid",
}
COMMON = {
 "id":"int","component":"str","title":"str","eyebrow":"str","description":"str","intro":"str",
 "content":"str","text":"str","label":"str","url":"str","href":"str","src":"str","alt":"str",
 "caption":"str","variant":"str","layout":"str","surface":"str","items":"list","steps":"list",
 "columns":"list","rows":"list","headers":"list","serviceIds":"intlist","articleIds":"intlist",
 "categoryId":"int","categoryIds":"intlist","source":"str","limit":"int","showDate":"bool",
 "schema":"dict","image":"dict","imageAlt":"str","actionLabel":"str","emptyTitle":"str",
 "emptyDescription":"str","phone":"str","email":"str","address":"str","name":"str",
 "value":"str","number":"str","icon":"str","class":"str","theme":"str",
}
COMPONENT_PROPS = {
 "faq":{"title","eyebrow","description","items","schema"},
 "how-to":{"title","description","steps","schema","layout","variant"},
 "howto":{"title","description","steps","schema","layout","surface"},
 "item-list":{"title","description","items","schema","layout","variant"},
 "content-list":{"title","description","source","categoryId","limit","schema"},
 "service-grid":{"title","description","serviceIds","layout","variant"},
 "hero":{"title","eyebrow","description","src","alt","image","imageAlt","variant","surface"},
 "home-hero":{"title","eyebrow","description","src","alt","image","imageAlt","variant"},
 "cta":{"title","eyebrow","description","label","url","href","variant","surface"},
 "steps":{"title","description","items","steps","schema","layout"},
 "table":{"title","description","headers","rows","items","schema"},
 "image":{"src","alt","caption","schema"},
 "rich-text":{"title","content","text","schema"},
 "content-section":{"title","eyebrow","description","items","layout","surface"},
 "link-grid":{"title","eyebrow","description","items","surface"},
 "listing":{"title","eyebrow","description","source","surface","emptyTitle","emptyDescription","actionLabel","url"},
 "upcoming-schedules":{"title","eyebrow","description","surface","emptyTitle","emptyDescription"},
 "contact":{"title","eyebrow","description","surface","phone","email","address"},
}
SCHEMA_BLOCKS = {"faq":{"FAQPage"},"how-to":{"HowTo"},"howto":{"HowTo"},"item-list":{"ItemList"},"steps":{"HowTo"},"table":{"Table"},"image":{"ImageObject"}}


SCHEMA_REGISTRY = {
 "WebPage":{"scope":"page","fieldMapping":{"name":"document.title","description":"document.description","url":"route.canonical"},"requiredFields":["document.title","route.canonical"],"optionalFields":["document.description","document.featuredImage"],"googleRichResultSupport":"not-applicable","mergeStrategy":"merge-by-stable-node-id","prohibitedUsage":["creating a new page node for each block"],"documentationUrl":["https://schema.org/WebPage"]},
 "Article":{"scope":"page","fieldMapping":{"headline":"document.title","description":"document.description","datePublished":"document.publishedDate","dateModified":"document.updatedDate","image":"document.featuredImage"},"requiredFields":["document.title"],"optionalFields":["document.description","document.publishedDate","document.updatedDate","document.featuredImage"],"googleRichResultSupport":"unknown","mergeStrategy":"merge-by-stable-node-id","prohibitedUsage":["invented author or publication dates"],"documentationUrl":["https://schema.org/Article"]},
 "Service":{"scope":"page","fieldMapping":{"name":"document.title","description":"document.description"},"requiredFields":["document.title"],"optionalFields":["document.description"],"googleRichResultSupport":"not-applicable","mergeStrategy":"merge-by-stable-node-id","prohibitedUsage":["inventing provider or offer data"],"documentationUrl":["https://schema.org/Service"]},
 "FAQPage":{"scope":"block","supportedComponents":["faq"],"fieldMapping":{"mainEntity":"items[].question+items[].answer"},"requiredFields":["items","items[].question","items[].answer"],"optionalFields":["title"],"googleRichResultSupport":"not-supported","mergeStrategy":"merge-by-stable-node-id","prohibitedUsage":["hidden or non-visible questions and answers"],"documentationUrl":["https://schema.org/FAQPage"]},
 "HowTo":{"scope":"block","supportedComponents":["how-to","howto","steps"],"fieldMapping":{"name":"title","description":"description","step":"steps[].name+steps[].text"},"requiredFields":["title","steps","steps[].name","steps[].text"],"optionalFields":["description"],"googleRichResultSupport":"not-supported","mergeStrategy":"merge-by-stable-node-id","prohibitedUsage":["benefit lists or unordered service lists"],"documentationUrl":["https://schema.org/HowTo"]},
 "ItemList":{"scope":"block","supportedComponents":["item-list"],"fieldMapping":{"itemListElement":"items[]"},"requiredFields":["items"],"optionalFields":["title","description"],"googleRichResultSupport":"not-applicable","mergeStrategy":"merge-by-stable-node-id","prohibitedUsage":["schema items that differ from visible items"],"documentationUrl":["https://schema.org/ItemList"]},
 "DefinedTerm":{"scope":"entity","entitySource":"document.title+document.intro","fieldMapping":{"name":"document.title","description":"document.intro"},"requiredFields":["document.title","document.intro"],"optionalFields":[],"googleRichResultSupport":"not-applicable","mergeStrategy":"reuse-entity-node","prohibitedUsage":["ordinary articles that do not define a single term"],"documentationUrl":["https://schema.org/DefinedTerm"]},
 "SiteNavigationElement":{"scope":"page","fieldMapping":{"name":"document.title"},"requiredFields":["document.title"],"optionalFields":[],"mappingStatus":"supported","googleRichResultSupport":"not-applicable","mergeStrategy":"merge-by-stable-node-id","prohibitedUsage":["inventing navigation targets"],"documentationUrl":["https://schema.org/SiteNavigationElement"]},
}

# Explicitly accepted page types without a generic source mapping. These are
# declaration-only: projects must add a project registry mapping before using
# them as generated JSON-LD types.
SCHEMA_DECLARATION_ONLY = PAGE_TYPES - {name for name, entry in SCHEMA_REGISTRY.items() if entry.get("scope") == "page"}
SCHEMA_TYPE_STATUS = {
 name: ("mapped" if name in SCHEMA_REGISTRY and SCHEMA_REGISTRY[name].get("scope") == "page" else "declaration-only")
 for name in PAGE_TYPES
}


def validate_schema_object(schema, scope, kind=None, component=None):
 issues=[]
 if not isinstance(schema,dict): return ["schema must be an object"]
 allowed_keys={"type","mainEntity"} if scope=="document" else {"type"}
 for key in schema:
  if key not in allowed_keys: issues.append("schema has unsupported property '%s'" % key)
 st=schema.get("type")
 if not isinstance(st,str) or not st: return issues+["schema.type must be a non-empty string"]
 if scope=="document":
  if st not in (PAGE_TYPES | ({"SiteNavigationElement"} if kind=="menu" else set()) | ({"Service"} if kind=="service" else set())): issues.append("schema.type '%s' is not an allowed page-level Schema.org type" % st)
  elif st not in SCHEMA_TYPE_STATUS: issues.append("schema.type '%s' has no explicit registry status" % st)
  main=schema.get("mainEntity")
  if main is not None:
   if not isinstance(main,dict) or set(main)!={"type"} or main.get("type") not in ENTITY_TYPES:
    issues.append("schema.mainEntity must be an object with an allowed entity-level 'type'")
   elif main.get("type")!="DefinedTerm": issues.append("schema.mainEntity.type is not enabled for this reference contract")
   elif kind!="page": issues.append("schema.mainEntity.type 'DefinedTerm' is only allowed for Page documents")
 else:
  if st not in SCHEMA_TYPES["block"]: issues.append("block schema.type '%s' is not in the block Schema Registry" % st)
  elif component and st not in SCHEMA_BLOCKS.get(component,set()):
   issues.append("schema type '%s' is not permitted for component '%s'" % (st,component))
 return issues

def validate_block(block):
 issues=[]
 component=block.get("component")
 if not isinstance(component,str) or not component.strip(): return ["component must be a non-empty string"]
 if component not in BLOCK_COMPONENTS: return ["unknown block component '%s' (not registered in Block Registry)" % component]
 allowed=COMPONENT_PROPS.get(component,set(COMMON))
 for key,value in block.items():
  if key not in COMMON: issues.append("block '%s' has unsupported prop '%s'" % (component,key)); continue
  if key not in {"id","component"} and component in COMPONENT_PROPS and key not in allowed:
   issues.append("block '%s' does not allow prop '%s'" % (component,key))
  if key in {"id","component","schema"}: continue
  typ=COMMON[key]
  valid={"str":lambda v:isinstance(v,str),"int":lambda v:isinstance(v,int) and not isinstance(v,bool) and v>0,
   "intlist":lambda v:isinstance(v,list) and all(isinstance(x,int) and not isinstance(x,bool) and x>0 for x in v),
   "list":lambda v:isinstance(v,list),"dict":lambda v:isinstance(v,dict),"bool":lambda v:isinstance(v,bool)}[typ]
  if not valid(value): issues.append("block '%s' prop '%s' must be %s" % (component,key,typ))
 if "schema" in block:
  issues.extend(validate_schema_object(block["schema"],"block",component=component))
  st=block["schema"].get("type") if isinstance(block["schema"],dict) else None
  entry=SCHEMA_REGISTRY.get(st,{})
  for field in entry.get("requiredFields",[]):
   root=field.split(".")[0]
   if root.endswith("[]"): root=root[:-2]
   if root not in block or block.get(root) in (None,"",[]): issues.append("schema '%s' requires block field '%s'" % (st,root))
  if st=="FAQPage" and isinstance(block.get("items"),list):
   for i,item in enumerate(block["items"]):
    if not isinstance(item,dict) or not isinstance(item.get("question"),str) or not item["question"].strip() or not isinstance(item.get("answer"),str) or not item["answer"].strip():
     issues.append("FAQPage items[%d] must contain non-empty question and answer" % i)
  if st=="HowTo" and isinstance(block.get("steps"),list):
   for i,item in enumerate(block["steps"]):
    if not isinstance(item,dict) or not isinstance(item.get("name"),str) or not item["name"].strip() or not isinstance(item.get("text"),str) or not item["text"].strip():
     issues.append("HowTo steps[%d] must contain non-empty name and text" % i)
 return issues
