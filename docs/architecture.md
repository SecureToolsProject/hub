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
