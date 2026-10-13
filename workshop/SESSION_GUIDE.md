# Faculty workshop: ask, inspect, and build with AI

**90 minutes · CloudBank Classroom · little or no coding experience**

Faculty practice turning a disciplinary question into an explicit instruction, checking the answer, and using AI to modify a small analysis tool. The first part is hands-on prompting; the second and third parts are instructor demonstrations with audience predictions and interpretation.

By the end, participants should be able to specify an extraction rubric, identify unsupported model output, distinguish an analysis result from its interpretation, and explain the difference between a downloaded model and a remotely hosted tool.

## Recommended structure

| Minutes | Activity | Audience action | Concrete output |
|---|---|---|---|
| 0–5 | Frame the session with one ambiguous text | Predict what information can actually be extracted | Shared distinction between stated, inferred, and missing |
| 5–25 | Part 1: three prompt rounds in small disciplinary groups | Apply baseline, rubric-based, and few-shot prompts to the same held-out records | Three outputs and a scored comparison |
| 25–40 | Part 1 app demo: text → JSON → validated table | Find one extraction error and explain its source | Small structured dataset with source evidence |
| 40–49 | Part 2 demo: human biology | Predict how a plot/filter changes an association | Interactive scatterplot tool |
| 49–58 | Part 2 demo: oceanography | Compare profiles and notice incomplete coverage | Interactive profile viewer |
| 58–67 | Part 2 demo: microscopy | Predict a threshold/seed change, then inspect the overlay | Interactive segmentation and measurement tool |
| 67–82 | Part 3 demo: Hugging Face | Contrast rubric labels with model labels; observe a tool call | Local sentiment function and optional Space API call |
| 82–90 | Reflection and exit ticket | Name a course use, a needed validation, and one limitation | Personal adaptation plan |

If you prefer two parts, put the Hugging Face demo at the end of Part 2. The time allocation is unchanged. Use selected cells for each nine-minute science demo; the complete notebooks contain deeper analysis for later exploration.

## Part 1: short unstructured text to structured information

Use three groups or let faculty choose a domain. The kit bundles **20 real examples per domain**, with source provenance and held-back metadata/annotations. This is a deliberately selected teaching sample, not a representative research sample.

| Domain / candidate | What makes it useful | Extraction fields | License and access |
|---|---|---|---|
| Public health: openFDA food recall reasons | Short hazard descriptions; uncertainty and missing consumer instructions are visible | Named product, hazard types/agents, assertion strength, illness count, stated action, exact evidence | CC0/public domain unless marked otherwise; [FDA food enforcement API](https://open.fda.gov/apis/food/enforcement/), [openFDA terms](https://open.fda.gov/terms/). Sample uses administrative recall-reason text. |
| Reviews: UCI Sentiment Labelled Sentences | Short product, restaurant, and film opinions; negation and implicit targets | Sentiment, explicitly named target, evaluated aspects, recommendation, evidence | CC BY 4.0; [UCI dataset](https://archive.ics.uci.edu/dataset/331/sentiment+labelled+sentences). 3,000 original labelled sentences. |
| Liberal arts: Emily Dickinson poems/stanzas | Short literary text with line breaks; interpretation needs explicit textual support | Grammatical person, coded imagery, proposed theme, theme evidence, alternative reading, context limits | Public-domain edition in the United States; [Project Gutenberg 12242](https://www.gutenberg.org/ebooks/12242). Preserve the edition's license and check local copyright rules if used elsewhere. |

For additional candidate datasets and alternatives, use the [Part 1 guide](part1/GUIDE.md). The fixed field-level rubrics and ready-to-copy prompts are in [public health](part1/prompts/public_health.md), [reviews](part1/prompts/reviews.md), and [liberal arts](part1/prompts/liberal_arts.md). Give participants the appropriate `part1/data/*_handout.md`, not the instructor labels/provenance.

Run three rounds while holding the model and test records constant:

1. **Baseline:** request the fields with minimal guidance.
2. **Rubric:** define allowed categories, missing-value behavior, evidence, and the JSON shape.
3. **Few-shot:** add one ordinary example and one ambiguous/missing-information example. These examples must be different from the evaluation records.

Evaluate JSON validity separately from semantic quality. A valid JSON object can still contain an invented fact. Have pairs code the held-out texts before examining the proposed instructor annotations. Use the included scoring rubric to assess field correctness, appropriate nulls, and source-supported evidence. Do not treat the model's stated confidence as evidence of accuracy.

**Facilitation question:** “What did you have to define that an expert reader usually leaves implicit?” The skill participants practice is making disciplinary judgment explicit, not writing a longer prompt for its own sake.

## No-code workflow recommendation

**Use Langflow for the instructor demonstration.** Its visible components make the transformation easy to explain, and its Structured Output component supports field-oriented extraction. Preconfigure the flow and provider before class. Participants can concentrate on their prompts through an approved chat interface, then see how the same rubric becomes an app. [Langflow structured output documentation](https://docs.langflow.org/structured-output).

Show one record with a schema wrapper before introducing a batch; the nested rubric fields still require validation. Then use the CSV import and batch workflow from [Part 1](part1/GUIDE.md). Preserve record IDs and original text, validate each response, inspect unsupported evidence, and export only reviewed rows. Batch prompting alone does not guarantee schema compliance or factual correctness. [Langflow Batch Run documentation](https://docs.langflow.org/batch-run).

| Tool | When I would choose it | Workshop tradeoff |
|---|---|---|
| Langflow | You want the audience to see how a flow connects text, prompts, model, and outputs | Good facilitator demo; installation, provider configuration, and batch parsing need preparation |
| Dify | You want a shared browser form with structured output from an LLM workflow | Useful app experience; deployment and provider setup still required, and its license includes additional conditions |
| Existing approved chat interface | You want all faculty experimenting immediately | Least setup for prompting; batch processing and validation are separate steps |

[Dify structured outputs](https://docs.dify.ai/en/cloud/use-dify/nodes/llm) · [Dify license](https://github.com/langgenius/dify/blob/main/LICENSE).

## Part 2: research and teaching questions, with notebooks

| Dataset | Questions worth asking | Notebook tool / analysis | Key interpretation check |
|---|---|---|---|
| UCI Heart Disease, processed Cleveland: 303 historical clinical records | How do age, resting blood pressure, and cholesterol vary? Does a cholesterol group comparison change across age bands? | Missingness, distributions, descriptive comparison, bootstrap interval, and adjustable scatterplot | Clinical selection and confounding limit generalization; association is not causation. Main documented units are years, mm Hg, and mg/dL. |
| CCHDO GO-SHIP P02W 2022: 682 pressure levels across three selected casts | How do temperature and salinity vary down the profile? How do QC policy and unequal coverage affect comparisons? | QC filtering, inverted-pressure profile charts, common-band summaries, adjustable viewer | Pressure is dbar, not measured depth; practical salinity is dimensionless. Three casts at different locations/dates cannot show a temporal climate trend. |
| scikit-image human_mitosis: one 512×512 fluorescence field | How does segmentation depend on threshold and seed spacing? Which bright regions are merged or split? | Otsu threshold, watershed, region measurements, sensitivity table, sliders, overlay | Unvalidated segmented objects are not verified cell counts; no pixel-size calibration or reference mask is supplied. |

Sources: [UCI Heart Disease](https://archive.ics.uci.edu/dataset/45/heart+disease), [CCHDO cruise](https://cchdo.ucsd.edu/cruise/33RR20220430), [NOAA CTD metadata and CC0 declaration](https://data.pmel.noaa.gov/generic/erddap/info/cchdo_ctd/index.html), [scikit-image image provenance and CC0](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.human_mitosis).

Additional candidates, with their own questions and implementation caveats:

| Domain | Backup candidate | Possible question | Status |
|---|---|---|---|
| Human biology | [UCI Heart Failure Clinical Records](https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records), 299 observations, CC BY 4.0 | How do ejection fraction and serum creatinine vary or covary across age groups? | Researched candidate; not implemented |
| Oceanography | [NOAA OISST v2.1](https://www.ncei.noaa.gov/products/optimum-interpolation-sst) | How does daily SST at one location vary over a season, and how does an anomaly differ from absolute temperature? | Researched candidate; subset/cache needed |
| Oceanography | [Argo](https://argo.ucsd.edu/data/) | How do successive temperature/salinity profiles differ, considering float movement and QC? | Researched candidate; select float/cycles and retain scientific acknowledgement |
| Microscopy | [BloodMNIST](https://medmnist.com/), 17,092 images, eight categories, CC BY 4.0 | Which blood-cell categories are most often confused by a classifier? | Researched candidate; use official data and preserve benchmark splits |
| Microscopy | [Quantitative phase cell image](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.cell), CC0 | How do physical pixel calibration and background artifacts affect a cell-area estimate? | Researched candidate; one calibrated image |

Detailed source/license notes: [human biology](notebooks/01_human_biology_sources.md), [oceanography](notes/02_oceanography_sources.md), [microscopy](notes/03_microscopy_sources.md). The three primary candidates have complete notebooks; backups are suggestions for adaptation.

### Nine-minute demo pattern

Use the same pattern each time: question → inspect source → predict → run tool → verify → suggest one AI modification.

- **Human biology:** show units and missingness, then the `explore` scatterplot function and age-range controls. Ask whether changing the age range changes the answer. Use the prewritten AI prompt to change one plot feature; the full bootstrap/stratification analysis is available for later discussion.
- **Oceanography:** show the three source profiles, point out the short cast, then use `plot_profile` to change station, variable, and QC policy. Ask why extrapolation or treating all pressure levels as independent replicates would mislead.
- **Microscopy:** show the source and overlay, then change the threshold and seed spacing one at a time. Ask which biological objects participants intend to measure before interpreting the output count.

Use this shared prompt when demonstrating an AI code change:

```text
I teach [discipline] and have little Python experience. Here is the current
analysis function and its data dictionary. Add [one specified control or plot].
Keep the source data, units, missing-value policy, and scientific assumptions
unchanged. Return one replacement notebook cell. Explain what changed and
give me two observable checks I can make on its output. Ask if you need
information the data dictionary does not contain.
```

Compare the returned cell with the original, then inspect the chart and counts. An AI-generated code cell needs the same scientific checks as code written by a person. Faculty supply the question, definitions, and interpretation; the assistant helps implement the tool.

## Part 3: Hugging Face models and hosted tools

Open [04_huggingface_tools.ipynb](notebooks/04_huggingface_tools.ipynb). The main demo loads the Apache 2.0 DistilBERT SST-2 sentiment model and wraps it in `classify_review`. Its binary output deliberately conflicts with the four-category review rubric's neutral/mixed cases. Discuss why a task-specific model does not automatically implement a custom extraction rubric. [Model card](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english).

The model runs in the CloudBank notebook process after the weights are downloaded. The optional Gradio client section calls the public `gradio/calculator` Space, illustrating a hosted callable tool. It sends only simple numbers, shows how to inspect the current API, and has a bounded result wait. [Official Gradio client guide](https://gradio.app/guides/getting-started-with-the-python-client).

Before adopting a model for a course, faculty should examine its intended task, license, language/domain, output labels, evaluation evidence, hardware requirements, and limitations. For microscopy, use a modality-appropriate model and reference masks; a generic visual model's plausible answer is not a segmentation validation.

## Minimal slide outline

1. Workshop question: “What can I ask AI to do, and how will I check it?”
2. One text, several plausible interpretations: why a rubric matters.
3. Prompt ingredients: task, context, definitions, output form, missing-value rules, examples.
4. Activity instructions and three disciplinary tracks.
5. Comparison: what changed from baseline to rubric to examples?
6. Live Langflow: text to a reviewed structured table.
7. From a research question to a transparent notebook tool.
8. Three brief notebook demonstrations and their interpretation checks.
9. Hugging Face: model weights, a local function, and a remotely hosted tool.
10. Exit ticket: one course use, one validation, one limitation.

## Participant exit ticket

“In my course, I could use AI to ____. I would give it this definition/rubric: ____. Before trusting the output I would check ____. A limitation students should understand is ____.”

Creation status and classroom preparation are documented in [README.md](README.md) and [CLOUDBANK_SETUP.md](CLOUDBANK_SETUP.md). Live execution testing is deferred to you as requested.
