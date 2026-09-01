#!/usr/bin/env python3
"""Validate the H3 migration inventory without network access or dependencies."""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from urllib.parse import urlsplit


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = REPOSITORY_ROOT / "docs" / "migrations" / "h3-url-map.csv"
PUBLIC_ROOT = REPOSITORY_ROOT / "public"
REDIRECTS_PATH = PUBLIC_ROOT / "_redirects"
EXPECTED_FIELDS = ["old_url", "new_url", "status", "reason"]


def hub_routes() -> set[str]:
    routes: set[str] = set()
    for index_file in PUBLIC_ROOT.rglob("index.html"):
        relative = index_file.relative_to(PUBLIC_ROOT).as_posix()
        routes.add("/" if relative == "index.html" else f"/{relative.removesuffix('index.html')}")
    return routes


def main() -> int:
    errors: list[str] = []
    with MAP_PATH.open(newline="", encoding="utf-8") as map_file:
        reader = csv.DictReader(map_file)
        if reader.fieldnames != EXPECTED_FIELDS:
            errors.append(f"columns must be exactly {EXPECTED_FIELDS!r}")
        rows = list(reader)

    seen_sources: set[str] = set()
    redirect_count = 0
    root_count = 0
    current_hub_routes = hub_routes()
    expected_redirects: dict[str, str] = {}

    for line_number, row in enumerate(rows, start=2):
        old_url = row.get("old_url", "")
        new_url = row.get("new_url", "")
        status = row.get("status", "")
        reason = row.get("reason", "").strip()
        old = urlsplit(old_url)
        new = urlsplit(new_url)

        if old_url in seen_sources:
            errors.append(f"line {line_number}: duplicate source URL {old_url}")
        seen_sources.add(old_url)

        if old.scheme != "https" or old.netloc != "securetools.app":
            errors.append(f"line {line_number}: source must use https://securetools.app")
        if old.query or old.fragment or new.query or new.fragment:
            errors.append(f"line {line_number}: inventory URLs must not contain query strings or fragments")
        if not old.path.endswith("/") or not new.path.endswith("/"):
            errors.append(f"line {line_number}: route paths must retain trailing slashes")
        if not reason:
            errors.append(f"line {line_number}: reason is required")

        if old.path == "/":
            root_count += 1
            if status != "no_redirect" or new_url != "https://securetools.app/":
                errors.append("the apex root must remain the Hub with status no_redirect")
            continue

        if status != "301":
            errors.append(f"line {line_number}: non-root migration entries must use status 301")
        else:
            redirect_count += 1
        if new.scheme != "https" or new.netloc != "tools.securetools.app":
            errors.append(f"line {line_number}: redirect target must use https://tools.securetools.app")
        if old.path != new.path:
            errors.append(f"line {line_number}: redirect target does not preserve {old.path}")
        if old.path in current_hub_routes:
            errors.append(f"line {line_number}: legacy redirect collides with Hub route {old.path}")
        expected_redirects[old.path] = new_url

    if root_count != 1:
        errors.append(f"expected one apex root reservation; found {root_count}")
    if redirect_count != 18:
        errors.append(f"expected 18 redirect inventory rows; found {redirect_count}")

    actual_redirects: dict[str, str] = {}
    if not REDIRECTS_PATH.is_file():
        errors.append("public/_redirects is missing")
    else:
        for line_number, raw_line in enumerate(
            REDIRECTS_PATH.read_text(encoding="utf-8").splitlines(), start=1
        ):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            fields = line.split()
            if len(fields) != 3:
                errors.append(f"_redirects line {line_number}: expected source destination status")
                continue
            source, destination, redirect_status = fields
            target = urlsplit(destination)
            if source in actual_redirects:
                errors.append(f"_redirects line {line_number}: duplicate source {source}")
            if "*" in source or ":" in source:
                errors.append(f"_redirects line {line_number}: wildcard or placeholder is not allowed")
            if source == "/":
                errors.append("_redirects must not redirect the Hub root")
            if source in current_hub_routes:
                errors.append(f"_redirects line {line_number}: Hub route collision {source}")
            if redirect_status != "301":
                errors.append(f"_redirects line {line_number}: status must be 301")
            if target.scheme != "https" or target.netloc != "tools.securetools.app":
                errors.append(f"_redirects line {line_number}: target host must be tools.securetools.app")
            if source != target.path:
                errors.append(f"_redirects line {line_number}: target must preserve path {source}")
            actual_redirects[source] = destination

    if actual_redirects != expected_redirects:
        missing = sorted(expected_redirects.keys() - actual_redirects.keys())
        unexpected = sorted(actual_redirects.keys() - expected_redirects.keys())
        mismatched = sorted(
            source
            for source in expected_redirects.keys() & actual_redirects.keys()
            if expected_redirects[source] != actual_redirects[source]
        )
        errors.append(
            "public/_redirects does not exactly match h3-url-map.csv "
            f"(missing={missing}, unexpected={unexpected}, mismatched={mismatched})"
        )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        f"Validated {len(rows)} inventory rows: "
        f"{redirect_count} redirects and {root_count} Hub-root no-redirect reservation."
    )
    print(f"Validated {len(actual_redirects)} exact Cloudflare Pages redirect rules.")
    print(f"Checked collisions against {len(current_hub_routes)} current Hub routes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
