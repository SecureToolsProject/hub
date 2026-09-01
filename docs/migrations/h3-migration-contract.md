# H3.1 — Domain Migration Contract and URL Inventory

Status: planning only. Nothing in this document authorizes a DNS, hosting, custom-domain, redirect, metadata, or Search Console change.

Issue: [#12](https://github.com/SecureToolsProject/hub/issues/12)

## Scope and evidence

This contract was prepared against:

- Hub `main` at `5066544e41ccbf85053b06ad7d74be951eb79fed`.
- `SecureToolsProject/Secure_Tools` `main` at `e80446c47f5acde60fbcbdc170067e062a8780a7`, inspected read-only.
- The public `https://securetools.app` responses verified on 2026-09-01 KST.
- The Web Utilities source sitemap, HTML entry points, `robots.txt`, and `CNAME`.

The public inventory contains 19 user-facing routes. Eighteen are future host-migration candidates and `/` is deliberately reserved for the Hub without a redirect. Static assets, `404.html`, `robots.txt`, and `sitemap.xml` are not legacy content-page redirects; each final host must publish the versions appropriate to its own site.

## Canonical host contract

| Product | Final canonical host |
| --- | --- |
| Secure Tools Project Hub | `https://securetools.app` |
| Secure Tools Web Utilities | `https://tools.securetools.app` |

There is no global Secure Tools ecosystem version. Product and library versions remain owned by their respective projects.

## Safe migration architecture

The current Web Utilities GitHub Pages site has `securetools.app` as its custom domain. A GitHub Pages site has one configured custom-domain identity, with special automatic behavior only for the apex/`www` pairing; the plan must not treat `tools.securetools.app` as a second parallel identity on that same deployment. See [GitHub Pages custom-domain behavior](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages).

The preferred bridge is a separate, temporary Cloudflare Pages deployment of the unchanged Web Utilities production source. It would allow `tools.securetools.app` to complete functional, TLS, privacy, and visual validation while the existing GitHub Pages deployment continues serving `securetools.app`. Only after the tools host passes every gate may the apex move to the Hub. The bridge is proposed for H3.2 and is not created by H3.1.

Cloudflare requires a custom domain to be associated with the Pages project rather than relying only on a manually created CNAME. Apex and subdomain attachment also have different prerequisites; those operations belong to later phases. See [Cloudflare Pages custom domains](https://developers.cloudflare.com/pages/configuration/custom-domains/).

## Migration invariants

1. The existing Web Utilities production site remains available until the final root cutover.
2. `securetools.app` does not move before `tools.securetools.app` passes functional, TLS, privacy, and visual QA.
3. Existing Web Utilities paths remain unchanged during the first migration.
4. Host migration and path cleanup are separate changes.
5. No Search Console Change of Address operation is planned because this is a partial host migration and the root domain remains active as the Hub.
6. Permanent redirects map old URLs to semantically equivalent new URLs.
7. `/` is intentionally reused by the Hub and never redirects to the Web Utilities homepage.
8. Rollback remains possible until the migration has stabilized.
9. Query strings should be preserved by the eventual redirect implementation.
10. No redirect may claim an existing Hub route.

## Current Web Utilities URL inventory

All routes below returned HTTP 200 on `https://securetools.app` during H3.1 validation.

| Path | Source/sitemap state | Migration disposition |
| --- | --- | --- |
| `/` | Source and sitemap | Hub root; no redirect |
| `/about/` | Source and sitemap | Same path on tools host |
| `/privacy/` | Source and sitemap | Same path on tools host |
| `/tools/pdf/` | Source and sitemap | Same path on tools host |
| `/tools/pdf/images-to-pdf/` | Source and sitemap | Same path on tools host |
| `/tools/pdf/merge/` | Source and sitemap | Same path on tools host |
| `/tools/pdf/split/` | Source and sitemap | Same path on tools host |
| `/tools/pdf/organize/` | Source and sitemap | Same path on tools host |
| `/tools/pdf/to-images/` | Source and sitemap | Same path on tools host |
| `/tools/pdf/metadata/` | Source and sitemap | Same path on tools host |
| `/tools/image/` | Source and sitemap | Same path on tools host |
| `/tools/image/converter/` | Source and sitemap | Same path on tools host |
| `/tools/image/resize/` | Source and sitemap | Same path on tools host |
| `/tools/image/compress/` | Source and sitemap | Same path on tools host |
| `/tools/image/metadata/` | Source and sitemap | Same path on tools host |
| `/tools/privacy/` | Source and sitemap | Same path on tools host |
| `/tools/scan/` | Source and sitemap | Same path on tools host |
| `/tools/media/` | Source and sitemap | Same path on tools host |
| `/tools/image-to-pdf/` | Source only; noindex legacy interstitial | Preserve same path on tools host; do not fold path cleanup into host migration |

The reviewable mapping is [h3-url-map.csv](./h3-url-map.csv). It contains 19 inventory rows: 18 planned `301` redirects and one `no_redirect` Hub-root reservation.

## Redirect contract

After apex cutover, requests for the 18 inventoried legacy paths on `securetools.app` should return `301 Moved Permanently` to the identical path on `tools.securetools.app`. The apex `/` must render the Hub and must not redirect. No nonexistent or speculative route is included.

The Hub is expected to own these source-controlled path redirects after cutover, likely through a future `public/_redirects` file. H3.1 does not create that file. Cloudflare Pages supports path redirects in `_redirects`, but not domain-level redirect rules. See [Cloudflare Pages redirects](https://developers.cloudflare.com/pages/configuration/redirects/).

Host-level behavior such as `www.securetools.app → securetools.app` must be implemented later with Cloudflare zone-level redirect configuration, not an ordinary Pages `_redirects` domain rule. Redirect activation must be isolated from DNS and canonical-metadata activation so each can be verified and rolled back independently.

## SEO contract

These are future activation requirements, not current metadata.

### Hub

- `canonical`: absolute `https://securetools.app/...` URL.
- `og:url`: absolute `https://securetools.app/...` URL.
- `og:image` and `twitter:image`: resolvable absolute `https://securetools.app/...` URLs.
- `sitemap.xml`: Hub URLs only.
- `robots.txt`: references the Hub sitemap.

### Web Utilities

- `canonical`: absolute `https://tools.securetools.app/...` URL.
- `og:url`: absolute `https://tools.securetools.app/...` URL.
- `og:image` and `twitter:image`: resolvable absolute `https://tools.securetools.app/...` URLs.
- `sitemap.xml`: Web Utilities URLs only.
- `robots.txt`: references the Web Utilities sitemap.

Canonical metadata, social image URLs, sitemaps, and robots files must not be activated until their target host is serving the correct production content over valid TLS.

## Search Console strategy

- Do not use Change of Address for `securetools.app → tools.securetools.app`; the root remains active and only the Web Utilities pages move.
- Add a separate `https://tools.securetools.app/` URL-prefix property for focused Web Utilities monitoring.
- A Domain property for `securetools.app` may optionally aggregate root and subdomain data.
- Submit separate Hub and Web Utilities sitemaps only after their production hosts and metadata are active.

Google explicitly excludes partial-page moves from Change of Address and recommends redirects plus sitemap updates instead. See [Search Console Change of Address guidance](https://support.google.com/webmasters/answer/9370220).

## Rollback contract

### Before apex cutover

- Leave the current GitHub Pages Web Utilities production deployment, `CNAME`, and DNS untouched.
- Treat the proposed Pages bridge and tools subdomain as additive validation surfaces only.
- A failed tools-host gate is a no-go; it does not trigger apex work.

### After apex cutover

- Preserve the previous GitHub Pages Web Utilities deployment and configuration long enough to remain a viable rollback origin.
- Keep DNS, redirects, and SEO activation changes isolated so each can be reverted independently.
- Record the pre-cutover DNS values, certificates, deployment identifiers, and tested rollback procedure before changing the apex.
- Do not remove rollback infrastructure during the initial stabilization period.
- If a critical gate regresses, restore the prior apex origin first and then revert redirect or SEO layers as required.

## Migration gates

Every gate requires recorded evidence and an explicit go/no-go decision. A failure blocks the next phase.

| Gate | Go criteria | No-go examples |
| --- | --- | --- |
| DNS | Intended records and TTLs reviewed; no premature apex change | Unexpected record replacement or unresolved tools host |
| TLS | Valid certificate and hostname coverage on the candidate host | Certificate error, hostname mismatch, incomplete issuance |
| HTTP status | All 19 inventory paths have their expected pre-cutover responses; later redirects return exactly 301 | 4xx/5xx, redirect loop, wrong status |
| Asset loading | Same-origin CSS, JavaScript, icons, workers, and tool assets load without mixed content | Missing assets, CSP errors, mixed content |
| PDF tools | Open and complete smoke tests for images-to-PDF, merge, split, organize, PDF-to-images, and metadata | Load failure, incorrect output, blocked download |
| Image tools | Open and complete converter, resize, compress, and metadata smoke tests | Processing or download regression |
| Metadata tools | PDF and image inspection/cleaning behavior matches production | Metadata leak or destructive mismatch |
| Privacy/local processing | Network inspection confirms file data remains local and disclosures remain accurate | File upload, new telemetry, undocumented request |
| Canonical metadata | Each page points only to its final serving host | Mixed hosts, premature activation, relative canonical |
| Sitemap | Each host lists only its own canonical URLs and every listed URL succeeds | Cross-host URLs, stale or missing routes |
| `robots.txt` | Each host references only its own sitemap and does not accidentally block production | Wrong sitemap or unintended disallow |
| Redirects | All 18 mapped paths preserve path and query; `/` renders Hub; no Hub collision | Root redirect, chain, path rewrite, speculative rule |
| Visual QA | Representative desktop/mobile, light/dark, keyboard, focus, zoom, and overflow checks pass | Unreviewed or material visual/accessibility regression |
| Rollback readiness | Previous origin and configuration are preserved; rollback is rehearsed and documented | Destructive removal or untested restoration |

## Proposed later H3 phases

1. **H3.2 — Web Utilities Migration Bridge:** create a temporary Cloudflare Pages delivery path for the unchanged Web Utilities build while preserving GitHub Pages production.
2. **H3.3 — Tools Subdomain Parallel Validation:** attach and validate `tools.securetools.app` across all gates before touching the apex.
3. **H3.4 — Canonical & Search Metadata Migration:** prepare and activate host-specific canonicals, social URLs, sitemap, and robots changes at the correct deployment boundary.
4. **H3.5 — Apex Cutover & Legacy Redirects:** move `securetools.app` to the Hub and activate the reviewed 301 map and zone-level host redirects.
5. **H3.6 — Search Migration Monitoring:** submit host-specific sitemaps and monitor indexing, redirects, availability, and rollback signals.

No later phase is authorized by this document alone.

## H3.4B preparation

[Issue #14](https://github.com/SecureToolsProject/hub/issues/14) prepares the Hub-owned H3.5
artifacts on an unmerged branch: final Hub metadata, sitemap and robots files,
hostname-specific Pages-alias noindex headers, and the 18 explicit redirects derived from this
inventory. The executable sequence and rollback requirements are in
[h3.5-cutover-runbook.md](./h3.5-cutover-runbook.md).

These files do not authorize or perform a merge, deployment, apex or `www` DNS change,
custom-domain attachment, zone redirect, Search Console operation, or Secure_Tools PR #73
merge. H3.5 must coordinate those operations only after all preflight gates pass.
