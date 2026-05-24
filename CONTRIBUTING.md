# Contributing

Grazie per voler contribuire a DataCivicLab.

Questa guida serve a orientarti senza farti studiare tutto prima.

Il Lab e' aperto, ma non caotico.
C'e' un posto giusto per ogni cosa.

## Da dove partire

Se vuoi capire il quadro generale, parti dalla repository `dataciviclab`.

Se vuoi contribuire all'organizzazione nel suo insieme:

- parti dalle [Discussions](https://github.com/orgs/dataciviclab/discussions) dell'org
- guarda [Open Board](https://github.com/orgs/dataciviclab/projects/5) per il lavoro in corso
- guarda [Roadmap](https://github.com/orgs/dataciviclab/projects/2) per capire direzione, progetti e milestone

Se invece vuoi contribuire a un repository specifico, usa questa regola semplice:

- [`dataciviclab`](https://github.com/dataciviclab/dataciviclab): hub pubblico — sito, analisi, documenti, discussioni
- [`source-observatory`](https://github.com/dataciviclab/source-observatory): scouting e monitoraggio delle fonti pubbliche
- [`dataset-incubator`](https://github.com/dataciviclab/dataset-incubator): intake tecnico — candidate, pipeline, contratto dati
- [`toolkit`](https://github.com/dataciviclab/toolkit): motore RAW → CLEAN → MART
- [`data-explorer`](https://github.com/dataciviclab/data-explorer): catalogo pubblico dei dataset puliti
- [`lab-dashboard`](https://github.com/dataciviclab/lab-dashboard): dashboard operativa — metriche, fonti, pipeline
- [`lab-connectors`](https://github.com/dataciviclab/lab-connectors): package Python condiviso (HTTP, GCS, MCP, DuckDB)
- [`agent-context-builder`](https://github.com/dataciviclab/agent-context-builder): contesto operativo per agenti AI del Lab
- `.github`: policy condivise, template, codice di condotta, profilo pubblico

In ogni caso:

- leggi il `README.md` del repository e il suo `CONTRIBUTING.md`
- controlla issue e discussions aperte
- per la guida completa su come contribuire al Lab, vedi [`docs/come-contribuire.md`](https://github.com/dataciviclab/dataciviclab/blob/main/docs/come-contribuire.md) in `dataciviclab`

Non serve essere esperti del motore per partecipare.
Puoi anche partire da una domanda, da una correzione piccola o da un problema ben descritto.

## Flusso minimo

Nell'organizzazione usiamo un flusso semplice:

1. apri o trovi una Discussion se serve chiarire il contesto
2. apri o prendi in carico una Issue quando il lavoro e' definito
3. proponi il cambiamento con una Pull Request

Le issue servono a rendere il lavoro visibile.
Le pull request servono a far entrare i cambiamenti in modo chiaro e revisionabile.

## Cosa usare e quando

- `Discussions`: domande, idee, confronto iniziale, orientamento
- `Issues`: lavoro concreto da fare o problema da risolvere
- `Pull requests`: proposta di modifica pronta da rivedere
- `Open Board`: vista pubblica del lavoro in corso
- `Roadmap`: vista pubblica di direzione, progetti e prossime tappe
- `Discord`: scambio veloce o informale, non traccia canonica

GitHub resta il posto dove deve restare la traccia utile.

GitHub Projects puo' essere usato dai maintainer per organizzare il lavoro, ma non sostituisce issue e pull request come traccia pubblica.

## Prima di aprire una PR

- controlla se esiste gia' una issue o discussion collegata
- tieni il cambiamento piccolo e leggibile
- spiega il perche', non solo il cosa
- se la modifica e' specifica di un repo, segui le regole di quel repo

## Confini di questa repo

La repository `.github` definisce il layer comune GitHub dell'organizzazione.
Non descrive il metodo dati, la pipeline tecnica o la struttura operativa dei repository dataset.

Per quei contenuti, fai riferimento ai repository dedicati.

## Per approfondire

- [`dataciviclab/docs/come-contribuire.md`](https://github.com/dataciviclab/dataciviclab/blob/main/docs/come-contribuire.md) — guida completa per nuovi contributor
- [`dataciviclab/docs/dataset-project-flow.md`](https://github.com/dataciviclab/dataciviclab/blob/main/docs/dataset-project-flow.md) — il flusso del Lab dalla domanda all'analisi
- [`dataciviclab/docs/governance-model.md`](https://github.com/dataciviclab/dataciviclab/blob/main/docs/governance-model.md) — ruoli e come si decide
