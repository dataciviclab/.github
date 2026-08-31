# Piano di unificazione GCS Auth + Pipeline Standardizzate

**Stato:** draft (2026-08-31)
**Obiettivo:** semplificare, uniformare e standardizzare il flusso end-to-end
  producer (pipeline → GCS) e consumer (dashboard ← GCS).

## Contesto

L'org ha ~15 repo con pipeline che pubblicano dati su 2 bucket GCS pubblici
(`dataciviclab-clean`, `dataciviclab-mart`). Ogni repo ha la propria Service
Account con secret nome diverso, e il pipeline.yml è scritto da zero con
pattern simili ma non identici.

### Stato attuale (agosto 2026)

| Repo | Secret | Auth | Path GCS |
|------|--------|------|----------|
| eurostat | `GCP_SA_KEY_EUROSTAT` | gcs-auth (SA key) | `eurostat/$slug/` |
| open-siope | `GCP_SA_KEY` | gcs-auth (SA key) | `siope/` |
| open-conto-annuale | `GCP_SA_KEY` | gcs-auth (SA key) | `conto-annuale/` |
| senato-akn | `GCP_SA_KEY_SENATO_AKN` | gcs-auth (SA key) | `$slug/` (no prefix!) |
| rna-aiuti-stato | `GCP_SA_KEY_RNA` | gcs-auth (SA key) | `$slug/` (no prefix!) |
| opere-pubbliche-intelligence | `GCP_SA_KEY_OPI` | gcs-auth (SA key) | `opere_pubbliche_intelligence/$slug/$year/` |
| debito-pubblico-intelligence | `GCP_SA_KEY_DPI` | gcs-auth (SA key) | `debito_pubblico_intelligence/$slug/$year/` |
| open-politica | `GCP_SA_KEY_OPEN_POLITICA` | gcs-auth (SA key) | `open-politica/$slug/$year/` |
| dcl-bologna | `GCP_SA_KEY_DCL_BOLOGNA` | inline (non usa gcs-auth) | *(placeholder D3)* |
| dataset-incubator | WIF | google-github-actions/auth | `$slug/$year/` |
| costituzione-italiana | — | nessun sync | — |

**Problemi:** 8 SA key diverse, path non standardizzate, pipeline.yml duplicato 10 volte.

### Info confermate

- Bucket **pubblici** (lettura anonima)
- Tutte le SA hanno gli **stessi permessi**: write su clean + mart
- Ogni repo ha 1 SA dedicata (funzionalmente identiche)
- Dashboard già pubbliche (Streamlit Cloud)

## Architettura proposta

### Principi

1. **1 SA unica** → 1 Workload Identity Federation, zero chiavi statiche
2. **Path contract standardizzato** → `gs://{bucket}/{repo-slug}/{dataset-slug}/{year}/`
3. **Reusable pipeline workflow** → il 90% del logic in `.github`, ogni repo ~15 righe
4. **Drift-check enforce** → verifica WIF + path contract automaticamente

### Componenti

```
.github/
├── actions/
│   ├── gcs-auth/action.yml          # WIF (legacy SA key come fallback)
│   ├── python-setup/action.yml      # (invariato)
│   ├── registry-update-pr/action.yml # (invariato)
│   └── python-ci/action.yml         # (invariato)
├── .github/workflows/
│   ├── pipeline-reusable.yml        # NUOVO: reusable workflow completo
│   ├── dataset-config-check-reusable.yml  # (invariato)
│   └── test-audit-reusable.yml      # (invariato)
└── scripts/
    └── drift_check.py               # AGGIORNATO: verifica WIF + paths
```

### Path contract

```python
# lab-connectors/lab_connectors/gcs/paths.py
CLEAN_BUCKET = "dataciviclab-clean"
MART_BUCKET = "dataciviclab-mart"

def clean_url(repo_slug, dataset_slug, year):
    return f"https://storage.googleapis.com/{CLEAN_BUCKET}/{repo_slug}/{dataset_slug}/{year}/"

def mart_url(repo_slug, dataset_slug, year):
    return f"https://storage.googleapis.com/{MART_BUCKET}/{repo_slug}/{dataset_slug}/{year}/"
```

## Piano di migrazione

### Fase 1 — WIF + path contract (1-2 settimane)

**Obiettivo:** eliminare le SA key, standardizzare le path GCS.

- [x] Setup GCP Workload Identity Pool + Provider
  - [x] Creare WIF Pool (`dataciviclab-pool`)
  - [x] Creare WIF Provider (`github-actions`)
  - [x] Creare 1 SA unica (`dcl-gcs-publisher`)
  - [x] IAM: SA → roles/storage.objectAdmin su `dataciviclab-clean` e `dataciviclab-mart`
  - [x] Binding: WIF Pool → workloadIdentityUser + serviceAccountTokenCreator sulla SA
- [x] Aggiornare `gcs-auth@main` per supportare WIF
  - [x] Fallback: se `GCP_WORKLOAD_IDENTITY_PROVIDER` è impostato → usa WIF
  - [x] Altrimenti → usa SA key (legacy, per transizione)
- [ ] Migrare 1 repo pilota (eurostat)
  - [ ] Aggiungere `id-token: write` nel workflow
  - [ ] Rimuovere `GCP_SA_KEY_EUROSTAT`
  - [ ] Testare sync su GCS
- [ ] Aggiornare `lab-connectors/gcs/paths.py` con path contract
- [ ] Migrare altri repo (ordine: open-conto-annuale → open-siope → gli altri)

**Eliminare dopo validazione:**
- [ ] `GCP_SA_KEY_EUROSTAT`
- [ ] `GCP_SA_KEY`
- [ ] `GCP_SA_KEY_SENATO_AKN`
- [ ] `GCP_SA_KEY_RNA`
- [ ] `GCP_SA_KEY_OPI`
- [ ] `GCP_SA_KEY_DPI`
- [ ] `GCP_SA_KEY_OPEN_POLITICA`
- [ ] `GCP_SA_KEY_DCL_BOLOGNA`

### Fase 2 — Reusable pipeline workflow (2-3 settimane)

**Obiettivo:** ogni repo ha ~15 righe di YAML, il logic vive in `.github`.

- [ ] Creare `pipeline-reusable.yml` in `.github/.github/workflows/`
- [ ] Aggiornare `project-template` con il pattern nuovo
- [ ] Migrare repo semplici (eurostat, open-conto-annuale, open-siope)
- [ ] Migrare repo complessi (open-politica, senato-akn, rna-aiuti-stato)
- [ ] Estendere drift-check per verificare l'uso del reusable

### Fase 3 — Cleanup (1 settimana)

- [ ] Eliminare SA key vecchie da GitHub
- [ ] Aggiornare drift-check per WIF + path contract
- [ ] Aggiornare documentazione (ADR, README, CONTRIBUTING)
- [ ] Verificare che tutti i repo siano conformi

### Fase 4 — Dashboard contract (futuro)

- [ ] lab-connectors espone path contract completo
- [ ] lab-dashboard e data-explorer migrano ai path ufficiali
- [ ] Eventuale trigger automatico (repository_dispatch)

## Note operative

### GCP Setup (da fare con accesso admin)

```bash
# 1. Crea WIF Pool
gcloud iam workload-identity-pools create dataciviclab-pool \
  --location=global \
  --display-name="DataCivicLab GitHub Actions"

# 2. Crea Provider
gcloud iam workload-identity-pools providers create-oidc github-actions \
  --workload-identity-pool=dataciviclab-pool \
  --location=global \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
  --attribute-condition="assertion.repository_owner == 'dataciviclab'" \
  --issuer-uri="https://token.actions.githubusercontent.com"

# 3. Crea SA
gcloud iam service-accounts create dcl-gcs-publisher \
  --display-name="DataCivicLab GCS Publisher"

# 4. IAM binding su SA (WIF può impersonare)
gcloud iam service-accounts add-iam-policy-binding dcl-gcs-publisher@PROJECT_ID \
  --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/PROJECT_NUM/locations/global/workloadIdentityPools/dataciviclab-pool/attribute.repository/*"

# 5. IAM binding: WIF può generare token per la SA
gcloud iam service-accounts add-iam-policy-binding dcl-gcs-publisher@PROJECT_ID \
  --role=roles/iam.serviceAccountTokenCreator \
  --member="principalSet://iam.googleapis.com/projects/PROJECT_NUM/locations/global/workloadIdentityPools/dataciviclab-pool/attribute.repository/*"

# 6. IAM binding su bucket (SA può scrivere)
gs iam ch serviceAccount:dcl-gcs-publisher@PROJECT_ID:objectAdmin \
  gs://dataciviclab-clean
gs iam ch serviceAccount:dcl-gcs-publisher@PROJECT_ID:objectAdmin \
  gs://dataciviclab-mart
```

### GitHub Secrets da configurare

```
ORGANIZATION-secrets:
  GCP_WORKLOAD_IDENTITY_PROVIDER: "projects/PROJECT_NUM/locations/global/workloadIdentityPools/dataciviclab-pool/providers/github-actions"
  GCP_SERVICE_ACCOUNT: "dcl-gcs-publisher@PROJECT_ID.iam.gserviceaccount.com"
```
