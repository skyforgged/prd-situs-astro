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
  type: AboutPage
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
    second = write_md(tmp_path / "articles/b.md", PAGE.replace("type: AboutPage", "type: Article").replace("id: 1", "id: 1"))
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
    good = PAGE.replace("type: AboutPage", "type: WebPage\n  mainEntity:\n    type: DefinedTerm").replace(
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
