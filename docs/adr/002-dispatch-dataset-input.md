# ADR-002: Input di dispatch per selezionare i dataset

**Status:** accepted (2026-11-04)

## Contesto

I workflow di pipeline dei repo dati espongono un input `workflow_dispatch` per
lanciare la pipeline su un sottoinsieme di dataset. A 2026-11-04 le convenzioni
sono **tre diverse su quattro workflow**:

| repo | input | valore | multipli | vuoto |
|---|---|---|---|---|
| `open-politica` | `dataset` | slug **o** path | no | = tutti |
| `open-mur` | `dataset` | **path** config | no | = tutti |
| `dcl-bologna` | `datasets` | slug | **sì, virgola** | = tutti |
| `dataset-incubator` | `slug` | slug (cartella) | no | = nessuno |

L'action condivisa `detect-changed-datasets` espone `slug-input`, usato **solo**
da `dataset-incubator`.

**Sintomo operativo.** Con un dispatch per dataset, `dataset-incubator` produce N
registry PR sullo stesso branch (`post-merge-registry/schedule-registry`) che si
sovrascrivono: il registry si costruisce dagli **artifact locali del run**, quindi
ogni run registra solo il proprio dataset. Dispatchare N volte non dà N dataset.

Alternative considerate:
- **Status quo** (un input diverso per repo): ogni automazione cross-repo deve
  conoscere il dialetto del repo; il bug del registry resta.
- **Un input per dataset, un run per dataset**: non risolvibile — il registry
  richiede che tutti gli artifact siano presenti nello stesso run.
- **Convenzione unica, normalizzata nell'action** (scelta).

## Decisione

Un solo input di dispatch per selezionare i dataset:

```
nome:    datasets
valore:  uno o più slug separati da virgola (spazi tollerati)
         ogni voce è lo slug della cartella (es. mase-gas-import)
         oppure il path del config (es. datasets/laureati/dataset.yml)
vuoto:   a discrezione del repo, documentato nella description dell'input
```

- **`datasets`** (plurale): l'input accetta una lista, e `dcl-bologna` lo usa già così.
- **virgola**: separatore già in uso in `dcl-bologna`; meno fragile dello spazio
  in un campo di testo GitHub.
- **slug o path**: entrambi accettati, così i repo che oggi passano un path
  (`open-mur`, `open-politica`) non cambiano il contratto d'uso.
- **normalizzazione nell'action**: `detect-changed-datasets` converte la virgola
  in spazio e risolve slug o path. Nessun consumatore reimplementa la logica.
- **vuoto**: non è parte della convenzione. Per i repo mono-dominio "tutti" è
  ragionevole; per `dataset-incubator` no (45 candidate) → "nessuno".

## Conseguenze

- `dataciviclab/.github`: input `slug-input` → `datasets` + normalizzazione.
- `dataset-incubator`: `slug` → `datasets` (bloccante: è il caso che ha motivato l'ADR).
- `open-politica`, `open-mur`: `dataset` → `datasets` (rinomina, comportamento invariato).
- `dcl-bologna`: `datasets` già conforme, aggiungere la tolleranza degli spazi.
- Retro-compatibile: una voce singola è una lista di uno.
- Un dispatch può processare più dataset in un run → un solo registry PR.

## Riferimenti

- `actions/detect-changed-datasets/action.yml`
- `dataset-incubator/.github/workflows/post-merge-candidate.yml`
- ADR-001 (architettura workflow)
