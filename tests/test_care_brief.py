from __future__ import annotations

import unittest

from liveforever_lab.analysis import analyze_dataset
from liveforever_lab.care_brief import build_care_brief
from liveforever_lab.planner import build_plan
from liveforever_lab.synthetic import generate_records


class CareBriefTests(unittest.TestCase):
    def setUp(self) -> None:
        self.analysis = analyze_dataset(generate_records())
        self.plan = build_plan(self.analysis)
        self.brief = build_care_brief(self.analysis, self.plan)

    def test_brief_preserves_the_primary_analysis_verbatim(self) -> None:
        self.assertEqual(
            self.brief["evidence_summary"]["primary_effect"],
            self.analysis["primary_effect"],
        )

    def test_brief_has_a_traceable_source_ledger(self) -> None:
        source_ids = {source["id"] for source in self.brief["source_ledger"]}
        self.assertEqual(
            source_ids,
            {"wearables", "habit_log", "laboratory", "genomics"},
        )
        self.assertTrue(
            all(source["provenance"] for source in self.brief["source_ledger"])
        )

    def test_brief_surfaces_uncertainty_and_missing_evidence(self) -> None:
        self.assertGreaterEqual(len(self.brief["uncertainty"]), 3)
        self.assertGreaterEqual(len(self.brief["missing_evidence"]), 3)
        combined = " ".join(self.brief["uncertainty"]).lower()
        self.assertIn("observational", combined)

    def test_brief_prepares_questions_for_a_clinician(self) -> None:
        questions = self.brief["questions_for_clinician"]
        self.assertGreaterEqual(len(questions), 4)
        self.assertTrue(all(question.endswith("?") for question in questions))

    def test_ai_contract_locks_calculations_and_forbids_medical_authority(self) -> None:
        contract = self.brief["ai_contract"]
        self.assertIn("evidence_summary.primary_effect", contract["immutable_paths"])
        self.assertIn("diagnose", " ".join(contract["forbidden_actions"]).lower())
        self.assertIn("prescribe", " ".join(contract["forbidden_actions"]).lower())

    def test_brief_is_explicitly_synthetic_and_non_clinical(self) -> None:
        self.assertEqual(self.brief["privacy"]["record_type"], "synthetic")
        self.assertFalse(self.brief["privacy"]["contains_phi"])
        self.assertIn("not medical advice", self.brief["review_status"].lower())


if __name__ == "__main__":
    unittest.main()
