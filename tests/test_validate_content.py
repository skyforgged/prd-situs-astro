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
    source = PAGE.replace("Intro", "Intro\n\nParagraf kedua").replace("Profil perusahaan.", "**Profil** perusahaan.")
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
