# DataCivicLab

DataCivicLab è uno spazio civico dove proviamo a rendere i dati pubblici italiani più leggibili, utili e condivisibili.

Nasce per chi vuole capire meglio il proprio territorio senza perdersi nel rumore, nei tecnicismi o nelle opinioni gridate.

**[Esplora i dati](https://explorer.dataciviclab.org/)** · **[Fai una domanda](https://github.com/orgs/dataciviclab/discussions/new?category=Domanda)** · **[dataciviclab.org](https://dataciviclab.org/)**

## Cosa puoi scoprire

Esempi di domande a cui cerchiamo di rispondere con dati verificabili, aperti e interrogabili:

- **Chi riceve i soldi pubblici?** — 17 milioni di aiuti alle imprese, bandi e appalti, progetti PNRR
  → [aiuti di Stato](https://explorer.dataciviclab.org/dataset/rna-aiuti-stato) · [bandi ANAC](https://explorer.dataciviclab.org/dataset/anac-bandi-gara) · [PNRR progetti](https://explorer.dataciviclab.org/dataset/pnrr-progetti)
- **Come sta messo il tuo territorio?** — spesa dei comuni, rifiuti, cementificazione, qualità dell'aria
  → [rifiuti urbani](https://explorer.dataciviclab.org/dataset/rifiuti-urbani) · [emissioni](https://explorer.dataciviclab.org/dataset/ispra-emissioni-ghg) · [IRPEF comunale](https://explorer.dataciviclab.org/dataset/irpef-comunale)
- **Quanto costa la sanità?** — spesa farmaceutica, posti letto, LEA regionali
  → [farmaceutica](https://explorer.dataciviclab.org/dataset/spesa-farmaceutica) · [LEA](https://explorer.dataciviclab.org/dataset/bdap-lea)
- **Come funziona il lavoro pubblico?** — stipendi, concorsi, pensioni
  → [dipendenti pubblici](https://explorer.dataciviclab.org/dataset/dipendenti-pubblici) · [pensioni INPS](https://explorer.dataciviclab.org/dataset/pensioni-inps)
- **Cosa decide il Parlamento?** — votazioni, attività in aula, elezioni dal 1948
  → [votazioni Camera](https://explorer.dataciviclab.org/dataset/votazioni-camera) · [elezioni](https://explorer.dataciviclab.org/dataset/elezioni-politiche)
- **E l'ambiente?** — consumo di suolo, emissioni, rinnovabili
  → [capacità rinnovabile](https://explorer.dataciviclab.org/dataset/capacita-rinnovabile)

Ogni dataset è pulito, documentato e pronto all'uso: [explorer.dataciviclab.org](https://explorer.dataciviclab.org/)

## Come funziona

Una domanda civica diventa dato pubblico in quattro passi:

1. **Chiedi** — apri una [domanda](https://github.com/orgs/dataciviclab/discussions/new?category=Domanda). Non serve saper programmare
2. **Verifichiamo** — se i dati esistono, dove stanno, se sono affidabili e abbastanza lunghi
3. **Prepariamo** — li mettiamo in forma pulita e documentata, con fonti e limiti dichiarati
4. **Pubblichiamo** — nell'[Explorer](https://explorer.dataciviclab.org/): serie storiche, download, interrogazione libera

Il percorso completo di un filone è descritto in [dataset-project-flow](https://github.com/dataciviclab/dataciviclab/blob/main/docs/dataset-project-flow.md).

## Partecipa

- **Hai una domanda sui dati pubblici?** — aprila in [Discussion](https://github.com/orgs/dataciviclab/discussions/new?category=Domanda). È il modo più semplice per iniziare
- **Conosci bene un settore** (giornalista, ricercatore, operatore)? — Commenta nelle [discussioni](https://github.com/orgs/dataciviclab/discussions): il contesto di dominio vale quanto il codice
- **Sai lavorare con i dati?** — guardale [issue con buon punto di ingresso](https://github.com/dataciviclab/dataciviclab/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22) e l'[Open Board](https://github.com/orgs/dataciviclab/projects/5). Ogni repository ha un `CONTRIBUTING.md`
- **Community** — [Discord](https://discord.gg/rAHpuTrYK3) · [LinkedIn](https://www.linkedin.com/company/dataciviclab/)

La traccia delle decisioni resta su GitHub.

## Per chi lavora con i dati

<details>
<summary>Mappa delle repo e architettura del Lab</summary>

Il percorso di un filone, dalla domanda all'output pubblico:

| Fase | Cosa fa | Repo |
|---|---|---|
| **Scouting** | Verifica delle fonti pubbliche, radar, monitoraggio | [`source-observatory`](https://github.com/dataciviclab/source-observatory) |
| **Incubazione** | Intake tecnico, contratto dataset, pipeline candidate | [`dataset-incubator`](https://github.com/dataciviclab/dataset-incubator) |
| **Motore** | RAW → CLEAN → MART, esecuzione delle pipeline | [`toolkit`](https://github.com/dataciviclab/toolkit) |
| **Catalogo** | Frontend pubblico sui dataset puliti | [`data-explorer`](https://github.com/dataciviclab/data-explorer) |
| **Analisi** | Hub pubblico, discussion, output con senso civico | [`dataciviclab`](https://github.com/dataciviclab/dataciviclab) |

Dati pubblicati per tema:

| Tema | Repo |
|---|---|
| **Spesa pubblica** | [`open-siope`](https://github.com/dataciviclab/open-siope) · [`partecipate-monitor`](https://github.com/dataciviclab/partecipate-monitor) · [`open-pnrr`](https://github.com/dataciviclab/open-pnrr) · [`open-coesione`](https://github.com/dataciviclab/open-coesione) |
| **Lavoro e welfare** | [`open-conto-annuale`](https://github.com/dataciviclab/open-conto-annuale) · [`open-inps`](https://github.com/dataciviclab/open-inps) · [`inpa-reclutamento`](https://github.com/dataciviclab/inpa-reclutamento) |
| **Economia e imprese** | [`rna-aiuti-stato`](https://github.com/dataciviclab/rna-aiuti-stato) · [`eurostat`](https://github.com/dataciviclab/eurostat) · [`imprese-italia`](https://github.com/dataciviclab/imprese-italia) |
| **Diritto e legislazione** | [`costituzione-italiana`](https://github.com/dataciviclab/costituzione-italiana) · [`italia-corpus`](https://github.com/dataciviclab/italia-corpus) · [`senato-akn`](https://github.com/dataciviclab/senato-akn) · [`giustizia-amministrativa`](https://github.com/dataciviclab/giustizia-amministrativa) |
| **Territorio e ambiente** | [`dcl-bologna`](https://github.com/dataciviclab/dcl-bologna) · [`open-ispra`](https://github.com/dataciviclab/open-ispra) · [`rifiuti-urbani`](https://github.com/dataciviclab/rifiuti-urbani) |

Setup locale, governance e regole di contributo: [dataciviclab.org/docs](https://dataciviclab.org/docs/) · [`.github/CONTRIBUTING.md`](https://github.com/dataciviclab/.github/blob/main/CONTRIBUTING.md)

</details>
