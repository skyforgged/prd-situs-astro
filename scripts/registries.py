"""Reference Schema and Block registries for the PRD Astro validator."""
SCHEMA_TYPES = {
 "block": {"FAQPage","HowTo","ItemList","VideoObject","ImageObject","Table","Course","Quiz","Question","Claim","Quotation","SpeakableSpecification"},
 "page": {"WebPage","Article","BlogPosting","TechArticle","NewsArticle","CollectionPage","AboutPage","ContactPage","ProfilePage","SearchResultsPage","QAPage","ItemPage"},
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

def validate_schema_object(schema, scope, kind=None, component=None):
 issues=[]
 if not isinstance(schema,dict): return ["schema must be an object"]
 allowed_keys={"type","mainEntity"} if scope=="document" else {"type"}
 for key in schema:
  if key not in allowed_keys: issues.append("schema has unsupported property '%s'" % key)
 st=schema.get("type")
 if not isinstance(st,str) or not st: return issues+["schema.type must be a non-empty string"]
 if scope=="document":
  if st not in PAGE_TYPES: issues.append("schema.type '%s' is not an allowed page-level Schema.org type" % st)
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
 if "schema" in block: issues.extend(validate_schema_object(block["schema"],"block",component=component))
 return issues
