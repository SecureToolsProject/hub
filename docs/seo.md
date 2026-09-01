# Hub search metadata

Status: H3.4B preparation only. The pull request must remain unmerged until the coordinated
H3.5 cutover.

## Final canonical identity

The final Hub origin is `https://securetools.app`. Each of the 10 public Hub routes has one
self-referencing absolute canonical and matching `og:url`. Open Graph and X image metadata
uses the existing 1200×630 PNG at
`https://securetools.app/assets/brand/social-preview.png`.

`404.html` is an error document, not a canonical Hub route. It is excluded from the sitemap
and does not receive a canonical URL.

## Crawler files

- `public/sitemap.xml` lists exactly the 10 Hub canonical URLs.
- `public/robots.txt` allows crawling and references
  `https://securetools.app/sitemap.xml`.
- No Web Utilities route, tools host, legacy redirect source, or Pages hostname appears in the
  Hub sitemap.

The static `public/_headers` contract applies
`X-Robots-Tag: noindex, nofollow` only to:

```text
https://secure-tools-hub-53i.pages.dev/*
https://:version.secure-tools-hub-53i.pages.dev/*
```

The future `securetools.app` custom domain does not match those patterns and remains
indexable. No Worker or Pages Function is required.

## Legacy path ownership

`public/_redirects` contains exactly the 18 explicit 301 mappings in
`docs/migrations/h3-url-map.csv`. Every destination is the same path on
`https://tools.securetools.app`. The Hub root and all Hub routes are excluded; no wildcard
can swallow future Hub content.

These redirects become reachable on the apex only after H3.5 attaches the custom domain to
the Hub Pages project. The H3.4B feature branch does not deploy or activate them.

## Validation and search activation

`scripts/validate-h3-hub-cutover.py` checks route metadata, social image dimensions,
sitemap, robots, and Pages-alias isolation. `scripts/validate-h3-url-map.py` compares the
redirect artifact directly with the H3.1 inventory and rejects duplicates, wildcards, wrong
hosts, changed paths, non-301 status, root redirects, and Hub-route collisions.

Search Console remains unchanged during preparation. After H3.5 HTTP, TLS, canonical, and
redirect validation, submit the Hub sitemap to the root property and monitor Web Utilities
through the tools URL-prefix property. Do not use Change of Address for this partial
migration.
