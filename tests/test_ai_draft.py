"""The cached AI draft must cite only locked numbers and make no forbidden claims."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from liveforever_lab import ai_draft

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = json.loads((ROOT / "demo" / "analysis.json").read_text(encoding="utf-8"))
CONTRACT = ANALYSIS["care_brief"]


def _doc(draft: dict, contract: dict = CONTRACT) -> dict:
    return {"inputs": {"contract_sha256": ai_draft.contract_sha256(contract)}, "draft": draft}


def _complete_draft(**overrides: object) -> dict:
    draft = {
        "question_for_review": "Does stopping caffeine by 2 PM improve next-day recovery?",
        "why_this_is_being_raised": "An HRV association across 73 paired nights is available for review.",
        "observed_signal": "Cutoff nights averaged 3.94 ms higher HRV (95% interval +1.13 to +6.42; 36 cutoff and 37 usual nights).",
        "evidence_and_provenance": "Four sources were supplied; laboratory and genomic context are excluded from the estimate.",
        "uncertainty_and_missing_context": ["Observational comparison.", "Illness and travel were not logged."],
        "what_this_does_not_establish": ["It does not establish that timing caused the difference.", "It is not a clinical finding."],
        "questions_for_clinician": ["Is this magnitude meaningful here?", "What else could explain it?"],
        "proposed_next_step": "A balanced 14-day retest is drafted for discussion.",
        "review_and_sharing_status": "Draft for clinician review; the user decides whether to share it.",
    }
    draft.update(overrides)
    return draft


class ContractValues(unittest.TestCase):
    def test_locked_numbers_are_allowed(self):
        allowed = ai_draft.contract_values(CONTRACT)
        for number in ("3.94", "1.13", "6.42", "36", "37", "73", "85", "95", "80", "14"):
            self.assertIn(number, allowed, number)

    def test_coverage_display_forms_are_allowed(self):
        allowed = ai_draft.contract_values(CONTRACT)
        self.assertIn("95", allowed)
        self.assertIn("95.2", allowed)


class Verification(unittest.TestCase):
    def test_complete_draft_with_locked_numbers_passes(self):
        result = ai_draft.verify(_doc(_complete_draft()), CONTRACT)
        self.assertEqual(result["unlisted_numbers"], [])
        self.assertEqual(result["forbidden_claims"], [])
        self.assertTrue(result["ok"], result)

    def test_invented_number_is_flagged(self):
        draft = _complete_draft(observed_signal="HRV was 4.1 ms higher, about 999 percent.")
        result = ai_draft.verify(_doc(draft), CONTRACT)
        self.assertEqual(result["unlisted_numbers"], ["4.1", "999"])
        self.assertFalse(result["ok"])

    def test_affirmative_claim_language_is_flagged_but_negated_use_is_allowed(self):
        negated = ai_draft.forbidden_claims("This does not establish that caffeine caused the change; it is not a diagnosis.")
        self.assertEqual(negated, [])
        affirmative = ai_draft.forbidden_claims("Late caffeine causes poor recovery, so she should stop it; this proves the effect.")
        labels = sorted(claim["label"] for claim in affirmative)
        self.assertEqual(labels, ["causal claim", "directive", "proof claim"])

    def test_stale_contract_hash_fails(self):
        doc = _doc(_complete_draft())
        doc["inputs"]["contract_sha256"] = "0" * 64
        result = ai_draft.verify(doc, CONTRACT)
        self.assertFalse(result["contract_sha256_matches"])
        self.assertFalse(result["ok"])

    def test_missing_section_fails(self):
        doc = _doc(_complete_draft(questions_for_clinician=[]))
        result = ai_draft.verify(doc, CONTRACT)
        self.assertEqual(result["missing_sections"], ["questions_for_clinician"])
        self.assertFalse(result["ok"])


class PromptAndSchema(unittest.TestCase):
    def test_prompt_carries_contract_and_boundaries(self):
        prompt = ai_draft.build_prompt(CONTRACT)
        self.assertIn("evidence_summary", prompt)
        self.assertIn("Do not diagnose", prompt)
        self.assertIn("## Care Brief Format", prompt)

    def test_schema_requires_every_section(self):
        schema = ai_draft.output_schema()
        self.assertEqual(set(schema["required"]), set(ai_draft.SECTIONS))
        self.assertFalse(schema["additionalProperties"])


class CachedDraft(unittest.TestCase):
    """The shipped draft is re-verified against the shipped contract on every run."""

    def test_cached_draft_verifies_against_current_contract(self):
        doc = json.loads((ROOT / "demo" / "ai_draft.json").read_text(encoding="utf-8"))
        result = ai_draft.verify(doc, CONTRACT)
        self.assertEqual(result["unlisted_numbers"], [], result)
        self.assertEqual(result["forbidden_claims"], [], result)
        self.assertTrue(result["contract_sha256_matches"], "regenerate demo/ai_draft.json after changing the contract")
        self.assertTrue(result["ok"], result)
        self.assertEqual(doc["generator"]["skill"], ai_draft.SKILL_NAME)
        self.assertIn("no live model calls", doc["generator"]["mode"])


if __name__ == "__main__":
    unittest.main()
