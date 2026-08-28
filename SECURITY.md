# Security Policy

## Supported versions

Security fixes are applied to the latest release on the default branch. Pre-release snapshots and older tags are not guaranteed to receive backports.

## Reporting a vulnerability

Please report vulnerabilities privately. Use GitHub's **Report a vulnerability** / private security-advisory flow for this repository when it is available. If it is not available, contact the maintainer through a trusted private channel shown on the repository owner's profile and share only enough information to establish a secure reporting path.

Do not open a public issue containing an exploit, credential, customer/order information, exact private merchant metrics, private endpoint, token, cookie, raw connector response, or other sensitive evidence. Do not test against the live PrimeOrder store, customer/admin accounts, checkout, integrations, or vendor systems without separate written authorization.

Include when safe:

- affected version/commit and component;
- concise impact and prerequisites;
- privacy-safe reproduction using `public-demo` fixtures;
- expected versus observed behavior;
- suggested mitigation, if known;
- whether you believe credentials or private data were exposed (do not include the values).

## Response expectations

The maintainer will attempt to acknowledge a complete private report promptly, validate scope, assess severity, coordinate remediation and publish a sanitized advisory when appropriate. No fixed response or remediation SLA is promised by this portfolio project.

## Project security boundaries

- PrimeOrder/Salla and all optional external connectors are read-only.
- Public builds and evidence use deterministic synthetic data only.
- Live aggregate exports remain in ignored local private paths.
- The public GitHub Pages application is static and must not call local/private APIs.
- Credentials belong in official tool/OS/environment secret storage, never repository files, logs, screenshots or chat.

Security design, threat model, release criteria and incident notes are documented under [`docs/security/`](docs/security/SECURITY_CONTROLS.md) and [`docs/privacy/`](docs/privacy/PRIVACY_DESIGN.md).

## Safe harbor scope

No broad testing authorization is granted. You may inspect the public repository and deterministic local `public-demo` in a way that does not access third-party/live systems, other users' data, or cause disruption. Social engineering, denial of service, credential attacks, automated scanning of the live merchant store, live cart/checkout/order activity, and vendor-account testing are out of scope.

