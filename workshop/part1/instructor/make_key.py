"""Create proposed instructor annotations; interpretations need human adjudication."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
entries = []


def add(dataset, annotation, note):
    entries.append({"dataset": dataset, "id": annotation["id"], "annotation_status": "Proposed workshop annotation, not independently expert-validated gold", "proposed_annotation": annotation, "adjudication_note": note})


def health(record_id, product, types, hazards, assertion, evidence, note):
    add("public_health", {"id": record_id, "product": product, "hazard_types": types, "hazards": hazards, "hazard_assertion": assertion, "illness_count": None, "recommended_action": None, "evidence": evidence}, note)


health("ph03", None, ["biological"], ["Salmonella"], "reported_present", ["Products were found to be contaminated with Salmonella."], "The record asserts a finding; the code does not independently verify it. Generic Products is not a named food.")
health("ph05", "Tartar sauce", ["undeclared_allergen"], ["fish", "soy", "milk"], "reported_present", ["Tartar sauce", "undeclared fish, soy, and milk allergens"], "Do not also add labeling_other solely for the allergen declaration failure.")
health("ph09", None, ["labeling_other", "undeclared_allergen"], ["milk"], "reported_present", ["lists FD&C Red #1 instead of FD&C Blue # 1", "does not declare milk on the label"], "The dye-name error is a distinct labeling issue, not evidence that the dye itself is toxic. Accept Sodium Caseinate as an additional named milk-related ingredient if the group agrees to include ingredients in hazards.")
health("ph11", None, ["biological", "chemical"], ["mold (Aspergillus brasiliensis)", "Ochratoxin A"], "reported_present", ["presence of mold (Aspergillus brasiliensis) and Ochratoxin A"], "Accept separate mold and Aspergillus brasiliensis entries or just the Latin name when the hazard is fully retained.")
health("ph13", "frozen manicotti pasta", ["biological"], ["Listeria monocytogenes"], "potential", ["Possible contamination with Listeria monocytogenes", "frozen manicotti pasta"], "Possible must not become confirmed; illness_count and consumer instructions are absent.")
health("ph16", None, ["undeclared_allergen", "chemical"], ["milk", "soy", "peanuts", "almonds", "walnuts", "pecans", "cashews", "sulfites"], "reported_present", ["undeclared milk, soy, peanuts, tree nuts (almonds, walnuts, pecans, cashews), and sulfites"], "Accept tree nuts as an additional umbrella term, with all four named nuts retained. This exercise's chemical code for sulfites is a rubric choice, not a risk ranking.")


def review(record_id, sentiment, target, aspects, recommendation, evidence, note):
    add("reviews", {"id": record_id, "sentiment": sentiment, "target": target, "aspects": aspects, "recommendation": recommendation, "evidence": evidence}, note)


review("rev03", "positive", "mic", ["sound"], "not_stated", ["mic is great"], "Praise is not an explicit recommendation. The source does not name the phone/headset model.")
review("rev07", "positive", None, ["unspecified"], "recommend", ["Highly recommend"], "The recommended object is not named. blue tooth phone describes potential users' equipment and need not be the reviewed product.")
review("rev10", "mixed", "phone", ["functionality"], "not_stated", ["simple little phone to use", "breakage is unacceptible"], "The published binary UCI label is negative. The workshop allows mixed sentiment; the discrepancy is a schema difference. Preserve the original spelling in evidence.")
review("rev12", "negative", "Crust", ["food"], "not_stated", ["Crust is not good."], "Good is negated; a keyword-only classifier may get this wrong.")
review("rev13", "positive", "menu", ["food", "value"], "not_stated", ["selection on the menu was great", "so were the prices"], "Both menu variety and prices are evaluated. Accept selection as the exact target phrase instead of menu.")
review("rev20", "negative", "food", ["food", "service"], "not_stated", ["Took an hour to get our food", "my food was Luke warm", "Our sever was running around like he was totally overwhelmed"], "Treat overwhelmed as the reviewer's interpretation. No need to correct Luke or sever in evidence. Accept multiple exact targets if the schema is intentionally revised.")


def literature(record_id, person, imagery, theme, support, alternative, limit, evidence, note):
    add("liberal_arts", {"id": record_id, "grammatical_person": person, "imagery": imagery, "proposed_theme": theme, "theme_evidence": support, "alternative_reading": alternative, "context_limit": limit, "evidence": evidence}, note)


literature("lit03", "second", ["religion"], "The addressed soul faces a risky choice.", "Soul, wilt thou toss again?", "A wager serves as a metaphor for repeated uncertainty.", "The excerpt does not identify the soul or explain the outcome of the choice.", ["Soul", "thou"], "Other for gambling imagery is reasonable if a group first expands the definition; toss does not establish a literal casino visit.")
literature("lit06", "multiple", ["body", "nature"], "Helping vulnerable beings gives life purpose.", "I shall not live in vain;", "The speaker sets a modest ethical standard for a worthwhile life.", "The stanza does not establish the author's motives or actual actions.", ["I", "his", "heart", "fainting robin", "nest"], "First-person I plus third-person his meets our explicit-pronoun rubric; first is acceptable under a revised narrator-perspective rubric. heart may be understood metaphorically.")
literature("lit08", "multiple", ["nature", "body"], "An outward burst of vitality may accompany suffering or death.", "'T is but the ecstasy of death,", "The stanza questions whether visible energy reveals well-being.", "This stanza does not establish a real observed animal event.", ["I", "'T is", "wounded deer", "death", "brake"], "Our rubric counts the contracted impersonal it as third person. A simpler speaker-perspective system could code first. brake refers to vegetation here; no need to resolve it using outside context.")
literature("lit11", "multiple", ["body", "other"], "Social consensus polices which behavior counts as sanity.", "Assent, and you are sane;", "The stanza contrasts discernment with coercive majority rule.", "The stanza does not identify a historical institution or diagnose anyone.", ["'T is", "you", "eye", "chain"], "The explicit you and contracted it yield multiple in this rubric. Accept second under a narrator/addressee rubric agreed before scoring. The theme is a proposed reading, not a diagnostic statement.")
literature("lit12", "multiple", ["commerce"], "A speaker offers existence in exchange for an unnamed desire.", "I offered Being for it;", "The merchant's smile suggests unequal power in an ambiguous exchange.", "The excerpt does not identify the requested thing or the merchant.", ["I", "it", "merchant"], "First person I and third person it meet the explicit-pronoun rule. Other interpretations can be supported; do not infer a biographical event.")
literature("lit19", "third", ["none"], "Pain disrupts a sense of beginnings and temporal continuity.", "It cannot recollect", "The stanza personifies pain as a state without a remembered origin.", "This excerpt does not establish a clinical mechanism of pain or the full poem's ending.", ["It"], "Pain is abstract; our imagery rubric does not automatically treat it as bodily imagery. body is acceptable only after a documented rubric change. Theme wording is not scored by exact match.")

(ROOT / "proposed_key.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in entries), encoding="utf-8")
for dataset in ["public_health", "reviews", "liberal_arts"]:
    (ROOT / (dataset + "_proposed_annotations.jsonl")).write_text("".join(json.dumps(x["proposed_annotation"], ensure_ascii=False) + "\n" for x in entries if x["dataset"] == dataset), encoding="utf-8")
print("Created 18 proposed annotations and adjudication notes.")
