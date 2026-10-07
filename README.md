# Secure Tools Project Hub

This repository is the future catalog, documentation, and navigation layer for the Secure
Tools local-first, privacy-conscious software ecosystem. It provides a multi-page static site
in `public/` and records the ecosystem's shared boundaries in `docs/`.

The Hub is not a combined application, central runtime, release bundle, or global version for
Secure Tools products. Products and libraries remain independently maintained and released.

## Status

The Hub is live at `https://securetools.app/`. It discovers independently maintained
products; Web Utilities is hosted at `https://tools.securetools.app/`.
GitHub Actions validates and deploys the static `public/` directory to Cloudflare Pages.
See [the v2.2 link migration](docs/migrations/v2.2-tool-links.md) for canonical tool destinations.

## Documentation

- [Architecture](docs/architecture.md)
- [Privacy model](docs/privacy-model.md)
- [Deployment transparency](docs/deployment.md)
- [Search metadata](docs/seo.md)
- [H3.5 cutover runbook](docs/migrations/h3.5-cutover-runbook.md)
- [H2.2 quality assurance](docs/h2.2-qa.md)

The static site can be previewed by serving `public/` with any local static file server.
