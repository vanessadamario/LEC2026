"""Rebuild the classroom subsets from the bundled, unchanged source snapshots.

Standard library only. Run from any working directory. No model/API calls.
"""
import csv
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
(ROOT / "instructor").mkdir(exist_ok=True)


def jsonl(path, rows):
    path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows), encoding="utf-8")


def emit(name, rows):
    jsonl(DATA / (name + ".jsonl"), rows)
    (DATA / (name + ".json")).write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # CSV is an optional Langflow import format, not a spreadsheet requirement.
    with (DATA / (name + "_langflow.csv")).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "text", "input"])
        writer.writeheader()
        writer.writerows(dict(row, input=json.dumps(row, ensure_ascii=False)) for row in rows)
    credits = {
        "public_health": "Source: U.S. Food and Drug Administration, openFDA food enforcement records (https://open.fda.gov/apis/food/enforcement/). CC0/public domain subject to marked third-party exceptions (https://open.fda.gov/terms/). Selected reason_for_recall excerpts; no wording changes.",
        "reviews": "Source: Kotzias, D. (2015). Sentiment Labelled Sentences [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C57604. CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Changes: selected review sentences; source sentiment labels omitted; original spelling and punctuation retained.",
        "liberal_arts": "Source: Emily Dickinson, Poems by Emily Dickinson, Three Series, Complete; early edition edited by Mabel Loomis Todd and T. W. Higginson; Project Gutenberg eBook 12242 (https://www.gutenberg.org/ebooks/12242), produced by Jim Tinsley. Public domain in the USA; check local law outside the USA. First stanzas selected; editorial headings omitted. Full Gutenberg notice retained in the bundled raw source.",
    }
    # Copy-paste packet: no coding or JSON knowledge needed.
    (DATA / (name + "_handout.md")).write_text(
        "# " + name.replace("_", " ").title() + "\n\n"
        + "Records 01–10 are practice; records 11–20 are the held-out challenge. "
        + "Preserve the record ID when submitting an answer.\n\n"
        + credits[name] + "\n\n"
        + "\n\n".join("## " + r["id"] + "\n\n```text\n" + r["text"] + "\n```" for r in rows) + "\n",
        encoding="utf-8",
    )


provenance = []
published_labels = []
fda = json.loads((ROOT / "raw/openfda_food_2023_2025.json").read_text(encoding="utf-8"))
unique = []
seen = set()
for row in fda["results"]:
    if row["reason_for_recall"] not in seen:
        seen.add(row["reason_for_recall"])
        unique.append(row)
# Purposive selection, not a representative sample: negation, uncertainty,
# named/unnamed hazards, multiple hazards, and incomplete product information.
fda_indices = [0, 4, 7, 8, 10, 13, 14, 15, 17, 18, 22, 23, 24, 26, 28, 35, 39, 41, 48, 52]
health = []
for n, index in enumerate(fda_indices, 1):
    row = unique[index]
    record = {"id": "ph%02d" % n, "text": row["reason_for_recall"]}
    health.append(record)
    url = "https://api.fda.gov/food/enforcement.json?search=recall_number:%22" + row["recall_number"] + "%22&limit=1"
    provenance.append({"id": record["id"], "dataset": "openFDA food enforcement", "source_record": row["recall_number"], "source_url": url, "report_date": row["report_date"], "transformation": "reason_for_recall field only; no wording changes", "license": "CC0 1.0 / public domain, subject to marked third-party exceptions"})
emit("public_health", health)

archive = zipfile.ZipFile(ROOT / "raw/reviews.zip")
review_indices = {
    "amazon_cells_labelled.txt": [1, 2, 5, 6, 11, 13, 16, 21, 24, 31],
    "yelp_labelled.txt": [1, 2, 5, 11, 12, 14, 15, 18, 28, 29],
}
reviews = []
for filename, indices in review_indices.items():
    archive_name = "sentiment labelled sentences/" + filename
    lines = archive.read(archive_name).decode("utf-8").splitlines()
    for index in indices:
        sentence, label = lines[index - 1].rsplit("\t", 1)
        record = {"id": "rev%02d" % (len(reviews) + 1), "text": sentence}
        reviews.append(record)
        provenance.append({"id": record["id"], "dataset": "UCI Sentiment Labelled Sentences", "source_file": archive_name, "source_line_1based": index, "source_url": "https://archive.ics.uci.edu/dataset/331/sentiment+labelled+sentences", "transformation": "sentence field only; original spelling/punctuation retained", "license": "CC BY 4.0", "attribution": "Kotzias, D. (2015). Sentiment Labelled Sentences [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C57604"})
        published_labels.append({"id": record["id"], "source_sentiment": "positive" if label == "1" else "negative", "label_origin": "published UCI label; not a label for aspects, recommendation, or evidence"})
emit("reviews", reviews)
jsonl(ROOT / "instructor/published_review_labels.jsonl", published_labels)

poems = (ROOT / "raw/dickinson_12242.txt").read_text(encoding="utf-8")
parts = re.split(r"\n([IVXLCDM]+)\.\n", poems[poems.index("I. LIFE."):])
literature = []
for n in range(1, 21):
    number, body = parts[2 * n - 1:2 * n + 1]
    # Remove an editorial title and the first poem's publication note.
    body = re.sub(r"\[Published.*?\]", "", body, flags=re.S)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body.strip()) if p.strip()]
    if "\n" not in paragraphs[0] and paragraphs[0].isupper():
        paragraphs = paragraphs[1:]
    stanza = paragraphs[0]
    record = {"id": "lit%02d" % n, "text": stanza}
    literature.append(record)
    provenance.append({"id": record["id"], "dataset": "Poems by Emily Dickinson, Three Series, Complete", "source_locator": "Series One, I. LIFE., poem " + number + ", first stanza", "source_url": "https://www.gutenberg.org/ebooks/12242", "transformation": "first stanza only; editorial titles and publication notes omitted; line breaks retained", "license": "Public domain in the USA; check local law outside the USA", "attribution": "Emily Dickinson; early edition edited by Mabel Loomis Todd and T. W. Higginson; Project Gutenberg eBook 12242, produced by Jim Tinsley"})
emit("liberal_arts", literature)
jsonl(DATA / "provenance.jsonl", provenance)

manifest = {
    "retrieved_on": "2026-10-13",
    "sample_design": "20 purposively selected teaching records per category, 60 total; not random or representative",
    "practice_ids": [r["id"] for rows in [health, reviews, literature] for r in rows[:10]],
    "holdout_ids": [r["id"] for rows in [health, reviews, literature] for r in rows[10:]],
    "sources": [
        {"file": "raw/openfda_food_2023_2025.json", "url": "https://api.fda.gov/food/enforcement.json?search=report_date:%5B20230101+TO+20251231%5D&limit=1000&sort=report_date:asc", "api_total_matching_at_retrieval": fda["meta"]["results"]["total"], "downloaded_records": len(fda["results"]), "api_last_updated": fda["meta"]["last_updated"], "license_url": "https://open.fda.gov/terms/", "selection": "20 unique reasons from the first 1000 chronologically sorted query results; sample records are 2023"},
        {"file": "raw/reviews.zip", "url": "https://archive.ics.uci.edu/static/public/331/sentiment+labelled+sentences.zip", "source_total_records": 3000, "license_url": "https://creativecommons.org/licenses/by/4.0/", "selection": "10 Amazon product sentences and 10 Yelp restaurant sentences; overall 10 published positive and 10 negative labels"},
        {"file": "raw/dickinson_12242.txt", "url": "https://www.gutenberg.org/ebooks/12242.txt.utf-8", "license_url": "https://www.gutenberg.org/ebooks/12242", "selection": "first stanzas of the first 20 poems in Series One, I. LIFE.; early edited edition, not a modern critical edition"},
    ],
}
for source in manifest["sources"]:
    source["sha256"] = hashlib.sha256((ROOT / source["file"]).read_bytes()).hexdigest()
(DATA / "source_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print("Built 60 source-backed records plus provenance, source labels, and import/handout formats.")
