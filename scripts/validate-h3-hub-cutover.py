#!/usr/bin/env python3
"""Validate the prepared H3 Hub SEO and crawler contract."""

from __future__ import annotations

import re
import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
ORIGIN = "https://securetools.app"
SOCIAL_IMAGE = f"{ORIGIN}/assets/brand/social-preview.png"
EXPECTED_ROUTES = {
    "/",
    "/products/",
    "/products/web-utilities/",
    "/products/desktop-pet/",
    "/products/local-ai/",
    "/libraries/",
    "/libraries/secure-metadata/",
    "/principles/",
    "/principles/privacy/",
    "/project/",
}
EXPECTED_HEADERS = """https://secure-tools-hub-53i.pages.dev/*
  X-Robots-Tag: noindex, nofollow

https://:version.secure-tools-hub-53i.pages.dev/*
  X-Robots-Tag: noindex, nofollow
"""


def route_for(index_file: Path) -> str:
    relative = index_file.relative_to(PUBLIC).as_posix()
    return "/" if relative == "index.html" else f"/{relative.removesuffix('index.html')}"


def values(markup: str, pattern: str) -> list[str]:
    return re.findall(pattern, markup, flags=re.IGNORECASE)


def main() -> int:
    errors: list[str] = []
    page_titles: set[str] = set()
    page_descriptions: set[str] = set()
    pages = {route_for(path): path for path in PUBLIC.rglob("index.html")}
    if set(pages) != EXPECTED_ROUTES:
        errors.append(
            f"Hub route inventory mismatch: missing={sorted(EXPECTED_ROUTES - set(pages))}, "
            f"unexpected={sorted(set(pages) - EXPECTED_ROUTES)}"
        )

    for route, path in sorted(pages.items()):
        markup = path.read_text(encoding="utf-8")
        expected_url = f"{ORIGIN}{route}"
        checks = {
            "canonical": values(markup, r'<link\s+rel="canonical"\s+href="([^"]+)"'),
            "og:url": values(markup, r'<meta\s+property="og:url"\s+content="([^"]+)"'),
            "og:image": values(markup, r'<meta\s+property="og:image"\s+content="([^"]+)"'),
            "twitter:image": values(markup, r'<meta\s+name="twitter:image"\s+content="([^"]+)"'),
        }
        title = values(markup, r"<title>([^<]+)</title>")
        description = values(markup, r'<meta\s+name="description"\s+content="([^"]+)"')
        if len(title) != 1 or not title[0].strip():
            errors.append(f"{route}: exactly one non-empty title is required")
        else:
            page_titles.add(title[0])
        if len(description) != 1 or not description[0].strip():
            errors.append(f"{route}: exactly one non-empty description is required")
        else:
            page_descriptions.add(description[0])
        required_metadata = {
            "og:title": r'<meta\s+property="og:title"\s+content="([^"]+)"',
            "og:description": r'<meta\s+property="og:description"\s+content="([^"]+)"',
            "og:type": r'<meta\s+property="og:type"\s+content="website"',
            "twitter:title": r'<meta\s+name="twitter:title"\s+content="([^"]+)"',
            "twitter:description": r'<meta\s+name="twitter:description"\s+content="([^"]+)"',
            "twitter:card": r'<meta\s+name="twitter:card"\s+content="summary_large_image"',
        }
        for label, pattern in required_metadata.items():
            if len(values(markup, pattern)) != 1:
                errors.append(f"{route}: exactly one {label} value is required")
        for label in ("canonical", "og:url"):
            if checks[label] != [expected_url]:
                errors.append(f"{route}: {label} must be exactly {expected_url}")
        for label in ("og:image", "twitter:image"):
            if checks[label] != [SOCIAL_IMAGE]:
                errors.append(f"{route}: {label} must be exactly {SOCIAL_IMAGE}")
        if 'content="1200"' not in markup or 'content="630"' not in markup:
            errors.append(f"{route}: social image dimensions are missing")
        if "pages.dev" in markup:
            errors.append(f"{route}: pages.dev must not appear in page metadata or content")
        if "<script" in markup.lower():
            errors.append(f"{route}: Hub pages must remain JavaScript-free")

    if len(page_titles) != len(pages):
        errors.append("Hub page titles must be page-specific")
    if len(page_descriptions) != len(pages):
        errors.append("Hub page descriptions must be page-specific")

    sitemap_path = PUBLIC / "sitemap.xml"
    try:
        sitemap = ET.parse(sitemap_path)
        locations = [
            element.text or ""
            for element in sitemap.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/"
                                           "{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        ]
    except (OSError, ET.ParseError) as error:
        errors.append(f"invalid sitemap.xml: {error}")
        locations = []
    expected_locations = {f"{ORIGIN}{route}" for route in EXPECTED_ROUTES}
    if len(locations) != len(set(locations)):
        errors.append("sitemap.xml contains duplicate URLs")
    if set(locations) != expected_locations:
        errors.append("sitemap.xml must contain exactly the 10 Hub canonical URLs")
    if any("tools.securetools.app" in url or "pages.dev" in url for url in locations):
        errors.append("sitemap.xml contains a non-Hub host")

    robots = (PUBLIC / "robots.txt").read_text(encoding="utf-8")
    expected_robots = "User-agent: *\nAllow: /\n\nSitemap: https://securetools.app/sitemap.xml\n"
    if robots != expected_robots:
        errors.append("robots.txt does not match the final Hub crawler contract")

    headers = (PUBLIC / "_headers").read_text(encoding="utf-8")
    if headers != EXPECTED_HEADERS:
        errors.append("_headers does not exactly isolate stable and immutable Pages aliases")

    image_path = PUBLIC / "assets" / "brand" / "social-preview.png"
    try:
        image_bytes = image_path.read_bytes()
        if image_bytes[:8] != b"\x89PNG\r\n\x1a\n":
            errors.append("social preview must be a PNG")
        elif struct.unpack(">II", image_bytes[16:24]) != (1200, 630):
            errors.append("social preview dimensions must be exactly 1200 x 630")
    except OSError as error:
        errors.append(f"social preview is unavailable: {error}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(pages)} Hub routes and canonical metadata records.")
    print(f"Validated {len(locations)} unique Hub sitemap URLs and robots.txt.")
    print("Validated Pages-alias noindex configuration and 1200 x 630 PNG social image.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
