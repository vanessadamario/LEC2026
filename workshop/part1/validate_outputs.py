"""Check classroom model outputs without dependencies or model calls.

Usage: python3 validate_outputs.py public_health predictions.jsonl
Checks format, declared types/enums, record IDs and quoted evidence.
It does NOT decide whether a scientific/literary annotation is correct.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def check_schema(value, schema, path="$"):
    problems = []
    types = schema.get("type", [])
    types = [types] if isinstance(types, str) else types
    matches = {
        "null": value is None,
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "array": isinstance(value, list),
        "object": isinstance(value, dict),
    }
    if types and not any(matches.get(t, False) for t in types):
        return [path + ": wrong type; expected " + str(types)]
    if "enum" in schema and value not in schema["enum"]:
        problems.append(path + ": value outside allowed vocabulary")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                problems.append(path + ": missing " + key)
        for key, item in value.items():
            if key not in schema.get("properties", {}):
                if schema.get("additionalProperties") is False:
                    problems.append(path + ": extra key " + key)
            else:
                problems.extend(check_schema(item, schema["properties"][key], path + "." + key))
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            problems.append(path + ": list too short")
        if schema.get("uniqueItems") and len({json.dumps(x, sort_keys=True) for x in value}) != len(value):
            problems.append(path + ": duplicate list values")
        for i, item in enumerate(value):
            problems.extend(check_schema(item, schema.get("items", {}), path + "[%d]" % i))
    if isinstance(value, int) and not isinstance(value, bool) and value < schema.get("minimum", value):
        problems.append(path + ": below minimum")
    return problems


def validate(name, rows):
    schema = json.loads((ROOT / "schemas" / (name + ".schema.json")).read_text())
    source = {x["id"]: x["text"] for x in map(json.loads, (ROOT / "data" / (name + ".jsonl")).read_text().splitlines())}
    seen = set()
    reports = []
    for line_number, row in enumerate(rows, 1):
        problems = []
        try:
            value = json.loads(row)
        except json.JSONDecodeError as exc:
            reports.append({"line": line_number, "ok": False, "problems": ["Invalid JSON: " + exc.msg]})
            continue
        # The optional single-record Langflow demonstration wraps one dictionary.
        if isinstance(value, dict) and set(value) == {"annotation"}:
            value = value["annotation"]
        problems.extend(check_schema(value, schema))
        record_id = value.get("id") if isinstance(value, dict) else None
        if record_id not in source:
            problems.append("Unknown or missing record ID")
        else:
            if record_id in seen:
                problems.append("Duplicate record ID")
            seen.add(record_id)
            text = source[record_id]
            evidence = value.get("evidence", [])
            for quote in evidence if isinstance(evidence, list) else []:
                if isinstance(quote, str) and (not quote or quote not in text):
                    problems.append("Evidence is not a nonempty exact input substring: " + repr(quote))
            for key in ["theme_evidence", "product", "target", "recommended_action"]:
                quote = value.get(key)
                if isinstance(quote, str) and (not quote or quote not in text):
                    problems.append(key + " is not an exact input substring")
            hazards = value.get("hazards", [])
            for quote in hazards if isinstance(hazards, list) else []:
                if isinstance(quote, str) and (not quote or quote not in text):
                    problems.append("Named hazard is not an exact input substring: " + repr(quote))
            for key, singleton in [("hazard_types", "unknown"), ("aspects", "unspecified"), ("imagery", "none")]:
                values = value.get(key, [])
                if isinstance(values, list) and singleton in values and len(values) > 1:
                    problems.append(singleton + " must appear alone")
            for key in ["proposed_theme", "alternative_reading"]:
                if isinstance(value.get(key), str) and len(value[key].split()) > 20:
                    problems.append(key + " exceeds 20 words")
            if name == "liberal_arts" and (value.get("proposed_theme") is None) != (value.get("theme_evidence") is None):
                problems.append("Theme and theme evidence must either both be null or both be supplied")
        reports.append({"line": line_number, "id": record_id, "ok": not problems, "problems": problems})
    return reports


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", choices=["public_health", "reviews", "liberal_arts"])
    parser.add_argument("outputs", type=Path)
    args = parser.parse_args()
    lines = args.outputs.read_text(encoding="utf-8").splitlines()
    reports = validate(args.dataset, lines)
    for report in reports:
        print(json.dumps(report, ensure_ascii=False))
    print("Valid structure/evidence: %d/%d. Content needs human review." % (sum(r["ok"] for r in reports), len(reports)))
    raise SystemExit(0 if reports and all(r["ok"] for r in reports) else 1)
