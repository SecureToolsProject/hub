# Hub architecture

## Responsibility

The Secure Tools Project Hub is the catalog, documentation, and navigation layer for the
Secure Tools ecosystem. It introduces the project, records shared principles, and directs
people to independently maintained products and libraries. It is not an application runtime
or a distribution that combines every project.

## Repository and release boundaries

Products live in independent repositories and retain responsibility for their own design,
implementation, testing, distribution, and support. Each product owns its release schedule
and version numbers. Future or experimental projects can be added without coupling their
lifecycle to existing products.

Libraries are listed separately from end-user products. A reusable package such as Secure
Metadata may support more than one product, but remains independently maintained and is not
presented as an application.

There is no global Secure Tools ecosystem semantic version. In particular, the version of
Secure Tools Web Utilities describes that product only.

## Static-first design

The Hub is a static-first website. Its publishable files live in `public/` and require no
server-side runtime. At this milestone it uses semantic HTML and CSS without a framework,
external asset pipeline, or central runtime dependency.

The Hub intentionally has no plugin framework. Projects integrate through documented links
and shared principles rather than executable plugins or a common application shell. This
keeps the catalog operationally separate from the software it describes.

## Visual identity and asset provenance

The public `SecureToolsProject/Secure_Tools` repository is the visual reference for the Hub's
system-first typography, warm neutral surfaces, green accent and signal mark, blue keyboard
focus treatment, spacing scale, borders, radii, and light/dark color behavior. The Hub applies
those shared cues to an editorial catalog rather than copying tool-specific application UI.

All Hub assets are served locally from `public/assets/`; no font, image, icon, or stylesheet is
loaded from the reference project at runtime. The SVG favicon is a Hub-owned vector adaptation
of the circular CSS brand mark used by Web Utilities. The 1200×630 social preview was generated
specifically for the Hub and uses its catalog language and visual system; it is not a copy of
the Web Utilities social image.

The social preview asset is ready, but host-dependent `og:image` and `twitter:image` metadata
is intentionally deferred until a separately reviewed production-domain migration establishes
the permanent Hub origin. Canonical and `og:url` metadata is deferred for the same reason. This
avoids coupling the public identity to a temporary validation hostname or claiming
`securetools.app` before migration.

## Product disclosure contract

The Hub uses a consistent, human-readable disclosure contract for products and libraries:

- name and concise description;
- type and current status;
- repository and primary entry point, when established;
- platform;
- processing location and boundaries;
- network behavior;
- storage behavior;
- telemetry behavior;
- license;
- version, where applicable; and
- privacy or technical documentation.

The contract does not require unsupported certainty. Fields that are not established may be
marked `Not finalized`, `Not yet released`, or `To be documented before release`. The linked
product repository and its release-specific documentation remain the source of truth.
