from __future__ import annotations

import unittest
import json
from copy import deepcopy

from liveforever_lab.analysis import analyze_dataset
from liveforever_lab.care_brief import build_care_brief, export_care_brief
from liveforever_lab.planner import build_plan
from liveforever_lab.synthetic import DEMO_PROVENANCE, generate_records


class CareBriefTests(unittest.TestCase):
    def setUp(self) -> None:
        self.analysis = analyze_dataset(generate_records(), provenance=DEMO_PROVENANCE)
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

    def brief_with_effect(self, **values):
        analysis = deepcopy(self.analysis)
        analysis["primary_effect"].update(values)
        return build_care_brief(analysis, build_plan(analysis))

    def test_negative_effect_never_claims_higher_recovery(self) -> None:
        brief = self.brief_with_effect(effect=-3.94, ci_low=-6.42, ci_high=-1.13)
        self.assertIn("3.94 ms lower", brief["plain_language_signal"])
        self.assertNotIn("higher", brief["plain_language_signal"])
        self.assertEqual(brief["readiness"]["signal"], "lower")
        self.assertNotIn("recovery pattern worth", brief["why_this_visit"])

    def test_interval_crossing_zero_remains_inconclusive(self) -> None:
        brief = self.brief_with_effect(effect=1.0, ci_low=-2.0, ci_high=4.0)
        self.assertEqual(brief["readiness"]["signal"], "inconclusive")
        self.assertEqual(brief["readiness"]["label"], "Comparison ready to review")
        self.assertIn("includes no difference", brief["plain_language_signal"])
        self.assertIn("inconclusive", brief["why_this_visit"].lower())

    def test_zero_effect_does_not_imply_improvement(self) -> None:
        brief = self.brief_with_effect(effect=0.0, ci_low=-2.0, ci_high=2.0)
        self.assertIn("No average HRV difference", brief["plain_language_signal"])

    def test_missing_condition_is_reviewable_without_a_made_up_estimate(self) -> None:
        records = generate_records()
        for record in records:
            record["caffeine_cutoff_2pm"] = 1
        analysis = analyze_dataset(records)
        brief = build_care_brief(analysis, build_plan(analysis))
        self.assertIsNone(brief["evidence_summary"]["primary_effect"]["effect"])
        self.assertEqual(brief["readiness"]["status"], "insufficient")
        self.assertIn("Cannot compare", brief["plain_language_signal"])
        self.assertEqual(brief["quality_warnings"], analysis["quality"]["warnings"])

    def test_empty_record_has_no_fabricated_dates_or_schedule(self) -> None:
        analysis = analyze_dataset([])
        plan = build_plan(analysis)
        brief = build_care_brief(analysis, plan)
        self.assertEqual(plan["schedule"], [])
        self.assertIsNone(brief["evidence_summary"]["data_window"]["start_date"])
        self.assertEqual(brief["readiness"]["status"], "insufficient")
        self.assertIn("No records supplied.", brief["quality_warnings"])

    def test_small_sample_and_poor_quality_never_get_ready_label(self) -> None:
        brief = self.brief_with_effect(n_on=2)
        self.assertEqual(brief["readiness"]["status"], "limited")
        analysis = deepcopy(self.analysis)
        analysis["quality"].update(score=40, grade="D")
        brief = build_care_brief(analysis, build_plan(analysis))
        self.assertEqual(brief["readiness"]["status"], "limited")
        self.assertIn("limitations", brief["why_this_visit"])

    def test_unknown_provenance_never_invents_synthetic_or_phi_clearance(self) -> None:
        analysis = analyze_dataset(generate_records())
        brief = build_care_brief(analysis, build_plan(analysis))
        self.assertEqual(brief["privacy"]["record_type"], "unspecified")
        self.assertIsNone(brief["privacy"]["contains_phi"])
        self.assertEqual(brief["persona"], "Not supplied")
        self.assertTrue(all("Synthetic" not in source["provenance"] for source in brief["source_ledger"]))

    def test_absent_optional_context_is_not_counted_as_supplied(self) -> None:
        sources = {source["id"]: source for source in self.brief["source_ledger"]}
        self.assertFalse(sources["laboratory"]["available"])
        self.assertFalse(sources["genomics"]["available"])
        self.assertIsNone(sources["laboratory"]["url"])
        self.assertEqual(self.brief["readiness"]["sources_supplied"], 2)

    def test_json_export_is_complete_and_does_not_mutate_brief(self) -> None:
        before = deepcopy(self.brief)
        self.assertEqual(json.loads(export_care_brief(self.brief, "json")), before)
        self.assertEqual(self.brief, before)

    def test_markdown_export_carries_sources_warnings_and_exact_evidence(self) -> None:
        text = export_care_brief(self.brief, "markdown")
        for warning in self.brief["quality_warnings"]:
            self.assertIn(warning, text)
        for item in self.brief["uncertainty"]:
            self.assertIn(item, text)
        self.assertIn(self.brief["source_ledger"][0]["url"], text)
        appendix = text.split("```json\n", 1)[1].split("\n```", 1)[0]
        self.assertEqual(json.loads(appendix), self.brief)

    def test_brief_copies_warnings_and_plan_stop_conditions(self) -> None:
        brief = deepcopy(self.brief)
        self.analysis["quality"]["warnings"].append("Changed after handoff")
        self.plan["stop_conditions"].append("Changed after handoff")
        self.assertNotIn("Changed after handoff", brief["quality_warnings"])
        self.assertEqual(self.brief["proposed_next_step"]["stop_conditions"], brief["proposed_next_step"]["stop_conditions"])

    def test_unsafe_source_urls_are_never_made_into_links(self) -> None:
        analysis = deepcopy(self.analysis)
        analysis["provenance"]["sources"]["wearables"]["url"] = "javascript:alert(1)"
        brief = build_care_brief(analysis, build_plan(analysis))
        self.assertIsNone(brief["source_ledger"][0]["url"])
        self.assertFalse(brief["readiness"]["core_sources_linked"])


if __name__ == "__main__":
    unittest.main()
