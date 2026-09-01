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

## Current validation deployment

The current deployment target is the Cloudflare Pages-managed
`https://secure-tools-hub-53i.pages.dev` site. This endpoint is for validating the Hub
deployment path and does not mean that the Hub has become the Secure Tools production site.

## Future production domain

`https://securetools.app` is **not yet connected to this repository**. It remains assigned to
Secure Tools Web Utilities. This workflow does not change DNS, configure a custom domain, or
perform the future production migration.

Any production domain migration and related redirects must be handled as a separate,
explicitly reviewed milestone.

## Prepared H3.5 deployment contract

The unmerged H3.4B branch prepares static `public/_headers` and `public/_redirects`
artifacts. The hostname-specific header rules keep the stable and immutable
`*.secure-tools-hub-53i.pages.dev` aliases non-indexable without applying noindex to the
future custom domain. The redirects contain only the 18 explicit H3.1 legacy Web Utilities
paths and preserve each path on `https://tools.securetools.app`; the Hub root and all Hub
routes are excluded.

Cloudflare Pages path redirects do not implement the future `www → apex` domain redirect.
That change requires a Cloudflare zone/account-level Redirect Rule or Bulk Redirect plus
proxied DNS during the coordinated H3.5 window. The exact activation and rollback order is
documented in [the H3.5 cutover runbook](./migrations/h3.5-cutover-runbook.md).

The H3.4B pull request does not attach a custom domain, change DNS, activate a `www` rule,
modify Search Console, or deploy from its feature branch.
