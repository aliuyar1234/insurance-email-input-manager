# Releases

This project publishes installable artifacts via GitHub Releases.

## Artifacts

Each release publishes:

- Helm chart package: `ieim-<version>.tgz`
- SBOMs (SPDX JSON): `ieim-api.spdx.json`, `ieim-worker.spdx.json`, `ieim-scheduler.spdx.json`
- Provenance bundle:
  - `provenance.json`
  - `provenance.sig`
  - `provenance.crt`
- Checksums: `SHA256SUMS.txt`

Container images are published to GHCR:

- `ghcr.io/<owner>/ieim-api:<version>`
- `ghcr.io/<owner>/ieim-worker:<version>`
- `ghcr.io/<owner>/ieim-scheduler:<version>`

## Verify checksums

```bash
sha256sum -c SHA256SUMS.txt
```

## Verify provenance (cosign)

The release workflow signs `provenance.json` as a blob.

```bash
cosign verify-blob \
  --certificate provenance.crt \
  --signature provenance.sig \
  provenance.json
```

## Verify container image signatures (cosign)

Images are signed using keyless signing (GitHub Actions OIDC).

Basic verification:

```bash
cosign verify ghcr.io/<owner>/ieim-api:<version>
```

Stricter verification (recommended for production) can additionally pin the GitHub OIDC issuer and the expected workflow identity.

## Install from a release

See `docs/INSTALL_HELM.md` for Helm installs and `docs/INSTALL_COMPOSE.md` for Docker Compose.

