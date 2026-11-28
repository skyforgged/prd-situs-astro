#!/usr/bin/env python3
"""Validate core PRD Astro content invariants across Markdown collections.

This first validator milestone intentionally covers repository-wide invariants:
frontmatter parsing, document IDs, block IDs, schema declarations, and timestamps.
Collection-specific fields, relations, block props, routes, and assets are layered
on in subsequent milestones through explicit registries rather than guesses.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
TIMESTAMP_FIELDS = {"publishedDate", "updatedDate"}


class DuplicateKeyError(ValueError):
    pass


class StrictLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_mapping(loader: StrictLoader, node: yaml.MappingNode, deep: bool = False) -> dict:
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping", node.start_mark,
                "found an unhashable key", key_node.start_mark,
            ) from exc
        if duplicate:
            raise DuplicateKeyError(f"duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


@dataclass(frozen=True)
class Issue:
    path: Path
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


def parse_frontmatter(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return None, f"cannot read UTF-8 Markdown: {exc}"
    match = FRONTMATTER_RE.match(source)
    if not match:
        return None, "missing or malformed YAML frontmatter (expected opening and closing ---)"
    try:
        data = yaml.load(match.group(1), Loader=StrictLoader)
    except (yaml.YAMLError, DuplicateKeyError) as exc:
        return None, f"invalid YAML frontmatter: {exc}"
    if not isinstance(data, dict):
        return None, "frontmatter must be a YAML mapping/object"
    return data, None


def _is_positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _parse_utc_timestamp(value: Any) -> datetime | None:
    # PyYAML parses ISO timestamp scalars into datetime instances. Strings are
    # also accepted only when they match the exact canonical UTC representation.
    if isinstance(value, datetime):
        parsed = value
        if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
            return None
        if parsed.microsecond != 0:
            return None
        return parsed
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value):
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def validate_document(path: Path, data: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    doc_id = data.get("id")
    if not _is_positive_int(doc_id):
        issues.append(Issue(path, "field 'id' must be a positive integer (boolean is not an integer ID)"))

    if "slug" in data and (not isinstance(data["slug"], str) or not data["slug"].strip()):
        issues.append(Issue(path, "field 'slug' must be a non-empty string when present"))

    if "schema" in data:
        schema = data["schema"]
        if not isinstance(schema, dict) or not isinstance(schema.get("type"), str) or not schema["type"].strip():
            issues.append(Issue(path, "field 'schema' must be an object with a non-empty string 'type'"))
    else:
        issues.append(Issue(path, "missing required field 'schema'"))

    if "blocks" in data:
        blocks = data["blocks"]
        if not isinstance(blocks, list):
            issues.append(Issue(path, "field 'blocks' must be an array when present"))
        else:
            seen_block_ids: set[int] = set()
            for index, block in enumerate(blocks):
                prefix = f"blocks[{index}]"
                if not isinstance(block, dict):
                    issues.append(Issue(path, f"{prefix} must be an object"))
                    continue
                block_id = block.get("id")
                if not _is_positive_int(block_id):
                    issues.append(Issue(path, f"{prefix}.id must be a positive integer"))
                elif block_id in seen_block_ids:
                    issues.append(Issue(path, f"duplicate block ID {block_id} within this document"))
                else:
                    seen_block_ids.add(block_id)
                component = block.get("component")
                if not isinstance(component, str) or not component.strip():
                    issues.append(Issue(path, f"{prefix}.component must be a non-empty string"))

    parsed_dates: dict[str, datetime] = {}
    for field in TIMESTAMP_FIELDS:
        if field in data:
            parsed = _parse_utc_timestamp(data[field])
            if parsed is None:
                issues.append(Issue(path, f"field '{field}' must use ISO 8601 UTC seconds: YYYY-MM-DDTHH:mm:ssZ"))
            else:
                parsed_dates[field] = parsed
    if "publishedDate" in parsed_dates and "updatedDate" in parsed_dates:
        if parsed_dates["updatedDate"] < parsed_dates["publishedDate"]:
            issues.append(Issue(path, "field 'updatedDate' must be equal to or later than 'publishedDate'"))
    return issues


def validate_paths(paths: list[Path]) -> list[Issue]:
    issues: list[Issue] = []
    seen_ids: dict[int, Path] = {}
    for path in sorted(paths):
        data, error = parse_frontmatter(path)
        if error:
            issues.append(Issue(path, error))
            continue
        assert data is not None
        issues.extend(validate_document(path, data))
        doc_id = data.get("id")
        if _is_positive_int(doc_id):
            if doc_id in seen_ids:
                issues.append(Issue(path, f"duplicate global document ID {doc_id}; first used in {seen_ids[doc_id]}"))
            else:
                seen_ids[doc_id] = path
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content_dir", type=Path, help="Root directory containing Markdown content collections")
    args = parser.parse_args(argv)
    if not args.content_dir.is_dir():
        print(f"ERROR: content directory does not exist: {args.content_dir}", file=sys.stderr)
        return 2
    files = sorted(path for path in args.content_dir.rglob("*.md") if path.is_file())
    if not files:
        print(f"ERROR: no Markdown files found under {args.content_dir}", file=sys.stderr)
        return 2
    issues = validate_paths(files)
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}")
        print(f"\nValidation failed: {len(issues)} issue(s) across {len(files)} Markdown file(s).")
        return 1
    print(f"Validation passed: {len(files)} Markdown file(s); core invariants are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
