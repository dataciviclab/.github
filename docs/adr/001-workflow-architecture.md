# ADR-001: Architettura dei workflow CI/pipeline del Lab

**Status:** proposed (2026-08-16)

## Contesto

I workflow GitHub Actions sono distribuiti in ~15 repo e crescono con logica
e dialetti diversi. Evidenza raccolta a 2026-08-16:

- **Versioni action disallineate**: `actions/checkout@v4/v5/v6/v6.0.3/v7` e
  `actions/setup-python@v5/v6/v6.2.0/v7` mescolati tra repo.
- **Setup Python duplicato** con implementazioni diverse: 4 repo usano
  `dataciviclab/.github/actions/python-setup@main`, ma `lab-connectors` e
  `lab-dashboard` fanno `setup-python` + `pip install` inline.
- **Stesso passo reimplementato**:
  - blocco preflight dei `dataset.yml` in 4 repo (eurostat, open-siope,
    open-conto-annuale, dcl-bologna) con logiche simili ma eccezioni diverse;
  - blocco "registry → diff → draft PR" post-merge in eurostat e open-siope
    (~40 righe ciascuno);
  - blocco "auth GCS (JSON/base64) → gcloud" duplicato.
- **Migrazione incompleta**: `test-audit-reusable.yml` è adottato da 3 repo,
  ma `lab-connectors` ha ancora la copia inline.
- **Naming ambiguo**: `smoke-weekly.yml` significa cose diverse in
  `lab-connectors` (probe manifest GCS) e `dataset-incubator` (probe
  raggiungibilità fonti).
- **Soglie coverage arbitrarie**: 60/65/70/80/81 a seconda del repo.

Sintomo operativo: ogni modifica a un workflow rischia di "spaccare" o di
lasciare repo indietro (dimenticanze).

Alternative considerate:
- **Status quo** (logica in YAML, copie per-repo): non risolve drift e
  dimenticanze; ogni fix va replicato a mano in ogni repo.
- **Centralizzazione totale in `.github`** (workflow unico per tutti i repo):
  i workflow diventano un monolito con troppi input; le semantiche dataset
  (dipendenze SIOPE, codelist, bootstrap varchi) non sono esprimibili senza
  stravolgere il modello; perde visibilità e contesto per-repo.
- **Modello a 4 layer con delega** (scelta).

## Decisione

### 1. Modello a 4 layer

Dipendenza in una sola direzione, top-down:

```
YAML workflow      = ORCHESTRATORE   trigger, schedule, secrets, ambiente.
                                     Nessuna logica: chiama solo target make.
Makefile per-repo  = INTERFACCIA     target stabili (lint/test/pipeline),
                                     delega a comandi condivisi, zero logica.
Package org        = IMPLEMENTAZIONE toolkit, lab-connectors: CLI versionati
                                     e testati (toolkit run, registry build,
                                     preflight, verify).
.github            = COMPONENTI+REGOLE reusable workflow, composite action,
                                     drift-check che impone il modello.
```

### 2. Regola d'oro

1. **La logica non vive mai in YAML.** Passi >10 righe di shell → package org
   o script versionato.
2. **Stesso passo in 2+ repo → componente condiviso in `.github`**, non copia.
3. **Il Makefile non contiene logica**, solo delega a comandi condivisi.
4. **Locale == CI**: lo stesso comando `make` gira identico in locale e in CI;
   il workflow chiama i target Makefile invece di replicare i comandi.

### 3. Confine semantico

Le semantiche dataset (dipendenze tra dataset, support seed, verify
specifici) restano per-repo: vivono in `dataset.yml` (dati, già dichiarativi)
e nel `pipeline.yml` orchestratore ridotto all'osso.

Criterio: *se il passo è piattaforma → condiviso; se è specifico del dataset
→ per-repo*. Le eccezioni (es. `varchi-ztl` skip, dipendenze SIOPE) restano
nel repo come input/condizioni, non come codice duplicato.

### 4. Catalogo componenti `.github` (target)

| Componente | Tipo | Sostituisce |
|---|---|---|
| `python-setup` | composite action | setup Python (già adottato, estendere a lab-connectors, lab-dashboard) |
| `gcs-auth` | composite action | blocco auth GCS JSON/base64 |
| `ci-python-reusable` | reusable workflow | CI Python (ruff+mypy+pytest) |
| `dataset-config-check-reusable` | reusable workflow | blocchi preflight dei dataset |
| `registry-update-pr-reusable` | reusable workflow | blocco registry→diff→draft PR |
| `test-audit-reusable` | reusable workflow | già esistente; completare migrazione lab-connectors |

### 5. Versioni e pinning

`checkout`, `setup-python` e dipendenze stanno dentro i componenti condivisi,
non nei workflow per-repo → il drift versioni si risolve in un solo posto e
dependabot si configura solo nel `.github`.

I consumer restano su `@main` finché il `.github` ha review; tag semver
(`@v1`) sono evoluzione futura se la frequenza di cambio cresce.

### 6. Processo di cambiamento

1. La modifica condivisa atterra in `.github` (o nel package org), mai nel
   workflow di un singolo repo.
2. La CI di `.github` valida: actionlint + validate template + drift-check.
3. Il drift-check segnala i repo non migrati → issue + PR piccola per repo.
4. I repo nuovi nascono allineati via `project-template`.

### 7. Naming

Disambiguare `smoke-weekly` per scopo: `probe-weekly` (raggiungibilità fonti)
e `manifest-smoke-weekly` (catalog manifest GCS).

## Conseguenze

**Positive:**
- La logica vive una sola volta, versionata e testata nei package org → meno
  "si spacca quando cambiamo un workflow".
- Le dimenticanze diventano visibili: il drift-check le segnala invece di
  scoprirle per caso.
- Locale == CI: spariscono i bug "funziona in locale ma non in CI".
- I repo pipeline si leggono in ~15 righe di YAML + un Makefile.
- I repo nuovi (project-template) nascono conformi.

**Negative:**
- Indirezione iniziale: per capire un workflow serve seguire la catena
  YAML → Makefile → package.
- Costo di migrazione dei repo esistenti (da fare uno alla volta).
- Rischio over-engineering se si estraggono componenti per passi usati da un
  solo repo → la regola "2+ repo" è il gate.
- Rischio di Makefile per-repo che riproducono la stessa logica in dialetti
  diversi → mitigato dal drift-check che verifica anche i target Makefile.

## Implementazione

1. [x] Questo ADR — review in `.github`
2. [ ] `templates.yml` → drift-check (actionlint + verifica consumer dei
       reusable + disallineamento versioni action)
3. [ ] Migrare `lab-connectors` su `python-setup` + `test-audit-reusable`
4. [ ] Estrarre `ci-python-reusable` e migrare i CI Python (toolkit,
       lab-connectors, source-observatory, agent-context-builder,
       lab-dashboard)
5. [ ] Estrarre `dataset-config-check-reusable`, `gcs-auth`,
       `registry-update-pr-reusable` e migrare i repo dataset (eurostat,
       open-siope, open-conto-annuale, dcl-bologna)
6. [ ] Disambiguare `smoke-weekly`
7. [ ] Allineare `project-template` al modello
