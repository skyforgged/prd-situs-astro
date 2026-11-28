from pathlib import Path
import sys
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_content import parse_frontmatter, validate_document, validate_paths

def write_md(path: Path, frontmatter: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{frontmatter}\n---\n\nKonten.", encoding="utf-8")
    return path

PAGE = """id: 1
slug: tentang
title: Tentang Kami
description: Profil perusahaan.
intro: PT Contoh menyediakan layanan profesional untuk kebutuhan pelanggan.
schema:
  type: WebPage
seo:
  title: Tentang Kami
  description: Profil perusahaan.
blocks:
  - id: 1
    component: rich-text
updatedDate: 2026-11-26T03:00:00Z"""

def test_valid_page_contract(tmp_path: Path):
    file = write_md(tmp_path / "pages/page.md", PAGE)
    assert validate_paths([file]) == []

def test_duplicate_yaml_keys_are_rejected(tmp_path: Path):
    file = write_md(tmp_path / "pages/duplicate.md", """id: 1
id: 2
schema:
  type: WebPage""")
    data, error = parse_frontmatter(file)
    assert data is None
    assert "duplicate YAML key" in error

def test_document_ids_are_global_across_files(tmp_path: Path):
    first = write_md(tmp_path / "pages/a.md", PAGE)
    second = write_md(tmp_path / "articles/b.md", PAGE.replace("type: WebPage", "type: Article").replace("id: 1", "id: 1"))
    issues = validate_paths([first, second])
    assert any("duplicate global document ID 1" in issue.message for issue in issues)

def test_block_ids_are_local_and_must_be_unique(tmp_path: Path):
    source = PAGE.replace("  - id: 1\n    component: rich-text", "  - id: 1\n    component: rich-text\n  - id: 1\n    component: faq")
    issues = validate_document(tmp_path / "pages/page.md", __import__("yaml").safe_load(source), "page")
    assert any("duplicate block ID 1" in issue.message for issue in issues)

@pytest.mark.parametrize("timestamp", ["2026-11-26T03:00:00+07:00", "2026-11-26T03:00:00", "2026-11-26T03:00:00.123Z", "2026-11-26"])
def test_noncanonical_timestamps_are_rejected(tmp_path: Path, timestamp: str):
    source = PAGE.replace("2026-11-26T03:00:00Z", f"'{timestamp}'")
    issues = validate_document(tmp_path / "pages/page.md", __import__("yaml").safe_load(source), "page")
    assert any("ISO 8601 UTC seconds" in issue.message for issue in issues)

def test_updated_date_cannot_precede_published_date(tmp_path: Path):
    source = PAGE + "\npublishedDate: 2026-11-27T03:00:00Z"
    issues = validate_document(tmp_path / "pages/page.md", __import__("yaml").safe_load(source), "page")
    assert any("updatedDate' must be equal to or later" in issue.message for issue in issues)

def test_boolean_is_not_accepted_as_integer_id(tmp_path: Path):
    source = PAGE.replace("id: 1", "id: true")
    issues = validate_document(tmp_path / "pages/page.md", __import__("yaml").safe_load(source), "page")
    assert any("positive integer" in issue.message for issue in issues)

def test_homepage_contract_requires_seo_and_blocks(tmp_path: Path):
    source = """id: 1
slug: home
title: Beranda
description: Ringkasan.
schema:
  type: WebPage
seo:
  title: Beranda
  description: Ringkasan.
blocks: []
updatedDate: 2026-11-26T03:00:00Z"""
    assert validate_document(tmp_path / "homepages/home.md", __import__("yaml").safe_load(source), "homepage") == []

def test_menu_requires_exactly_one_target_and_valid_location(tmp_path: Path):
    source = """id: 2
slug: main
title: Menu Utama
schema:
  type: SiteNavigationElement
location: sidebar
items:
  - label: Invalid
    pageId: 1
    url: https://example.com
updatedDate: 2026-11-26T03:00:00Z"""
    issues = validate_document(tmp_path / "menus/main.md", __import__("yaml").safe_load(source), "menu")
    assert any("location" in issue.message for issue in issues)
    assert any("exactly one target" in issue.message for issue in issues)

def test_menu_rejects_depth_greater_than_three(tmp_path: Path):
    source = """id: 2
slug: main
title: Menu
schema:
  type: SiteNavigationElement
location: header
items:
  - label: One
    pageId: 1
    children:
      - label: Two
        pageId: 2
        children:
          - label: Three
            pageId: 3
            children:
              - label: Four
                pageId: 4
updatedDate: 2026-11-26T03:00:00Z"""
    issues = validate_document(tmp_path / "menus/main.md", __import__("yaml").safe_load(source), "menu")
    assert any("maximum menu depth of 3" in issue.message for issue in issues)

def test_article_requires_intro_image_dates_and_seo(tmp_path: Path):
    source = """id: 5
slug: artikel
title: Artikel
description: Ringkasan
intro: Intro substantif satu paragraf.
schema:
  type: Article
seo: {}
featuredImage:
  src: /images/a.webp
  alt: Foto dokumen yang sedang diperiksa.
publishedDate: 2026-11-20T01:00:00Z
updatedDate: 2026-11-26T03:00:00Z
blocks: []"""
    assert validate_document(tmp_path / "articles/a.md", __import__("yaml").safe_load(source), "article") == []

def test_article_rejects_missing_or_invalid_featured_image(tmp_path: Path):
    source = """id: 5
slug: artikel
title: Artikel
description: Ringkasan
intro: Intro substantif.
schema:
  type: Article
seo:
  title: Artikel
  description: Ringkasan
publishedDate: 2026-11-20T01:00:00Z
updatedDate: 2026-11-26T03:00:00Z
blocks: []"""
    issues = validate_document(tmp_path / "articles/a.md", __import__("yaml").safe_load(source), "article")
    assert any("featuredImage" in issue.message for issue in issues)

def test_intro_rejects_multiple_paragraphs_and_markdown(tmp_path: Path):
    source = PAGE.replace(
        "intro: PT Contoh menyediakan layanan profesional untuk kebutuhan pelanggan.",
        "intro: |\n  PT **Contoh** menyediakan layanan profesional.\n\n  Paragraf kedua."
    ).replace("description: Profil perusahaan.", "description: '**Profil** perusahaan.'")
    issues = validate_document(tmp_path / "pages/page.md", __import__("yaml").safe_load(source), "page")
    assert any("exactly one paragraph" in issue.message for issue in issues)
    assert any("plain text" in issue.message for issue in issues)

def test_defined_term_must_be_page_level_and_follow_title_is_definition(tmp_path: Path):
    good = PAGE.replace("type: WebPage", "type: WebPage\n  mainEntity:\n    type: DefinedTerm").replace(
        "PT Contoh menyediakan layanan profesional untuk kebutuhan pelanggan.",
        "Tentang Kami adalah penjelasan mengenai identitas, tujuan, dan ruang lingkup organisasi."
    )
    assert validate_document(tmp_path / "pages/glossary.md", __import__("yaml").safe_load(good), "page") == []
    bad = good.replace("Tentang Kami adalah", "Halaman ini membahas")
    issues = validate_document(tmp_path / "pages/glossary.md", __import__("yaml").safe_load(bad), "page")
    assert any("DefinedTerm intro must begin" in issue.message for issue in issues)

def test_defined_term_not_allowed_for_article(tmp_path: Path):
    source = """id: 5
slug: article
title: Istilah
description: Ringkasan
intro: Istilah adalah konsep yang dijelaskan.
schema:
  type: Article
  mainEntity:
    type: DefinedTerm
seo:
  title: Istilah
  description: Ringkasan
featuredImage:
  src: /a.webp
  alt: Ilustrasi istilah.
publishedDate: 2026-11-20T01:00:00Z
updatedDate: 2026-11-26T03:00:00Z
blocks: []"""
    issues = validate_document(tmp_path / "articles/a.md", __import__("yaml").safe_load(source), "article")
    assert any("only allowed for Page" in issue.message for issue in issues)

def test_service_relation_fields_must_be_positive_and_unique(tmp_path: Path):
    source = """id: 7
slug: service
title: Layanan
description: Ringkasan
intro: Layanan ini menjelaskan pendampingan teknis.
schema:
  type: Service
seo:
  title: Layanan
  description: Ringkasan
categoryIds: [2, 2]
relatedServiceIds: [0]
updatedDate: 2026-11-26T03:00:00Z
blocks: []"""
    issues = validate_document(tmp_path / "services/s.md", __import__("yaml").safe_load(source), "service")
    assert any("duplicate IDs" in issue.message for issue in issues)
    assert any("array of positive integers" in issue.message for issue in issues)

def test_unknown_collection_requires_explicit_mapping(tmp_path: Path):
    file = write_md(tmp_path / "content/document.md", PAGE)
    issues = validate_paths([file])
    assert any("cannot infer document contract" in issue.message for issue in issues)

def test_category_archive_contract_requires_metadata_and_blocks(tmp_path: Path):
    source = """id: 30
slug: panduan
title: Panduan
description: Kumpulan artikel panduan.
schema:
  type: CollectionPage
seo:
  title: Panduan
  description: Kumpulan panduan.
blocks:
  - id: 1
    component: content-list
updatedDate: 2026-11-26T03:00:00Z"""
    assert validate_document(tmp_path / "categories/panduan.md", __import__("yaml").safe_load(source), "category") == []

def test_explicit_collection_mapping_supports_project_specific_directory_names(tmp_path: Path):
    file = write_md(tmp_path / "content/static/a.md", PAGE)
    issues = validate_paths([file], {str((tmp_path / "content/static").resolve()): "page"})
    assert issues == []


def test_foreign_keys_resolve_to_existing_documents_of_expected_kind(tmp_path: Path):
    page = write_md(tmp_path / "pages/page.md", PAGE)
    article = write_md(tmp_path / "articles/article.md", """id: 2
slug: article
title: Artikel
description: Ringkasan
intro: Intro substantif.
schema:
  type: Article
seo: {}
categoryIds: [3]
relatedArticleIds: [4]
relatedServiceId: 5
featuredImage:
  src: /a.webp
  alt: Foto dokumen.
publishedDate: 2026-11-20T01:00:00Z
updatedDate: 2026-11-26T03:00:00Z
blocks: []""")
    category = write_md(tmp_path / "categories/category.md", """id: 3
slug: kategori
title: Kategori
description: Ringkasan kategori.
schema:
  type: CollectionPage
seo: {}
blocks: []
updatedDate: 2026-11-26T03:00:00Z""")
    related = write_md(tmp_path / "articles/related.md", """id: 4
slug: related
title: Artikel terkait
description: Ringkasan
intro: Intro substantif.
schema:
  type: Article
seo: {}
featuredImage:
  src: /b.webp
  alt: Foto dokumen.
publishedDate: 2026-11-20T01:00:00Z
updatedDate: 2026-11-26T03:00:00Z
blocks: []""")
    service = write_md(tmp_path / "services/service.md", """id: 5
slug: service
title: Layanan
description: Ringkasan
intro: Intro layanan substantif.
schema:
  type: Service
seo: {}
updatedDate: 2026-11-26T03:00:00Z
blocks: []""")
    assert validate_paths([page, article, category, related, service]) == []


def test_foreign_key_missing_target_fails(tmp_path: Path):
    article = write_md(tmp_path / "articles/article.md", """id: 2
slug: article
title: Artikel
description: Ringkasan
intro: Intro substantif.
schema:
  type: Article
seo: {}
relatedServiceId: 999
featuredImage:
  src: /a.webp
  alt: Foto dokumen.
publishedDate: 2026-11-20T01:00:00Z
updatedDate: 2026-11-26T03:00:00Z
blocks: []""")
    issues = validate_paths([article])
    assert any("missing relatedServiceId target ID 999" in issue.message for issue in issues)


def test_foreign_key_wrong_target_kind_fails(tmp_path: Path):
    page = write_md(tmp_path / "pages/page.md", PAGE)
    article = write_md(tmp_path / "articles/article.md", """id: 2
slug: article
title: Artikel
description: Ringkasan
intro: Intro substantif.
schema:
  type: Article
seo: {}
relatedServiceId: 1
featuredImage:
  src: /a.webp
  alt: Foto dokumen.
publishedDate: 2026-11-20T01:00:00Z
updatedDate: 2026-11-26T03:00:00Z
blocks: []""")
    issues = validate_paths([page, article])
    assert any("expected service" in issue.message for issue in issues)


def test_nested_menu_page_ids_are_resolved(tmp_path: Path):
    page = write_md(tmp_path / "pages/page.md", PAGE)
    menu = write_md(tmp_path / "menus/menu.md", """id: 2
slug: nav
title: Navigasi
schema:
  type: SiteNavigationElement
location: header
items:
  - label: Parent
    url: https://example.com
    children:
      - label: Child
        pageId: 999
updatedDate: 2026-11-26T03:00:00Z""")
    issues = validate_paths([page, menu])
    assert any("items[0].children[0].pageId references missing pageId target ID 999" in issue.message for issue in issues)


def test_menu_target_accepts_homepage_and_page_only(tmp_path: Path):
    homepage = write_md(tmp_path / "homepages/home.md", """id: 1
slug: home
title: Beranda
description: Ringkasan.
schema:
  type: WebPage
seo: {}
blocks: []
updatedDate: 2026-11-26T03:00:00Z""")
    menu = write_md(tmp_path / "menus/menu.md", """id: 2
slug: nav
title: Navigasi
schema:
  type: SiteNavigationElement
location: header
items:
  - label: Beranda
    pageId: 1
updatedDate: 2026-11-26T03:00:00Z""")
    assert validate_paths([homepage, menu]) == []


def test_block_level_foreign_keys_are_resolved(tmp_path: Path):
    homepage = write_md(tmp_path / "homepages/home.md", """id: 1
slug: home
title: Beranda
description: Ringkasan.
schema:
  type: WebPage
seo: {}
blocks:
  - id: 1
    component: service-grid
    serviceIds: [999]
updatedDate: 2026-11-26T03:00:00Z""")
    issues = validate_paths([homepage])
    assert any("blocks[0].serviceIds references missing serviceIds target ID 999" in issue.message for issue in issues)


def test_content_list_category_id_is_resolved(tmp_path: Path):
    page = write_md(tmp_path / "pages/page.md", PAGE.replace(
        "component: rich-text", "component: content-list\n    categoryId: 999"
    ))
    issues = validate_paths([page])
    assert any("blocks[0].categoryId references missing categoryId target ID 999" in issue.message for issue in issues)


@pytest.mark.parametrize(("kind", "field", "message"), [
    ("article", "authorId", "Author/Person target contract"),
    ("service", "providerId", "Organization/Provider target contract"),
])
def test_unsupported_entity_relations_are_rejected_when_populated(tmp_path: Path, kind: str, field: str, message: str):
    if kind == "article":
        source = """id: 2
slug: article
title: Artikel
description: Ringkasan
intro: Intro substantif.
schema:
  type: Article
seo: {}
authorId: 1
featuredImage:
  src: /a.webp
  alt: Foto dokumen.
publishedDate: 2026-11-20T01:00:00Z
updatedDate: 2026-11-26T03:00:00Z
blocks: []"""
        path = write_md(tmp_path / "articles/article.md", source)
    else:
        source = """id: 2
slug: service
title: Layanan
description: Ringkasan
intro: Intro layanan.
schema:
  type: Service
seo: {}
providerId: 1
updatedDate: 2026-11-26T03:00:00Z
blocks: []"""
        path = write_md(tmp_path / "services/service.md", source)
    issues = validate_paths([path])
    assert any(message in issue.message for issue in issues)


def test_parent_page_cycle_is_rejected(tmp_path: Path):
    first = write_md(tmp_path / "pages/one.md", PAGE.replace("id: 1", "id: 1") + "\nparentPageId: 2")
    second = write_md(tmp_path / "pages/two.md", PAGE.replace("id: 1", "id: 2") + "\nparentPageId: 1")
    issues = validate_paths([first, second])
    assert any("parentPageId hierarchy contains a cycle" in issue.message for issue in issues)


def test_self_referential_related_content_is_rejected(tmp_path: Path):
    article = write_md(tmp_path / "articles/article.md", """id: 2
slug: article
title: Artikel
description: Ringkasan
intro: Intro substantif.
schema:
  type: Article
seo: {}
relatedArticleIds: [2]
featuredImage:
  src: /a.webp
  alt: Foto dokumen.
publishedDate: 2026-11-20T01:00:00Z
updatedDate: 2026-11-26T03:00:00Z
blocks: []""")
    issues = validate_paths([article])
    assert any("cannot reference the source Article itself" in issue.message for issue in issues)


def test_block_relation_cardinality_and_duplicates_are_validated(tmp_path: Path):
    malformed = write_md(tmp_path / "homepages/malformed.md", """id: 1
slug: home
title: Beranda
description: Ringkasan.
schema:
  type: WebPage
seo: {}
blocks:
  - id: 1
    component: service-grid
    serviceIds: 5
updatedDate: 2026-11-26T03:00:00Z""")
    duplicated = write_md(tmp_path / "homepages/duplicated.md", """id: 2
slug: home-2
title: Beranda Dua
description: Ringkasan.
schema:
  type: WebPage
seo: {}
blocks:
  - id: 1
    component: service-grid
    serviceIds: [5, 5]
updatedDate: 2026-11-26T03:00:00Z""")
    issues = validate_paths([malformed, duplicated])
    assert any("serviceIds must be an array of positive integers" in issue.message for issue in issues)
    assert any("serviceIds must not contain duplicate IDs" in issue.message for issue in issues)

def test_schema_registry_rejects_unknown_page_type(tmp_path: Path):
    issues = validate_document(tmp_path / "pages/a.md", __import__("yaml").safe_load(PAGE.replace("WebPage", "MadeUpPage")), "page")
    assert any("not an allowed page-level Schema.org type" in issue.message for issue in issues)


def test_schema_registry_rejects_entity_type_as_page_type(tmp_path: Path):
    issues = validate_document(tmp_path / "pages/a.md", __import__("yaml").safe_load(PAGE.replace("WebPage", "Organization")), "page")
    assert any("not an allowed page-level Schema.org type" in issue.message for issue in issues)


def test_schema_registry_allows_defined_term_only_as_page_main_entity(tmp_path: Path):
    good = PAGE.replace("WebPage", "WebPage").replace(
        "PT Contoh menyediakan layanan profesional untuk kebutuhan pelanggan.",
        "Tentang Kami adalah penjelasan mengenai identitas organisasi."
    ).replace("type: WebPage", "type: WebPage\n  mainEntity:\n    type: DefinedTerm")
    assert validate_document(tmp_path / "pages/glossary.md", __import__("yaml").safe_load(good), "page") == []


def test_schema_registry_rejects_unknown_schema_properties(tmp_path: Path):
    source = PAGE.replace("type: WebPage", "type: WebPage\n  name: Tidak boleh")
    issues = validate_document(tmp_path / "pages/a.md", __import__("yaml").safe_load(source), "page")
    assert any("schema has unsupported property 'name'" in issue.message for issue in issues)


def test_block_registry_rejects_unknown_component(tmp_path: Path):
    source = PAGE.replace("component: rich-text", "component: imaginary-block")
    issues = validate_document(tmp_path / "pages/a.md", __import__("yaml").safe_load(source), "page")
    assert any("unknown block component 'imaginary-block'" in issue.message for issue in issues)


def test_block_registry_rejects_unknown_props(tmp_path: Path):
    source = PAGE.replace("component: rich-text", "component: rich-text\n    inventedProp: true")
    issues = validate_document(tmp_path / "pages/a.md", __import__("yaml").safe_load(source), "page")
    assert any("unsupported prop 'inventedProp'" in issue.message for issue in issues)


def test_block_registry_validates_component_specific_props(tmp_path: Path):
    source = PAGE.replace("component: rich-text", "component: faq\n    content: Tidak diizinkan")
    issues = validate_document(tmp_path / "pages/a.md", __import__("yaml").safe_load(source), "page")
    assert any("does not allow prop 'content'" in issue.message for issue in issues)


def test_block_registry_validates_prop_types(tmp_path: Path):
    source = PAGE.replace("component: rich-text", "component: service-grid\n    serviceIds: 12")
    issues = validate_document(tmp_path / "pages/a.md", __import__("yaml").safe_load(source), "page")
    assert any("prop 'serviceIds' must be intlist" in issue.message for issue in issues)


def test_block_schema_must_be_allowed_for_component(tmp_path: Path):
    source = PAGE.replace("component: rich-text", "component: faq\n    schema:\n      type: HowTo")
    issues = validate_document(tmp_path / "pages/a.md", __import__("yaml").safe_load(source), "page")
    assert any("not permitted for component 'faq'" in issue.message for issue in issues)


def test_block_schema_registry_accepts_faq_page(tmp_path: Path):
    source = PAGE.replace("component: rich-text", "component: faq\n    schema:\n      type: FAQPage\n    items:\n      - question: Apa ini?\n        answer: Penjelasan.")
    assert validate_document(tmp_path / "pages/a.md", __import__("yaml").safe_load(source), "page") == []


def test_block_registry_rejects_boolean_as_numeric_prop(tmp_path: Path):
    source = PAGE.replace("component: rich-text", "component: service-grid\n    serviceIds: [true]")
    issues = validate_document(tmp_path / "pages/a.md", __import__("yaml").safe_load(source), "page")
    assert any("prop 'serviceIds' must be intlist" in issue.message for issue in issues)


def test_route_validation_detects_invalid_slug_and_collision(tmp_path: Path):
    from validate_content import validate_routes
    first = write_md(tmp_path / "pages/one.md", PAGE.replace("slug: tentang", "slug: same"))
    second = write_md(tmp_path / "pages/two.md", PAGE.replace("slug: tentang", "slug: same").replace("id: 1", "id: 2"))
    docs = [(first, {"slug":"same"}, "page"), (second, {"slug":"same"}, "article")]
    issues, routes = validate_routes(docs, {"article":"/"})
    assert any("ROUTE_COLLISION" in issue.message for issue in issues)


def test_route_validation_rejects_noncanonical_slug(tmp_path: Path):
    from validate_content import validate_routes
    path = tmp_path / "pages/a.md"
    issues, _ = validate_routes([(path, {"slug":"Upper Case"}, "page")])
    assert any("INVALID_SLUG" in issue.message for issue in issues)


def test_asset_validation_detects_missing_local_image(tmp_path: Path):
    from validate_content import validate_assets_and_links
    root = tmp_path / "site"
    root.mkdir()
    path = write_md(tmp_path / "pages/page.md", PAGE)
    data = {"featuredImage":{"src":"/images/not-found.webp","alt":"Gambar"}}
    issues = validate_assets_and_links([(path,data,"page")], root, {"/tentang/":path})
    assert any("ASSET_NOT_FOUND" in issue.message for issue in issues)


def test_asset_validation_ignores_external_media(tmp_path: Path):
    from validate_content import validate_assets_and_links
    root = tmp_path / "site"
    root.mkdir()
    path = write_md(tmp_path / "pages/page.md", PAGE)
    data = {"featuredImage":{"src":"https://cdn.example.test/a.webp","alt":"Gambar"}}
    assert validate_assets_and_links([(path,data,"page")], root, {}) == []


def test_internal_link_validation_detects_unknown_route(tmp_path: Path):
    from validate_content import validate_assets_and_links
    root = tmp_path / "site"
    root.mkdir()
    path = write_md(tmp_path / "pages/page.md", PAGE)
    data = {"blocks":[{"component":"cta","url":"/missing/"}]}
    issues = validate_assets_and_links([(path,data,"page")], root, {"/tentang/":path})
    assert any("INTERNAL_LINK_NOT_FOUND" in issue.message for issue in issues)


def test_route_manifest_requires_routes_array(tmp_path: Path):
    from validate_content import validate_route_manifest
    manifest = tmp_path / "routes.yml"
    manifest.write_text("notRoutes: []", encoding="utf-8")
    issues = validate_route_manifest(manifest,tmp_path,{})
    assert any("INVALID_MANIFEST" in issue.message for issue in issues)


def test_route_manifest_checks_generated_routes_and_sitemap(tmp_path: Path):
    from validate_content import validate_route_manifest
    manifest = tmp_path / "routes.yml"
    manifest.write_text("routes:\n  - path: /tentang/\n    indexable: true\nsitemap: public/sitemap.xml\n",encoding="utf-8")
    (tmp_path/"public").mkdir()
    (tmp_path/"public/sitemap.xml").write_text("<urlset></urlset>",encoding="utf-8")
    issues = validate_route_manifest(manifest,tmp_path,{"/tentang/":tmp_path/"pages/page.md"})
    assert any("SITEMAP_ROUTE_MISSING" in issue.message for issue in issues)


def test_duplicate_canonical_urls_are_rejected(tmp_path: Path):
    from validate_content import validate_seo_uniqueness
    docs = [
        (tmp_path/"pages/one.md", {"seo":{"canonical":"https://example.test/about/"}}, "page"),
        (tmp_path/"articles/two.md", {"seo":{"canonical":"https://example.test/about"}}, "article"),
    ]
    issues = validate_seo_uniqueness(docs)
    assert any("DUPLICATE_CANONICAL" in issue.message for issue in issues)


def test_unique_canonical_urls_are_accepted(tmp_path: Path):
    from validate_content import validate_seo_uniqueness
    docs = [
        (tmp_path/"pages/one.md", {"seo":{"canonical":"https://example.test/about/"}}, "page"),
        (tmp_path/"articles/two.md", {"seo":{"canonical":"https://example.test/news/"}}, "article"),
    ]
    assert validate_seo_uniqueness(docs) == []


def test_cli_help_smoke():
    import subprocess
    result = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parents[1] / "scripts" / "validate_content.py"), "--help"],
        text=True, capture_output=True,
    )
    assert result.returncode == 0
    assert "--site-root" in result.stdout
    assert "--route-manifest" in result.stdout


def test_cli_runs_route_and_canonical_checks(tmp_path: Path):
    import subprocess
    content = tmp_path / "content"
    page1 = write_md(content / "pages" / "one.md", PAGE.replace("canonical", "canonical"))
    page2_source = PAGE.replace("id: 1", "id: 2").replace("slug: tentang", "slug: about")
    page2_source = page2_source.replace("  type: WebPage", "  type: WebPage")
    page2 = write_md(content / "pages" / "two.md", page2_source)
    # Add duplicate canonical metadata to both documents.
    for file in (page1, page2):
        source = file.read_text(encoding="utf-8")
        source = source.replace("  description: Profil perusahaan.\nblocks:", "  description: Profil perusahaan.\n  canonical: https://example.test/shared/\nblocks:")
        file.write_text(source, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parents[1] / "scripts" / "validate_content.py"), str(content)],
        text=True, capture_output=True,
    )
    assert result.returncode == 1
    assert "DUPLICATE_CANONICAL" in result.stdout


def test_cli_fails_when_internal_link_is_missing(tmp_path: Path):
    import subprocess
    content = tmp_path / "content"
    page = write_md(content / "pages" / "page.md", PAGE.replace(
        "component: rich-text", "component: cta\n    url: /missing/"
    ))
    site_root = tmp_path / "site"
    site_root.mkdir()
    result = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parents[1] / "scripts" / "validate_content.py"),
         str(content), "--site-root", str(site_root)],
        text=True, capture_output=True,
    )
    assert result.returncode == 1
    assert "INTERNAL_LINK_NOT_FOUND" in result.stdout


def test_cli_passes_with_route_manifest_and_sitemap(tmp_path: Path):
    import subprocess
    content = tmp_path / "content"
    write_md(content / "pages" / "page.md", PAGE)
    site_root = tmp_path / "site"
    (site_root / "public").mkdir(parents=True)
    (site_root / "public" / "sitemap.xml").write_text(
        "<urlset><loc>https://example.test/tentang/</loc></urlset>", encoding="utf-8"
    )
    (site_root / "routes.yml").write_text(
        "routes:\n  - path: /tentang/\n    source: public/sitemap.xml\n    indexable: true\nsitemap: public/sitemap.xml\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parents[1] / "scripts" / "validate_content.py"),
         str(content), "--site-root", str(site_root), "--route-manifest", str(site_root / "routes.yml")],
        text=True, capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "route manifest/sitemap/redirects" in result.stdout


def test_extension_contract_validates_training_schedule_and_foreign_keys(tmp_path: Path):
    from validate_content import load_extension_contracts
    content = tmp_path / "content"
    training = write_md(content / "trainings" / "course.md", """id: 101
slug: kursus-astro
title: Kursus Astro
description: Pelatihan contoh.
schema:
  type: Course
updatedDate: 2026-11-26T03:00:00Z
scheduleIds: [201]""")
    schedule = write_md(content / "schedules" / "batch.md", """id: 201
slug: batch-november
title: Batch November
schema:
  type: Event
updatedDate: 2026-11-26T03:00:00Z
startDate: 2026-11-29
endDate: 2026-11-30""")
    registry = tmp_path / "contracts.yml"
    registry.write_text("""version: 1
collections:
  training:
    directory: trainings
    requiredFields: [id, slug, title, schema, updatedDate]
    fieldTypes:
      id: positive_int
      slug: string
      title: string
      description: string
      schema: object
      updatedDate: utc_datetime
      startDate: iso_date_or_datetime
      endDate: iso_date_or_datetime
      scheduleIds: positive_int_array
    schemaTypes: [Course]
    schemaMappings:
      Course:
        fieldMapping:
          name: title
          description: description
        requiredFields: [title, description]
    routePrefix: /training/
    relations:
      scheduleIds:
        target: schedule
        cardinality: many
  schedule:
    directory: schedules
    requiredFields: [id, slug, title, schema, updatedDate, startDate, endDate]
    fieldTypes:
      id: positive_int
      slug: string
      title: string
      description: string
      schema: object
      updatedDate: utc_datetime
      startDate: iso_date_or_datetime
      endDate: iso_date_or_datetime
    schemaTypes: [Event]
    schemaMappings:
      Event:
        fieldMapping:
          name: title
          startDate: startDate
          endDate: endDate
        requiredFields: [title, startDate, endDate]
    routePrefix: /schedule/
""", encoding="utf-8")
    contracts, mapping = load_extension_contracts(registry, content)
    issues = validate_paths([training, schedule], mapping, contracts)
    assert issues == []


def test_extension_contract_rejects_missing_relation_target(tmp_path: Path):
    from validate_content import load_extension_contracts
    content = tmp_path / "content"
    training = write_md(content / "trainings" / "course.md", """id: 101
slug: kursus-astro
title: Kursus Astro
description: Pelatihan contoh.
schema:
  type: Course
updatedDate: 2026-11-26T03:00:00Z
scheduleIds: [999]""")
    registry = tmp_path / "contracts.yml"
    registry.write_text("""version: 1
collections:
  training:
    directory: trainings
    requiredFields: [id, slug, title, schema, updatedDate]
    fieldTypes:
      id: positive_int
      slug: string
      title: string
      description: string
      schema: object
      updatedDate: utc_datetime
      startDate: iso_date_or_datetime
      endDate: iso_date_or_datetime
      scheduleIds: positive_int_array
    schemaTypes: [Course]
    schemaMappings:
      Course:
        fieldMapping:
          name: title
          description: description
        requiredFields: [title, description]
    routePrefix: /training/
    relations:
      scheduleIds:
        target: schedule
        cardinality: many
  schedule:
    directory: schedules
    requiredFields: [id, slug, title, schema, updatedDate]
    fieldTypes:
      id: positive_int
      slug: string
      title: string
      description: string
      schema: object
      updatedDate: utc_datetime
      startDate: iso_date_or_datetime
      endDate: iso_date_or_datetime
    schemaTypes: [Event]
    schemaMappings:
      Event:
        fieldMapping:
          name: title
          startDate: startDate
          endDate: endDate
        requiredFields: [title, startDate, endDate]
    routePrefix: /schedule/
""", encoding="utf-8")
    contracts, mapping = load_extension_contracts(registry, content)
    issues = validate_paths([training], mapping, contracts)
    assert any("references missing schedule ID 999" in issue.message for issue in issues)


def test_schema_registry_explicitly_accounts_for_every_page_type():
    from registries import PAGE_TYPES, SCHEMA_REGISTRY, SCHEMA_DECLARATION_ONLY, SCHEMA_TYPE_STATUS, SCHEMA_TYPES, SCHEMA_SCOPE_STATUS, SCHEMA_DECLARATION_ONLY_BY_SCOPE
    mapped = {name for name, entry in SCHEMA_REGISTRY.items() if entry.get("scope") == "page"}
    assert PAGE_TYPES == mapped | SCHEMA_DECLARATION_ONLY
    assert set(SCHEMA_TYPE_STATUS) == PAGE_TYPES
    assert all(SCHEMA_TYPE_STATUS[name] == "declaration-only" for name in SCHEMA_DECLARATION_ONLY)
    for scope, types in SCHEMA_TYPES.items():
        mapped_types = {name for name, entry in SCHEMA_REGISTRY.items() if entry.get("scope") == scope}
        assert set(SCHEMA_SCOPE_STATUS[scope]) == types
        assert types == mapped_types | SCHEMA_DECLARATION_ONLY_BY_SCOPE[scope]


def test_cli_loads_project_extension_registry(tmp_path: Path):
    import subprocess
    content = tmp_path / "content"
    write_md(content / "trainings" / "course.md", """id: 101
slug: kursus-astro
title: Kursus Astro
description: Pelatihan contoh.
schema:
  type: Course
updatedDate: 2026-11-26T03:00:00Z""")
    write_md(content / "schedules" / "batch.md", """id: 201
slug: batch-november
title: Batch November
startDate: 2026-11-29
endDate: 2026-11-30
schema:
  type: Event
updatedDate: 2026-11-26T03:00:00Z""")
    registry = tmp_path / "contracts.yml"
    registry.write_text("""version: 1
collections:
  training:
    directory: trainings
    requiredFields: [id, slug, title, schema, updatedDate]
    fieldTypes:
      id: positive_int
      slug: string
      title: string
      description: string
      schema: object
      updatedDate: utc_datetime
      startDate: iso_date_or_datetime
      endDate: iso_date_or_datetime
    schemaTypes: [Course]
    schemaMappings:
      Course:
        fieldMapping:
          name: title
          description: description
        requiredFields: [title, description]
    routePrefix: /training/
  schedule:
    directory: schedules
    requiredFields: [id, slug, title, schema, updatedDate]
    fieldTypes:
      id: positive_int
      slug: string
      title: string
      description: string
      schema: object
      updatedDate: utc_datetime
      startDate: iso_date_or_datetime
      endDate: iso_date_or_datetime
    schemaTypes: [Event]
    schemaMappings:
      Event:
        fieldMapping:
          name: title
          startDate: startDate
          endDate: endDate
        requiredFields: [title, startDate, endDate]
    routePrefix: /schedule/
""", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parents[1] / "scripts" / "validate_content.py"),
         str(content), "--contract-registry", str(registry)],
        text=True, capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "slug/routes" in result.stdout


def test_schema_registry_rejects_declaration_only_page_type(tmp_path: Path):
    source = PAGE.replace("type: WebPage", "type: AboutPage")
    issues = validate_document(tmp_path / "pages/a.md", __import__("yaml").safe_load(source), "page")
    assert any("declaration-only" in issue.message for issue in issues)


def test_cli_uses_route_prefix_override(tmp_path: Path):
    import json
    import subprocess
    content = tmp_path / "content"
    write_md(content / "pages" / "page.md", PAGE)
    site_root = tmp_path / "site"
    (site_root / "public").mkdir(parents=True)
    (site_root / "public" / "sitemap.xml").write_text(
        "<urlset><loc>https://example.test/custom/tentang/</loc></urlset>", encoding="utf-8"
    )
    prefixes = tmp_path / "prefixes.json"
    prefixes.write_text(json.dumps({"page": "/custom/"}), encoding="utf-8")
    manifest = site_root / "routes.yml"
    manifest.write_text(
        "routes:\n  - path: /custom/tentang/\n    source: public/sitemap.xml\n    indexable: true\nsitemap: public/sitemap.xml\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parents[1] / "scripts" / "validate_content.py"),
         str(content), "--site-root", str(site_root), "--route-prefixes", str(prefixes),
         "--route-manifest", str(manifest)],
        text=True, capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_extension_supports_static_schema_type_natural_key_and_offset_dates(tmp_path: Path):
    from validate_content import load_extension_contracts
    content = tmp_path / "content"
    training = write_md(content / "trainings" / "astro.md", """id: 301
ulid: 01ARZ3NDEKTSV4RRFFQ69G5FAV
type: training
trainingSlug: astro-course
slug: astro-course
title: Astro Course
description: Training Astro.
pubDate: '2026-11-26T10:00:00+07:00'
updatedDate: '2026-11-27T10:00:00+07:00'""")
    schedule = write_md(content / "schedules" / "batch.md", """id: 401
ulid: 01ARZ3NDEKTSV4RRFFQ69G5FAW
type: schedule
scheduleId: batch-001
publisherId: publisher-01
trainingSlug: astro-course
batchNo: '001'
slug: astro-course-batch-001
title: Batch 001
description: Schedule Astro.
startDate: 2026-12-01
endDate: 2026-12-03
dateLabel: 1-3 Desember 2026
timezone: Asia/Jakarta
pubDate: '2026-11-26T10:00:00+07:00'
updatedDate: '2026-11-27T10:00:00+07:00'
status: scheduled""")
    registry = tmp_path / "contracts.yml"
    registry.write_text("""version: 1
collections:
  training:
    directory: trainings
    requiredFields: [id, ulid, type, trainingSlug, slug, title, description, pubDate, updatedDate]
    fieldTypes:
      id: positive_int
      ulid: ulid
      type: string
      trainingSlug: string
      slug: string
      title: string
      description: string
      pubDate: offset_datetime
      updatedDate: offset_datetime
    fieldEnums:
      type: [training]
    schemaTypes: [Course]
    schemaType: Course
    schemaMappings:
      Course:
        fieldMapping:
          name: title
          description: description
        requiredFields: [title, description]
    routePrefix: /training/
  schedule:
    directory: schedules
    requiredFields: [id, ulid, type, scheduleId, publisherId, trainingSlug, batchNo, slug, title, description, startDate, endDate, dateLabel, timezone, pubDate, updatedDate, status]
    fieldTypes:
      id: positive_int
      ulid: ulid
      type: string
      scheduleId: string
      publisherId: string
      trainingSlug: string
      batchNo: string
      slug: string
      title: string
      description: string
      startDate: iso_date_or_datetime
      endDate: iso_date_or_datetime
      dateLabel: string
      timezone: string
      pubDate: offset_datetime
      updatedDate: offset_datetime
      status: string
    fieldEnums:
      type: [schedule]
      status: [scheduled, ongoing, completed, postponed, cancelled]
    schemaTypes: [Event]
    schemaType: Event
    schemaMappings:
      Event:
        fieldMapping:
          name: title
          startDate: startDate
          endDate: endDate
        requiredFields: [title, startDate, endDate]
    routePrefix: /schedule/
    relations:
      trainingSlug:
        target: training
        targetField: trainingSlug
        cardinality: one
""", encoding="utf-8")
    contracts, mapping = load_extension_contracts(registry, content)
    assert validate_paths([training, schedule], mapping, contracts) == []


def test_extension_field_enum_rejects_unknown_value(tmp_path: Path):
    from validate_content import load_extension_contracts
    content = tmp_path / "content"
    item = write_md(content / "schedules" / "batch.md", """id: 401
ulid: 01ARZ3NDEKTSV4RRFFQ69G5FAW
type: schedule
scheduleId: batch-001
publisherId: publisher-01
trainingSlug: astro-course
batchNo: '001'
slug: astro-course-batch-001
title: Batch 001
description: Schedule Astro.
startDate: 2026-12-01
endDate: 2026-12-03
dateLabel: 1-3 Desember 2026
timezone: Asia/Jakarta
pubDate: '2026-11-26T10:00:00+07:00'
updatedDate: '2026-11-27T10:00:00+07:00'
status: invalid""")
    registry = Path(__file__).resolve().parents[1] / "examples" / "content-contracts" / "training-schedule.yml"
    contracts, mapping = load_extension_contracts(registry, content)
    issues = validate_paths([item], mapping, contracts)
    assert any("field 'status' must be one of" in issue.message for issue in issues)


def test_block_schema_rejects_declaration_only_type(tmp_path: Path):
    source = PAGE.replace("component: rich-text", "component: faq\n    schema:\n      type: Quiz")
    issues = validate_document(tmp_path / "pages/a.md", __import__("yaml").safe_load(source), "page")
    assert any("declaration-only" in issue.message for issue in issues)


def test_block_schema_registry_maps_table_and_image_object(tmp_path: Path):
    table = PAGE.replace("component: rich-text", "component: table\n    schema:\n      type: Table\n    headers: [A]\n    rows: [[B]]")
    image = PAGE.replace("component: rich-text", "component: image\n    schema:\n      type: ImageObject\n    src: /a.webp\n    alt: Gambar.")
    assert validate_document(tmp_path / "pages/table.md", __import__("yaml").safe_load(table), "page") == []
    assert validate_document(tmp_path / "pages/image.md", __import__("yaml").safe_load(image), "page") == []


def test_extension_accepts_yaml_native_offset_datetime_and_date_values(tmp_path: Path):
    from validate_content import load_extension_contracts
    content = tmp_path / "content"
    training = write_md(content / "trainings" / "astro.md", """id: 501
slug: astro-course
title: Astro Course
description: Training Astro.
pubDate: 2026-11-26T10:00:00+07:00
updatedDate: 2026-11-27T10:00:00+07:00
schema:
  type: Course""")
    schedule = write_md(content / "schedules" / "batch.md", """id: 601
slug: astro-batch
title: Astro Batch
startDate: 2026-12-01
endDate: 2026-12-03
pubDate: 2026-11-26T10:00:00+07:00
updatedDate: 2026-11-27T10:00:00+07:00
schema:
  type: Event""")
    registry = tmp_path / "contracts.yml"
    registry.write_text("""version: 1
collections:
  training:
    directory: trainings
    requiredFields: [id, slug, title, description, pubDate, updatedDate, schema]
    fieldTypes:
      id: positive_int
      slug: string
      title: string
      description: string
      pubDate: offset_datetime
      updatedDate: offset_datetime
      schema: object
    schemaTypes: [Course]
    schemaMappings:
      Course:
        fieldMapping:
          name: title
          description: description
        requiredFields: [title, description]
    routePrefix: /training/
  schedule:
    directory: schedules
    requiredFields: [id, slug, title, startDate, endDate, pubDate, updatedDate, schema]
    fieldTypes:
      id: positive_int
      slug: string
      title: string
      startDate: iso_date_or_datetime
      endDate: iso_date_or_datetime
      pubDate: offset_datetime
      updatedDate: offset_datetime
      schema: object
    schemaTypes: [Event]
    schemaMappings:
      Event:
        fieldMapping:
          name: title
          startDate: startDate
          endDate: endDate
        requiredFields: [title, startDate, endDate]
    routePrefix: /schedule/
""", encoding="utf-8")
    contracts, mapping = load_extension_contracts(registry, content)
    assert validate_paths([training, schedule], mapping, contracts) == []


@pytest.mark.parametrize("registry_text, expected", [
    ("""version: 1
collections:
  training:
    directory: trainings
    requiredFields: [id, title]
    fieldTypes:
      id: positive_int
      title: string
    fieldEnums:
      missingField: [one, two]
    schemaTypes: [Course]
    schemaMappings:
      Course:
        fieldMapping:
          name: title
        requiredFields: [title]
    routePrefix: /training/
""", "fieldEnums"),
    ("""version: 1
collections:
  training:
    directory: trainings
    requiredFields: [id, title]
    fieldTypes:
      id: positive_int
      title: string
    schemaTypes: [Course]
    schemaMappings:
      Course:
        fieldMapping:
          name: undeclaredTitle
        requiredFields: [title]
    routePrefix: /training/
""", "fieldMapping sources"),
    ("""version: 1
collections:
  training:
    directory: trainings
    requiredFields: [id, title]
    fieldTypes:
      id: positive_int
      title: string
    schemaTypes: [Course]
    schemaMappings:
      Course:
        fieldMapping:
          name: title
        requiredFields: [title]
    routePrefix: /training?draft=1/
""", "routePrefix"),
])
def test_extension_registry_rejects_inconsistent_contracts(tmp_path: Path, registry_text: str, expected: str):
    from validate_content import load_extension_contracts
    content = tmp_path / "content"
    content.mkdir()
    registry = tmp_path / "contracts.yml"
    registry.write_text(registry_text, encoding="utf-8")
    with pytest.raises(ValueError, match=expected):
        load_extension_contracts(registry, content)


def test_route_manifest_missing_sitemap_reports_error_without_crashing(tmp_path: Path):
    from validate_content import validate_route_manifest
    manifest = tmp_path / "routes.yml"
    manifest.write_text("routes: []\nsitemap: public/missing.xml\n", encoding="utf-8")
    issues = validate_route_manifest(manifest, tmp_path, {})
    assert any("SITEMAP_NOT_FOUND" in issue.message for issue in issues)


def test_route_manifest_rejects_source_path_escape(tmp_path: Path):
    from validate_content import validate_route_manifest
    manifest = tmp_path / "routes.yml"
    manifest.write_text(
        "routes:\n  - path: /private/\n    source: ../outside.astro\n    indexable: true\n",
        encoding="utf-8",
    )
    issues = validate_route_manifest(manifest, tmp_path, {})
    assert any("INVALID_SOURCE" in issue.message for issue in issues)
