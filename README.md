# Secure Tools Project Hub

This repository is the future catalog, documentation, and navigation layer for the Secure
Tools local-first, privacy-conscious software ecosystem. It provides a multi-page static site
in `public/` and records the ecosystem's shared boundaries in `docs/`.

The Hub is not a combined application, central runtime, release bundle, or global version for
Secure Tools products. Products and libraries remain independently maintained and released.

## Status

The repository now includes its information architecture, standardized product disclosure
model, and a production-polished visual system aligned with Secure Tools Web Utilities, but it
is not released as the production Hub.
Production migration has not happened: `securetools.app` remains assigned to Secure Tools Web
Utilities. The configured workflow publishes `main` only to the Cloudflare-managed `pages.dev`
validation target.

## Documentation

- [Architecture](docs/architecture.md)
- [Privacy model](docs/privacy-model.md)
- [Deployment transparency](docs/deployment.md)
- [H2.2 quality assurance](docs/h2.2-qa.md)

The static site can be previewed by serving `public/` with any local static file server.
