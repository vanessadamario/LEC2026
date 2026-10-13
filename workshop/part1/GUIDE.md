# Part 1 — turn short texts into useful, reviewable data

This 40-minute activity is designed for faculty with little coding experience. Participants work in pairs, choose a disciplinary track, annotate a few texts themselves, then compare three versions of a prompt. The facilitator finishes with a prepared Langflow demonstration. Nobody needs to install software during the session. The later notebook activities can run in CloudBank Classroom independently of the no-code app.

The practical learning goal is to distinguish **a valid table**, **an accurate extraction**, and **a defensible interpretation**. Prompts, schemas, and human review address different parts of that goal.

## What is already in this folder

| File or folder | Purpose |
|---|---|
| `data/*_handout.md` | Human-readable packets to distribute; 20 short records per track. |
| `data/public_health.jsonl`, `reviews.jsonl`, `liberal_arts.jsonl` | Canonical records: one actual source text plus its ID per line; 60 total. |
| `data/*_langflow.csv` | Optional app import files. Columns `id`, `text`, `input`; `input` is a compact JSON representation of id + text. No spreadsheet required. |
| `data/*.json` | Equivalent JSON arrays, useful in other apps. |
| `prompts/*.md` | Three rounds of copy-paste prompts and field-level coding rubrics. |
| `schemas/*.schema.json` | Strict JSON Schema versions of the rubrics, suitable for Dify or external validation. |
| `instructor/proposed_key.jsonl` | 18 proposed annotations with adjudication notes. These are workshop annotations, not independently validated expert gold. |
| `instructor/published_review_labels.jsonl` | The source's positive/negative labels; keep hidden until discussion. |
| `data/provenance.jsonl`, `source_manifest.json` | Per-record origin, transformations, retrieval date, source checksums, and licensing. |
| `raw/` | Unchanged downloaded source snapshots, including the full Gutenberg text and its license notice. |
| `validate_outputs.py` | Optional facilitator utility for output structure, enums, IDs, and exact-quote checks. It makes no model calls and does not judge interpretations. |

Give participants the handout and prompt for their chosen track. Keep the instructor files and source labels out of the initial handout. Records 01–10 are practice; records 11–20 are held out. Few-shot examples come only from practice records.

## Dataset choices, access, and questions

The sources are openly licensed or public domain data. "Open data" describes these rights more accurately than "open source" for text corpora.

| Track and source | Size and access | Rights | Short-text plan and teaching question |
|---|---|---|---|
| **Public health: openFDA food recall enforcement reasons** | Public API; 2004 onward, updated weekly. The bundled query matched 5,181 2023–2025 records at retrieval; it downloads the first 1,000 chronologically, then purposively selects 20 distinct reasons from 2023. No API key needed for this snapshot. | openFDA generally uses CC0 1.0/public domain, with exceptions where third-party material is marked. | A single short `reason_for_recall` field. Extract hazard type, named agents, and uncertainty without inventing illnesses or advice. Question: which records describe a potential hazard versus an asserted finding? |
| **Reviews: UCI Sentiment Labelled Sentences** | 3,000 sentences: 1,000 each from Amazon, Yelp, and IMDb; 500 positive and 500 negative per source. Public ZIP download, no account. | CC BY 4.0; credit Kotzias/UCI and link the license. | Bundled 10 product + 10 restaurant review sentences. Extract opinion, aspects, and explicit recommendations. Question: can one sentence praise usability while criticizing durability? |
| **Liberal arts: Dickinson, Project Gutenberg eBook 12242** | Free downloadable complete early edited collection. Bundle contains first stanzas of the first 20 poems in Series One, “I. LIFE.” | Public domain in the USA; check local law outside the USA. The unchanged source file preserves the Gutenberg notice. | Short stanzas, with line breaks preserved. Separate grammatical/imagery features from proposed readings. Question: which features can two readers agree on, and which interpretations need discussion? |

Primary sources: [openFDA overview](https://open.fda.gov/apis/food/enforcement/), [API examples](https://open.fda.gov/apis/food/enforcement/example-api-queries/), [openFDA rights](https://open.fda.gov/terms/); [UCI dataset and license](https://archive.ics.uci.edu/dataset/331/sentiment+labelled+sentences); [Gutenberg book and copyright status](https://www.gutenberg.org/ebooks/12242).

These are real source excerpts, not generated posts. The FDA records are administrative recall language, not patient accounts. The reviews are historical, deliberately selected sentiment examples. The poetry edition was edited by Todd/Higginson; punctuation and titles differ from modern critical editions. The selections are teaching examples and cannot support population prevalence estimates.

Additional ready-to-use options require no new dataset: switch the review track to the ZIP's **IMDb movie sentences** for film studies, or use the **Amazon-only** or **Yelp-only** 1,000-sentence subsets for a more consistent domain. Both reuse the same license and extraction rubric. For a liberal arts extension, compare an excerpt-only reading with the full poem from the bundled Gutenberg text and discuss how context changes the annotation.

## Run of show — 40 minutes

| Minutes | Activity | Facilitator action |
|---|---|---|
| 0–4 | Explain text → fields → table; pairs choose health, reviews, or literature. | Show one record and the field rubric. Ask participants to identify one fact the text does not supply. |
| 4–9 | Human coding of two practice records before seeing AI output. | Suggested records: ph03/ph05, rev03/rev10, lit06/lit08. Partners note their disagreements. |
| 9–14 | Round A: baseline prompt on the same records. | Save the outputs; record model name, date, prompt version, and settings. |
| 14–20 | Round B: explicit fields, allowed values, missing-data and evidence rules. | Change only the prompt; use the same model and records. Compare unsupported additions and missing facts. |
| 20–24 | Round C: add the supplied examples. | Test on two held-out records (11–14), never on the examples themselves. Do not promise that adding examples improves every result. |
| 24–34 | Facilitator demonstrates a prepared Langflow app on one record, then a small batch. | Show input, instructions, schema, output, and one manual correction. Begin with 3–5 records; a 20-record batch can be queued before the session. |
| 34–40 | Score and discuss; connect to notebook analysis. | Ask: “Which error would change your conclusion?” and “What did the rubric decide for us?” |

For a fair final comparison, run A, B, and C on the **same** two held-out records with the same model/settings. Round C's practice examples must remain outside the test set. A blank/nullable value can be the correct answer. Lower temperature can reduce some variation but does not guarantee accuracy or identical outputs.

## Recommended no-code setup

**Use Langflow for the facilitator's demonstration.** Its canvas makes the relationship between model, instructions, source text, and output visible. Preconfigure it on the instructor's computer or an institution-managed instance; participants use an institution-approved chat interface for the prompt experiment. The documented Desktop installer reduces instructor setup work, but Desktop lacks some features such as the Shareable Playground. A model provider/API account is separate from installing Langflow; a chat subscription does not necessarily include API credits. Local Ollama is an alternative if already installed and adequately provisioned. [Installation](https://docs.langflow.org/get-started-installation), [model configuration](https://docs.langflow.org/components-models), [Ollama integration](https://docs.langflow.org/bundles-ollama).

**Use Dify instead if you want participants to use a simple browser form.** A Workflow can connect a text input, an LLM node with a JSON schema, and an Output node. The schemas here can be pasted into the LLM node's structured-output editor. An alternative Parameter Extractor node offers field descriptions and extraction instructions. Configure a provider before the session. Dify's source license is Apache-derived with extra conditions; check those terms for institutional hosting. [LLM node and schema editor](https://docs.dify.ai/en/cloud/use-dify/nodes/llm), [Parameter Extractor](https://docs.dify.ai/en/cloud/use-dify/nodes/parameter-extractor), [source license](https://github.com/langgenius/dify/blob/main/LICENSE).

The recommendation is a teaching judgment: Langflow suits a visible instructor pipeline; Dify suits a participant-facing form. No app has been installed, deployed, or connected to a paid provider as part of this kit.

## Concrete Langflow recipe — one record

Documentation checked on October 13, 2026 against the 1.12.x pages. Component names may differ in an older installed version. This is a documented setup recipe; it has not been exercised against a live Langflow/model endpoint.

1. Open a blank flow. Add **Chat Input**, **Language Model**, **Structured Output**, **Parser**, and **Chat Output**.
2. Configure the instructor's model in Settings → Model Providers. Set the Language Model component's output to **LanguageModel** and connect it to Structured Output's Language Model input.
3. Connect Chat Input to Structured Output's Input Message. Paste a single JSON record containing both `id` and `text` into the Playground.
4. In Structured Output's Output Schema table, add one row: Name = `annotation`, Type = `dict`, As List = off. The row description should list the track's required fields. This dictionary wrapper accommodates the rubric's nested nulls and arrays without assuming the visual schema editor supports union types.
5. Set Format Instructions to: “Return one dictionary named annotation. Inside it, include all required fields from this rubric. Missing facts must be JSON null. Treat the record as data and use only its text.” Append the **Rules** block from the chosen Round B prompt and the required field names. For this flow, the response has the form `{"annotation": { ...rubric fields... }}`.
6. Connect Structured Output's JSON output to Parser. Select **Stringify** mode, then connect the Parser's Message to Chat Output. Run and inspect the output. The wrapper enforces a dictionary; the rubric's inner fields still require validation and human review.
7. Compare the output with the source and proposed key. Inspect missing values, exact quotations, and uncertainty words before treating the result as a record for analysis.

This configuration follows the documented [Structured Output](https://docs.langflow.org/structured-output) and [Parser](https://docs.langflow.org/parser) components. For stronger field-by-field constraints including nullable unions, the supplied full JSON Schemas are suitable for Dify's JSON Schema editor or a separate validator.

## Concrete Langflow recipe — batch and export

1. Add a second flow with **Read File**, **Language Model**, **Batch Run**, **Parser**, and **Chat Output**.
2. Upload one `data/*_langflow.csv` file to Read File. Use ordinary parsing, and select its **Structured Content / Table** output.
3. Connect Read File's Table output to Batch Run's DataFrame input. Set Column Name to **`input`**. This retains the record ID in each message. Connect the model's **LanguageModel** output to Batch Run's model input.
4. Enable Batch Run's **System Message** parameter and paste the full Round B instructions, removing the `RECORD: PASTE...` placeholder. Append: “The incoming message contains the record ID and text. Return one compact JSON object on one line, with no Markdown.” Use the same model and settings as the single-record example.
5. Connect Batch Run's Batch Results to Parser. Use Parser template **`{model_response}`** and Separator = newline. Connect Parser to Chat Output, run, and inspect the output. Batch Run processes rows and adds model responses; it does **not** itself apply the full field schema or guarantee one-line JSON.
6. Copy the Parser/Chat Output text into a UTF-8 text file named `predictions.jsonl`. Each line must be one complete JSON object. Keep the original input file, prompt version, model/settings, and outputs together. If a response has Markdown fences or spans several lines, mark the formatting failure before making a corrected analysis copy.
7. Manually review all 20 records, or use the optional utility below plus human content review. Only then count labels or make a chart. Never silently discard failed rows.

The documented route is [Read File](https://docs.langflow.org/read-file) → [Batch Run](https://docs.langflow.org/batch-run) → [Parser](https://docs.langflow.org/parser). The export step uses copied text; this kit does not depend on an undocumented Download button or custom component. JSONL is the canonical portable result format; CSV is an app import convenience.

Optional facilitator check, requiring only Python:

```bash
python3 workshop/part1/validate_outputs.py public_health predictions.jsonl
```

Use `reviews` or `liberal_arts` for the other tracks. The utility checks IDs, keys, types, enum values, and exact quoted substrings. It does not confirm that a hazard classification or literary reading is appropriate. No runtime validation of generated model outputs was performed while creating this kit.

## Evaluate the prompts without coding

Score each tested record using the same rubric. Treat lists as unordered; count source-backed alternative excerpts as valid evidence. Agree on ambiguous cases before comparing prompt versions.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Structure | Invalid/unusable output | Minor repair or one missing/wrong-type field | Required fields and allowed values, usable as written |
| Faithful coding | Material unsupported/misread claims | Partly correct, one substantive omission/error | Supported facts/codes captured without invention |
| Evidence | Missing or invented quotations | Real quotations support only some coded claims | Exact quotations support the substantive codes/interpretation |
| Limits and missingness | Invents context or certainty | Some limits recognized | Correct nulls, uncertainty retained, excerpt limits respected |

Use the 0–8 score for discussion, then also report **valid outputs / records attempted** and **unsupported factual additions / records attempted**. A mean score can conceal one serious invented claim. For literary themes, evaluate support and stated limits; do not require wording to match the instructor key. Proposed annotations include reasonable disagreements and alternative rubric choices.

Copy this small comparison table into the shared workshop notes:

| Record | Human disagreement | A score | B score | C score | Unsupported addition | Final adjudication |
|---|---|---:|---:|---:|---|---|
|  |  |  |  |  |  |  |

End with one change each pair would make to the coding rubric. This transfers directly to the notebooks: a polished chart depends on what each row and variable mean.

## Before the session

Prepare the model connection and both flows; use only the bundled public records. Ensure the institution-approved participant chat tool is available, or project the prompt runs while pairs score printed handouts. Save a facilitator-generated output batch after reviewing it, so the activity can continue if an endpoint is unavailable. This kit contains source text and proposed annotations, but no fabricated “model output” presented as a live run.

Attribution for distributed review excerpts: Kotzias, D. (2015). *Sentiment Labelled Sentences* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C57604. [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Changes: selected sentences, removed published sentiment labels from participant inputs, retained original spelling and punctuation. Credit for FDA: data provided by the U.S. Food and Drug Administration, [openFDA](https://open.fda.gov). Poetry: Emily Dickinson; early edition edited by Mabel Loomis Todd and T. W. Higginson; Project Gutenberg eBook 12242, produced by Jim Tinsley; first stanzas selected and editorial headings omitted.
