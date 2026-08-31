# Ecosystem privacy model

Secure Tools is guided by local-first processing where practical, minimal unnecessary data
exposure, transparent network behavior, privacy-aware defaults, auditable implementation
where practical, and traceable deployment.

These are ecosystem-level design principles, not identical guarantees for every product.
Exact privacy, storage, and network behavior is product-specific and can change with a
product's features, platform, and release. No ecosystem-level statement should be interpreted
as an absolute security or privacy guarantee.

## Behaviors products must describe

Each product must disclose what it actually does, including applicable behaviors such as:

- browser-local processing, and when data remains within the browser;
- desktop-local processing, including files or processes accessed on the device;
- model downloads needed to enable local AI features;
- optional network access initiated by a feature or by the user;
- static website requests needed to load published HTML, CSS, and other assets;
- application update checks and the information those checks transmit; and
- caches, settings, databases, or other local storage retained on the device.

A local-first feature may still require an initial application or model download, update
checks, or optional online capabilities. Conversely, a static website still creates ordinary
requests to its hosting provider when it is visited. Product documentation should distinguish
these cases instead of relying on a broad ecosystem claim.

## Product responsibility

Every product repository is responsible for maintaining accurate, release-specific privacy
and network documentation. Disclosures should identify required and optional connections,
the purpose of retained local data, relevant user controls, and meaningful changes between
releases.
