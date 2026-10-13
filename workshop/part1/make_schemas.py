"""Write strict JSON Schemas for Dify or an independent output validator."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
(ROOT / "schemas").mkdir(exist_ok=True)


def string(enum=None, nullable=False):
    result = {"type": ["string", "null"] if nullable else "string"}
    if enum:
        result["enum"] = enum
    return result


def array(enum=None):
    return {"type": "array", "items": string(enum), "uniqueItems": True}


fields = {
    "public_health": {
        "id": string(), "product": string(nullable=True),
        "hazard_types": array(["biological", "undeclared_allergen", "foreign_material", "chemical", "labeling_other", "process_hygiene", "other", "unknown"]),
        "hazards": array(), "hazard_assertion": string(["reported_present", "potential", "mixed", "unspecified"]),
        "illness_count": {"type": ["integer", "null"], "minimum": 0},
        "recommended_action": string(nullable=True), "evidence": array(),
    },
    "reviews": {
        "id": string(), "sentiment": string(["positive", "negative", "mixed", "neutral", "unclear"]),
        "target": string(nullable=True),
        "aspects": array(["functionality", "sound", "battery", "comfort", "value", "food", "service", "ambience", "other", "unspecified"]),
        "recommendation": string(["recommend", "avoid", "not_stated"]), "evidence": array(),
    },
    "liberal_arts": {
        "id": string(), "grammatical_person": string(["first", "second", "third", "multiple", "undetermined"]),
        "imagery": array(["nature", "body", "religion", "war", "commerce", "domestic", "arts_reading", "other", "none"]),
        "proposed_theme": string(nullable=True), "theme_evidence": string(nullable=True),
        "alternative_reading": string(nullable=True), "context_limit": string(), "evidence": array(),
    },
}
for name, properties in fields.items():
    for key in ["hazard_types", "aspects", "imagery"]:
        if key in properties:
            properties[key]["minItems"] = 1
    schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": name + " workshop annotation", "type": "object", "properties": properties, "required": list(properties), "additionalProperties": False}
    (ROOT / "schemas" / (name + ".schema.json")).write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
print("Wrote three annotation schemas.")
