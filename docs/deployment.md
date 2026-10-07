# Deployment transparency

The Hub uses a static Cloudflare Pages Direct Upload path. The public workflow makes the
deployment sequence inspectable:

```text
main
→ GitHub Actions
→ Cloudflare Wrangler
→ Cloudflare Pages
```

| Setting | Value |
| --- | --- |
| Source | `https://github.com/SecureToolsProject/hub` |
| Production branch | `main` |
| Static output | `public/` |
| Hosting | Cloudflare Pages |
| Cloudflare Pages project | `secure-tools-hub` |
| Build transformation | None |
| Server-side application runtime | None |
| Pages Functions | None |
| Workers | None |
| Analytics and telemetry | Not configured |

## Deployment provenance

Deployment is initiated by the public GitHub Actions workflow at
`.github/workflows/deploy.yml`. It runs only for a push to `main` or an explicit manual
dispatch. Pull requests, feature branch pushes, and tags do not trigger it.

The workflow validates the static output and uploads only `public/`; it performs no build or
content transformation. The Cloudflare API token and account ID are stored only as GitHub
Actions secrets. The API token is intended to be scoped to the relevant Cloudflare account
with `Cloudflare Pages: Edit` permission.

External actions are pinned to immutable full commit SHAs. The Wrangler Action receives the
workflow's short-lived `GITHUB_TOKEN` so that each upload creates or updates a visible GitHub
Deployment record. The workflow has only `contents: read` and `deployments: write`
permissions.

## Production identity

`https://securetools.app/` serves the Hub. `https://tools.securetools.app/` serves Web Utilities.
The stable and immutable `secure-tools-hub-53i.pages.dev` aliases remain validation endpoints
with hostname-specific noindex headers. The Hub is a static catalog, not a tool runtime.

## Redirect contract

`public/_redirects` preserves the 18 historical apex source paths and sends them directly
to root-level canonical Web Utilities URLs with 301 responses. The root and all Hub routes
remain Hub-owned. Query strings are preserved by Pages redirect behavior.
The migration CSV documents historical sources, canonical targets, and tools-host 308 support.
See [the v2.2 link migration](./migrations/v2.2-tool-links.md).

This content/link migration changes no DNS, custom domains, TLS, zone rules, Search Console,
or Web Utilities code. The H3.5 runbook is retained as a historical cutover record.
