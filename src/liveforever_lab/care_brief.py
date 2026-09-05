"""Build a source-linked, clinician-reviewable brief from fixed analysis output.

The brief is a deterministic handoff contract. It prepares the evidence and
questions for review; it does not diagnose, prescribe, or replace a visit.
"""

from __future__ import annotations

from copy import deepcopy
import json
import math
import re
from typing import Any
from urllib.parse import quote, urlsplit


def _number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _source_url(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = urlsplit(value)
        if parsed.scheme in {"http", "https"} and parsed.hostname and not parsed.username and not parsed.password:
            return quote(value, safe=":/?=&%#-._~")
    except ValueError:
        pass
    return None


def _source_ledger(analysis: dict[str, Any]) -> list[dict[str, Any]]:
    dataset = analysis["dataset"]
    quality = analysis["quality"]
    laboratory = analysis.get("longevity_snapshot") or {}
    genomics = analysis.get("genomics_context") or {}
    counts = dataset.get("field_coverage", {})
    provenance = (analysis.get("provenance") or {}).get("sources", {})
    sources = [
        {
            "id": "wearables",
            "label": "Wearable recovery record",
            "status": f'{dataset["recorded_days"]} recorded days',
            "fields": ["nightly HRV", "sleep duration", "resting heart rate"],
            "available": any(counts.get(field, 0) for field in ("hrv_ms", "sleep_hours", "resting_hr")),
            "coverage": {field: counts.get(field, 0) for field in ("hrv_ms", "sleep_hours", "resting_hr")},
            "role": "Measured outcomes; the primary estimate uses next-day HRV pairs.",
        },
        {
            "id": "habit_log",
            "label": "Caffeine and context log",
            "status": f'{quality["paired_days"]} paired nights',
            "fields": ["caffeine timing", "daily dose", "training", "alcohol"],
            "available": counts.get("caffeine_cutoff_2pm", 0) > 0,
            "coverage": {field: counts.get(field, 0) for field in ("caffeine_cutoff_2pm", "caffeine_mg", "training_load", "alcohol_units")},
            "role": "Caffeine timing is the exposure; other logged behaviors provide context.",
        },
        {
            "id": "laboratory",
            "label": "Laboratory context",
            "status": laboratory.get("completeness", "Not supplied for this run"),
            "fields": ["published PhenoAge inputs"],
            "available": _number(laboratory.get("phenoage")),
            "coverage": {},
            "role": "Context only; excluded from the caffeine effect estimate.",
        },
        {
            "id": "genomics",
            "label": "Genomic hypothesis context",
            "status": genomics.get("confidence", "Not supplied for this run"),
            "fields": [genomics.get("gene", "CYP1A2 marker not supplied")],
            "available": bool(genomics) and genomics.get("confidence") not in {None, "not available"},
            "coverage": {},
            "role": "Hypothesis context only; excluded from the caffeine effect estimate.",
        },
    ]
    for source in sources:
        origin = provenance.get(source["id"], {}) if source["available"] else {}
        source["url"] = _source_url(origin.get("url"))
        source["provenance"] = origin.get("provenance") or (
            "Provenance not supplied for this source." if source["available"] else "Not supplied for this run."
        )
        if not source["available"]:
            source["status"] = "Not supplied for this run"
    return sources


def _readiness(primary: dict[str, Any], quality: dict[str, Any], sources: list[dict[str, Any]]) -> dict[str, Any]:
    """Workflow triage, not a validated clinical score or a significance verdict."""
    n_on, n_off = primary["n_on"], primary["n_off"]
    has_effect = _number(primary.get("effect")) and min(n_on, n_off) > 0
    has_interval = _number(primary.get("ci_low")) and _number(primary.get("ci_high"))
    if not has_effect:
        signal = "unavailable"
    elif not has_interval:
        signal = "interval_unavailable"
    elif primary["ci_low"] <= 0 <= primary["ci_high"]:
        signal = "inconclusive"
    else:
        signal = "higher" if primary["effect"] > 0 else "lower"
    core_sources = sources[:2]
    source_links = all(source["available"] and source["url"] for source in core_sources)
    sample_met = min(n_on, n_off) >= 10
    quality_met = _number(quality.get("score")) and quality["score"] >= 75
    if not has_effect:
        status, label = "insufficient", "Comparison unavailable"
    elif not sample_met or not has_interval or not quality_met or not source_links:
        status, label = "limited", "Evidence has review gaps"
    else:
        status = "reviewable"
        label = "Comparison ready to review" if signal == "inconclusive" else "Association ready to review"
    return {
        "status": status, "label": label, "signal": signal,
        "sample_target_per_condition": 10,
        "sample_target_met": sample_met,
        "interval_available": has_interval,
        "core_sources_linked": bool(source_links),
        "sources_supplied": sum(source["available"] for source in sources),
        "sources_total": len(sources),
        "warning_count": len(quality["warnings"]),
        "boundary": "Readiness describes evidence available for review, not medical significance or permission to act. Optional context does not validate the association.",
    }


def _signal_text(primary: dict[str, Any], readiness: dict[str, Any]) -> tuple[str, str]:
    counts = f"{primary['n_on']} cutoff and {primary['n_off']} usual-timing nights"
    effect = primary.get("effect")
    if readiness["signal"] == "unavailable":
        return "HRV comparison unavailable", f"Cannot compare nightly HRV: both conditions need paired outcomes ({counts})."
    if effect == 0:
        headline = "No average HRV difference"
        text = "No average HRV difference was observed between cutoff and usual-timing nights"
    else:
        direction = "higher" if effect > 0 else "lower"
        headline = f"{abs(effect):.2f} ms {direction} nightly HRV"
        text = f"Cutoff days were followed by {abs(effect):.2f} ms {direction} nightly HRV on average"
    if readiness["interval_available"]:
        text += f" (95% interval {primary['ci_low']:+.2f} to {primary['ci_high']:+.2f} ms; {counts})."
    else:
        text += f" ({counts}). The uncertainty interval is unavailable."
    if readiness["signal"] == "inconclusive":
        text += " The interval includes no difference; this comparison is inconclusive."
    if not readiness["sample_target_met"]:
        text += " This is an early estimate below the target of 10 paired observations per condition."
    return headline, text


def build_care_brief(
    analysis: dict[str, Any], plan: dict[str, Any]
) -> dict[str, Any]:
    """Return an immutable-evidence brief for a user-controlled clinical handoff."""
    primary = analysis["primary_effect"]
    secondary = analysis["secondary_effects"]
    quality = analysis["quality"]
    paired_days = primary["n_on"] + primary["n_off"]
    sources = _source_ledger(analysis)
    readiness = _readiness(primary, quality, sources)
    headline, signal_text = _signal_text(primary, readiness)
    provenance = analysis.get("provenance") or {}
    if readiness["status"] == "insufficient":
        why_this_visit = "The record cannot support a comparison yet. Review missing outcomes and condition coverage before interpreting a signal."
    elif readiness["status"] == "limited":
        why_this_visit = f"This comparison covers {paired_days} paired nights but has evidence limitations. Review sample size, uncertainty, source links, and quality warnings before interpreting it."
    elif readiness["signal"] == "inconclusive":
        why_this_visit = f"The HRV comparison across {paired_days} paired nights is inconclusive. Review uncertainty and possible alternative explanations."
    else:
        why_this_visit = f"An observed HRV association across {paired_days} paired nights is available for review. Its clinical relevance and alternative explanations remain open questions."

    return {
        "schema_version": "1.1",
        "title": "Personal evidence brief",
        "persona": analysis["dataset"]["persona"],
        "review_status": "Draft for clinician review; not medical advice.",
        "privacy": {
            "record_type": provenance.get("record_type", "unspecified"),
            "contains_phi": provenance.get("contains_phi"),
            "sharing_control": "User reviews and exports the brief; nothing is transmitted by the demo.",
        },
        "visit_question": analysis["question"],
        "why_this_visit": why_this_visit,
        "readiness": readiness,
        "signal_headline": headline,
        "evidence_summary": {
            "analysis_type": analysis["analysis_type"],
            "data_window": {
                "start_date": analysis["dataset"]["start_date"],
                "end_date": analysis["dataset"]["end_date"],
                "recorded_days": analysis["dataset"]["recorded_days"],
            },
            "primary_effect": deepcopy(primary),
            "secondary_effects": deepcopy(secondary),
            "quality": deepcopy(quality),
            "calculation_provenance": deepcopy(analysis.get("calculation_provenance", [])),
            "claim_boundary": analysis["claim_boundary"],
        },
        "plain_language_signal": signal_text,
        "source_ledger": sources,
        "quality_warnings": deepcopy(quality["warnings"]),
        "uncertainty": [
            "The comparison is observational and does not establish that caffeine timing caused the differences.",
            "Missing days, concurrent behaviors, illness, travel, stress, and device noise may influence the result.",
            f"The evidence-quality grade is {quality['grade']} ({quality['score']}/100), and all quality warnings remain attached.",
            "Genomic and laboratory context can prioritize a question but cannot validate the observed association.",
        ],
        "missing_evidence": [
            "A prospectively registered replication with balanced conditions and adherence tracking.",
            "Symptom, medication, illness, travel, and major schedule context reviewed for the same dates.",
            "Confirmation that the wearable trend is meaningful for this person in the broader clinical context.",
        ],
        "questions_for_clinician": [
            "Is this magnitude and pattern meaningful in the context of the person's history and symptoms?",
            "What clinical or behavioral context could offer a more likely explanation for the observed pattern?",
            "Are there reasons a caffeine-timing retest would be inappropriate or should be modified?",
            "What additional measurements would make a future comparison more useful for review?",
        ],
        "proposed_next_step": {
            "title": plan["title"],
            "design": plan["design"],
            "decision_rule": plan["decision_rule"],
            "controls": deepcopy(plan["controls"]),
            "stop_conditions": deepcopy(plan["stop_conditions"]),
            "schedule": deepcopy(plan["schedule"]),
            "schedule_status": plan["status"],
            "status": "Discuss before starting; this is an experiment draft, not a treatment plan.",
        },
        "ai_contract": {
            "role": "Turn the locked evidence into a concise, source-linked draft and prepare questions for human review.",
            "immutable_paths": [
                "evidence_summary.primary_effect",
                "evidence_summary.secondary_effects",
                "evidence_summary.quality",
                "source_ledger",
                "readiness",
                "quality_warnings",
            ],
            "allowed_actions": [
                "Explain fixed results in plain language.",
                "Identify uncertainty, missing context, and alternative hypotheses.",
                "Organize questions for a clinician and shorten the draft after user review.",
            ],
            "forbidden_actions": [
                "Do not diagnose a condition.",
                "Do not prescribe treatment or change medication or supplements.",
                "Do not alter, recompute, omit, or invent evidence values or sources.",
                "Do not convert an association into a causal or clinical claim.",
            ],
            "human_gate": "The user reviews every field and chooses whether to export or share it.",
        },
    }


def export_care_brief(brief: dict[str, Any], format: str = "json") -> str:
    """Serialize without altering evidence or selecting away warnings/sources.

    Markdown includes the complete JSON contract as an auditable appendix. This
    function only returns text; callers and the browser choose where to save it.
    """
    contract = json.dumps(brief, ensure_ascii=False, indent=2, allow_nan=False)
    if format == "json":
        return contract + "\n"
    if format != "markdown":
        raise ValueError("Export format must be 'json' or 'markdown'.")

    def md(value: Any) -> str:
        text = str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return re.sub(r"([\\`*_\[\]|])", r"\\\1", text)

    window = brief["evidence_summary"]["data_window"]
    lines = [
        f"# {md(brief['title'])}", "", md(brief["review_status"]), "",
        f"Person: {md(brief['persona'])}  ",
        f"Record: {md(brief['privacy']['record_type'])}  ",
        f"Window: {window['start_date'] or 'Not supplied'} to {window['end_date'] or 'Not supplied'}; {window['recorded_days']} recorded days.", "",
        f"## {md(brief['visit_question'])}", "", md(brief["why_this_visit"]), "",
        f"**{md(brief['readiness']['label'])}.** {md(brief['readiness']['boundary'])}", "",
        "## Observed comparison", "", md(brief["plain_language_signal"]), "",
        "## Quality warnings", "", *[f"- {md(item)}" for item in brief["quality_warnings"]], "",
        "## Sources and coverage", "",
    ]
    for source in brief["source_ledger"]:
        label = md(source["label"])
        url = _source_url(source.get("url"))
        lines += [f"### {label}", "", f"{md(source['status'])}. {md(source['role'])}", "", md(source["provenance"])]
        if url:
            lines += ["", f"[Inspect source]({url})"]
        if source["coverage"]:
            lines += ["", "Recorded field counts: " + "; ".join(f"{md(field)}: {count}" for field, count in source["coverage"].items()) + "."]
        lines.append("")
    for heading, key in (
        ("Uncertainty", "uncertainty"), ("Missing evidence", "missing_evidence"),
        ("Questions for a clinician", "questions_for_clinician"),
    ):
        lines += [f"## {heading}", "", *[f"- {md(item)}" for item in brief[key]], ""]
    step = brief["proposed_next_step"]
    lines += ["## Proposed next step for discussion", "", md(step["title"]), "", md(step["status"]), "", md(step["design"]), "", md(step["decision_rule"]), "", "Controls:", "", *[f"- {md(item)}" for item in step["controls"]], "", "When to pause:", "", *[f"- {md(item)}" for item in step["stop_conditions"]], "", md(brief["privacy"]["sharing_control"]), "", "## Complete evidence contract", "", "The exact source, numerical, uncertainty, plan, and AI-boundary fields are retained below.", ""]
    fence = "`" * max(3, 1 + max((len(match) for match in re.findall(r"`+", contract)), default=0))
    lines += [fence + "json", contract, fence, ""]
    return "\n".join(lines)
