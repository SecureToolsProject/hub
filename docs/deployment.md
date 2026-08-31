# Deployment model

This document describes the intended production model. It does not configure or authorize a
deployment.

| Setting | Intended value |
| --- | --- |
| Production domain | `https://securetools.app` — **not yet connected to this repository** |
| Source | `https://github.com/SecureToolsProject/hub` |
| Production branch | `main` |
| Static output directory | `public/` |
| Planned hosting | Cloudflare Pages |
| Planned deployment | GitHub Actions → Cloudflare Pages |
| Server-side runtime | None planned |
| Pages Functions | None planned |
| Workers | None planned |
| Analytics | None planned |

`securetools.app` currently remains assigned to Secure Tools Web Utilities and must not be
changed during this milestone. No DNS, CNAME, GitHub Pages, Cloudflare Pages, or deployment
workflow changes are part of the Hub foundation.

Any later production migration must be handled as a separate, explicitly reviewed change.
