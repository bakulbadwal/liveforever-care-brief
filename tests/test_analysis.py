from __future__ import annotations

import unittest
from datetime import date, timedelta

from liveforever_lab.analysis import (
    analyze_dataset,
    binary_effect,
    pearson_with_interval,
    quality_report,
)
from liveforever_lab.synthetic import generate_records


class AnalysisTests(unittest.TestCase):
    def test_synthetic_primary_signal_is_recovered(self) -> None:
        analysis = analyze_dataset(generate_records())
        effect = analysis["primary_effect"]
        self.assertGreater(effect["effect"], 2.0)
        self.assertGreater(effect["ci_low"], 0.0)
        self.assertGreaterEqual(effect["n_on"], 30)
        self.assertGreaterEqual(effect["n_off"], 30)
        self.assertEqual((effect["effect"], effect["ci_low"], effect["ci_high"], effect["n_on"], effect["n_off"]), (3.94, 1.13, 6.42, 36, 37))
        self.assertEqual([(item["effect"], item["ci_low"], item["ci_high"]) for item in analysis["secondary_effects"]], [(0.3, 0.05, 0.56), (-1.38, -2.26, -0.45)])

    def test_lag_pairs_exposure_with_next_day(self) -> None:
        start = date(2026, 1, 1)
        records = []
        conditions = [1, 0, 1, 0, 1, 0]
        outcomes = [0, 10, 1, 10, 1, 10]
        for index, (condition, outcome) in enumerate(zip(conditions, outcomes)):
            records.append({
                "date": (start + timedelta(days=index)).isoformat(),
                "cutoff": condition,
                "outcome": outcome,
            })
        effect = binary_effect(records, "cutoff", "outcome", lag_days=1, minimum_per_group=1)
        self.assertEqual(effect.n_on, 3)
        self.assertEqual(effect.n_off, 2)
        self.assertGreater(effect.effect, 8)

    def test_small_groups_are_labeled_early(self) -> None:
        records = generate_records(days=18)
        effect = binary_effect(records, "caffeine_cutoff_2pm", "hrv_ms")
        self.assertIn("minimum sample", effect.interpretation)

    def test_quality_report_flags_missing_calendar_days(self) -> None:
        records = generate_records()
        quality = quality_report(records, "caffeine_cutoff_2pm", "hrv_ms")
        self.assertLess(quality["coverage"], 1.0)
        self.assertTrue(any("coverage" in warning.lower() for warning in quality["warnings"]))

    def test_quality_report_preserves_observational_boundary(self) -> None:
        quality = quality_report(generate_records(), "caffeine_cutoff_2pm", "hrv_ms")
        self.assertTrue(any("not a randomized causal" in warning for warning in quality["warnings"]))

    def test_pearson_interval_contains_ordered_bounds(self) -> None:
        result = pearson_with_interval(generate_records(), "caffeine_mg", "sleep_hours")
        self.assertIsNotNone(result["r"])
        self.assertLess(result["ci_low"], result["r"])
        self.assertLess(result["r"], result["ci_high"])

    def test_singleton_condition_does_not_report_false_precision(self) -> None:
        records = [
            {"date": "2026-01-01", "cutoff": 1, "outcome": 0},
            {"date": "2026-01-02", "cutoff": 0, "outcome": 10},
            {"date": "2026-01-03", "cutoff": 0, "outcome": 1},
        ]
        effect = binary_effect(records, "cutoff", "outcome")
        self.assertEqual(effect.effect, 9)
        self.assertIsNone(effect.ci_low)
        self.assertIsNone(effect.ci_high)
        self.assertIn("interval unavailable", effect.interpretation)

    def test_timeline_uses_actual_previous_calendar_day(self) -> None:
        records = [
            {"date": "2026-01-01", "caffeine_cutoff_2pm": 1, "hrv_ms": 40},
            {"date": "2026-01-02", "caffeine_cutoff_2pm": 0, "hrv_ms": 50},
            {"date": "2026-01-04", "caffeine_cutoff_2pm": 1, "hrv_ms": 45},
        ]
        timeline = analyze_dataset(records)["timeline"]
        self.assertIsNone(timeline[0]["prior_day_caffeine_cutoff_2pm"])
        self.assertEqual(timeline[1]["prior_day_caffeine_cutoff_2pm"], 1)
        self.assertIsNone(timeline[2]["prior_day_caffeine_cutoff_2pm"])

    def test_field_coverage_counts_actual_outcomes(self) -> None:
        analysis = analyze_dataset(generate_records())
        self.assertEqual(analysis["dataset"]["field_coverage"]["hrv_ms"], 78)
        self.assertEqual(analysis["dataset"]["field_coverage"]["caffeine_cutoff_2pm"], 80)

    def test_empty_quality_contract_is_complete(self) -> None:
        quality = quality_report([], "cutoff", "outcome")
        self.assertEqual(quality["paired_days"], 0)
        self.assertEqual(quality["coverage"], 0)
        self.assertEqual(quality["grade"], "F")


if __name__ == "__main__":
    unittest.main()
