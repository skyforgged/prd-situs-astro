from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_content import parse_frontmatter, validate_paths


def write_md(path: Path, frontmatter: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{frontmatter}\n---\n\nKonten.", encoding="utf-8")
    return path


def test_valid_core_contract(tmp_path: Path):
    file = write_md(tmp_path / "page.md", """id: 1
slug: home
schema:
  type: WebPage
publishedDate: 2026-11-20T01:00:00Z
updatedDate: 2026-11-26T03:00:00Z
blocks:
  - id: 1
    component: hero
  - id: 2
    component: faq""")
    assert validate_paths([file]) == []


def test_duplicate_yaml_keys_are_rejected(tmp_path: Path):
    file = write_md(tmp_path / "duplicate.md", """id: 1
id: 2
schema:
  type: WebPage""")
    data, error = parse_frontmatter(file)
    assert data is None
    assert "duplicate YAML key" in error


def test_document_ids_are_global_across_files(tmp_path: Path):
    first = write_md(tmp_path / "pages/a.md", "id: 9\nschema:\n  type: WebPage")
    second = write_md(tmp_path / "articles/b.md", "id: 9\nschema:\n  type: Article")
    issues = validate_paths([first, second])
    assert any("duplicate global document ID 9" in issue.message for issue in issues)


def test_block_ids_are_local_and_must_be_unique(tmp_path: Path):
    file = write_md(tmp_path / "page.md", """id: 1
schema:
  type: WebPage
blocks:
  - id: 1
    component: hero
  - id: 1
    component: faq""")
    issues = validate_paths([file])
    assert any("duplicate block ID 1" in issue.message for issue in issues)


@pytest.mark.parametrize("timestamp", [
    "2026-11-26T03:00:00+07:00",
    "2026-11-26T03:00:00",
    "2026-11-26T03:00:00.123Z",
    "2026-11-26",
])
def test_noncanonical_timestamps_are_rejected(tmp_path: Path, timestamp: str):
    file = write_md(tmp_path / "page.md", f"id: 1\nschema:\n  type: WebPage\nupdatedDate: '{timestamp}'")
    issues = validate_paths([file])
    assert any("ISO 8601 UTC seconds" in issue.message for issue in issues)


def test_updated_date_cannot_precede_published_date(tmp_path: Path):
    file = write_md(tmp_path / "page.md", """id: 1
schema:
  type: Article
publishedDate: 2026-11-27T03:00:00Z
updatedDate: 2026-11-26T03:00:00Z""")
    issues = validate_paths([file])
    assert any("updatedDate' must be equal to or later" in issue.message for issue in issues)


def test_boolean_is_not_accepted_as_integer_id(tmp_path: Path):
    file = write_md(tmp_path / "page.md", "id: true\nschema:\n  type: WebPage")
    issues = validate_paths([file])
    assert any("positive integer" in issue.message for issue in issues)
