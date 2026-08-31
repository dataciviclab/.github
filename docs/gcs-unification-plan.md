# Piano di unificazione GCS Auth + Pipeline Standardizzate

**Stato:** in corso (31/08/2026)
**Obiettivo:** semplificare, uniformare e standardizzare il flusso end-to-end
  producer (pipeline → GCS) e consumer (dashboard ← GCS).

## Scoperta chiave

> `attribute.repository/*` NON funziona con GCP IAM quando i valori
> contengono `/` (es. `dataciviclab/eurostat`). Il wildcard non matcha.
> Fix: usare `attribute.repository_owner/dataciviclab` (senza slash).

## Architettura (aggiornata)

### Componenti

```
.github/
├── actions/
│   ├── gcs-auth/action.yml          # WIF + legacy SA key fallback
│   ├── python-setup/action.yml
│   ├── registry-update-pr/action.yml
│   └── python-ci/action.yml
├── .github/workflows/
│   ├── pipeline-reusable.yml        # ✅ REUSABLE (merged)
│   ├── dataset-config-check-reusable.yml
│   └── test-audit-reusable.yml
└── scripts/
    └── drift_check.py
```

### Reusable workflow — Input disponibili

| Input | Tipo | Default | Descrizione |
|-------|------|---------|-------------|
| `repo-slug` | string | (required) | Prefisso GCS/registry |
| `run-command` | string | (required) | Comando make (es. `make run-all`) |
| `sync-pattern` | string | `flat` | `flat` o `per-dataset` |
| `pre-run-command` | string | `""` | Detect, codelists, bootstrap |
| `verify-command` | string | `""` | Verify post-run |
| `extra-env` | string | `""` | KEY=VALUE per riga |
| `python-extra-packages` | string | `""` | pip extras |

### Template caller (~25 righe)

```yaml
jobs:
  pipeline:
    uses: dataciviclab/.github/.github/workflows/pipeline-reusable.yml@main
    with:
      repo-slug: <slug>
      run-command: make run-all
      verify-command: make verify
    secrets: inherit
```

## Stato migrazione

### ✅ Completati

| Repo | PR | Tipo |
|------|----|------|
| `.github` | #28 (merged) | pipeline-reusable.yml |
| `eurostat` | #134 (merged) | WIF custom (detect logic) |
| `open-conto-annuale` | #11 (merged) | WIF + reusable |
| `open-siope` | #82 (aperta) | WIF + reusable |
| `debito-pubblico-intelligence` | #11 (aperta) | WIF fix (no reusable) |

### ⏳ Da migrare

| Repo | Difficoltà | Candidate reusable | Note |
|------|-----------|-------------------|------|
| `opere-pubbliche-intelligence` | 🟢 bassa | ✅ sì | `make run-all && make layers && make panorama` |
| `dcl-bologna` | 🟡 media | ✅ sì (con pre-run) | Bootstrap varchi-ztl |
| `open-politica` | 🔴 alta | ❌ no | Detect complesso (compose/, ponte-persona) |
| `senato-akn` | 🔴 alta | ❌ no | Self-hosted runner, extract incrementale |
| `rna-aiuti-stato` | 🔴 alta | ❌ no | Self-hosted runner, full_batch, manifest |

### ⚪ Non migrabili

| Repo | Motivo |
|------|--------|
| `dataset-incubator` | Usa già WIF (pattern diverso) |
| `costituzione-italiana` | Nessun sync GCS |

### 🔑 SA key da eliminare (dopo validazione)

- `GCP_SA_KEY_EUROSTAT`
- `GCP_SA_KEY` (open-siope, open-conto-annuale)
- `GCP_SA_KEY_SENATO_AKN`
- `GCP_SA_KEY_RNA`
- `GCP_SA_KEY_OPI`
- `GCP_SA_KEY_DPI`
- `GCP_SA_KEY_OPEN_POLITICA`
- `GCP_SA_KEY_DCL_BOLOGNA`

## Prossimi passi

1. ✅ Mergiare open-siope #82 + DPI #11
2. ⏳ Migrare opere-pubbliche-intelligence + dcl-bologna
3. 📋 Aggiornare project-template con pattern WIF + reusable
4. 📋 Aggiornare drift-check per verificare WIF
5. 🗑️ Eliminare SA key vecchie
6. 📋 Aggiornare ADR-001 con Fase 1 + 2 completate

## Note operative

### GCP Setup (completato)

- Pool: `dataciviclab-pool` (project: `dataciviclab`, num: `217326868340`)
- Provider: `github-actions` (issuer: `token.actions.githubusercontent.com`)
- SA: `dcl-gcs-publisher@dataciviclab.iam.gserviceaccount.com`
- IAM: `workloadIdentityUser` + `serviceAccountTokenCreator` su `attribute.repository_owner/dataciviclab`
- API: `iamcredentials.googleapis.com` abilitata
- Bucket: `objectAdmin` su `dataciviclab-clean` + `dataciviclab-mart`

### GitHub Secrets (org-level)

```
GCP_WORKLOAD_IDENTITY_PROVIDER: projects/217326868340/locations/global/workloadIdentityPools/dataciviclab-pool/providers/github-actions
GCP_SERVICE_ACCOUNT: dcl-gcs-publisher@dataciviclab.iam.gserviceaccount.com
```

### Pattern WIF (per i nuovi repo)

```yaml
# Nel caller:
env:
  GCP_WORKLOAD_IDENTITY_PROVIDER: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
  GCP_SERVICE_ACCOUNT: ${{ secrets.GCP_SERVICE_ACCOUNT }}

# Nel job:
permissions:
  id-token: write

# Auth:
- uses: google-github-actions/auth@v3
  with:
    workload_identity_provider: ${{ env.GCP_WORKLOAD_IDENTITY_PROVIDER }}
    service_account: ${{ env.GCP_SERVICE_ACCOUNT }}
- uses: google-github-actions/setup-gcloud@v3
```
