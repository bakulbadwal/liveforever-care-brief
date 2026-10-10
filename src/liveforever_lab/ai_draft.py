"""Cached AI draft: prompt, verification, and ingestion for the bounded model layer.

The hosted demo never calls a model. A draft is produced once, at build time,
by running the repository Skill through a model, and is then verified here
against the locked care-brief contract before it may ship:

* every number the model cites must already exist in the contract, at the
  contract's own rounding;
* no affirmative diagnostic, prescriptive, causal, or proof language may
  appear (negated uses such as "does not establish causation" are allowed);
* the draft must carry the SHA-256 of the exact contract it was written from,
  so a regenerated contract invalidates a stale draft.

The verification result is stored inside the draft so the page can show it,
and ``tests/test_ai_draft.py`` re-runs it on every test run.

Usage (build time):

    PYTHONPATH=src python3.11 -m liveforever_lab.ai_draft prompt --out /tmp/prompt.md
    PYTHONPATH=src python3.11 -m liveforever_lab.ai_draft schema --out /tmp/schema.json
    codex exec -m <model> --output-schema /tmp/schema.json -o /tmp/draft.json "$(cat /tmp/prompt.md)"
    PYTHONPATH=src python3.11 -m liveforever_lab.ai_draft ingest --result /tmp/draft.json \
        --model <model> --runner "codex-cli <version>"
    PYTHONPATH=src python3.11 -m liveforever_lab.ai_draft verify
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_PATH = ROOT / "demo" / "analysis.json"
DRAFT_PATH = ROOT / "demo" / "ai_draft.json"
SKILL_PATH = ROOT / "SKILL.md"

SCHEMA_VERSION = "1.0"
SKILL_NAME = "liveforever-evidence-lab"

PROSE_SECTIONS = (
    "question_for_review",
    "why_this_is_being_raised",
    "observed_signal",
    "evidence_and_provenance",
    "proposed_next_step",
    "review_and_sharing_status",
)
LIST_SECTIONS = (
    "uncertainty_and_missing_context",
    "what_this_does_not_establish",
    "questions_for_clinician",
)
SECTIONS = PROSE_SECTIONS[:4] + LIST_SECTIONS + PROSE_SECTIONS[4:]

_NUMBER = re.compile(r"\d+(?:\.\d+)?")

# Affirmative claim language the contract forbids. A match is allowed when a
# negation cue sits earlier in the same clause ("does not establish that ...").
_FORBIDDEN = (
    (re.compile(r"\bdiagnos(?:e|es|ed|is|tic)\b", re.I), "diagnosis"),
    (re.compile(r"\bprescri(?:be|bes|bed|ption)\b", re.I), "prescription"),
    (re.compile(r"\b(?:you|she|he|they|maya)\s+should\s+(?:take|stop|start|increase|reduce|cut|switch|avoid)\b", re.I), "directive"),
    (re.compile(r"\bprov(?:e|es|ed|en)\b", re.I), "proof claim"),
    (re.compile(r"\bcaus(?:es|ed|al|ation)\b", re.I), "causal claim"),
    (re.compile(r"\bclinically\s+normal\b", re.I), "clinical-normal claim"),
    (re.compile(r"\b(?:cures?|cured|treats?|treated|treatment)\b", re.I), "treatment claim"),
)
_NEGATION = re.compile(
    r"\b(?:not|no|never|cannot|can't|without|non|rather than|instead of|isn't|is not|does not|do not|did not|"
    r"doesn't|don't|didn't|neither|nor|unproven|untested|association only)\b",
    re.I,
)


# ----------------------------------------------------------------------------
# Contract helpers
# ----------------------------------------------------------------------------

def load_analysis(path: Path = ANALYSIS_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def contract_sha256(contract: dict[str, Any]) -> str:
    canonical = json.dumps(contract, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _canonical(token: str) -> str | None:
    try:
        value = Decimal(token)
    except InvalidOperation:
        return None
    text = format(value.normalize(), "f")
    return text[:-2] if text.endswith(".0") else text


def _walk(value: Any):
    if isinstance(value, dict):
        for item in value.values():
            yield from _walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk(item)
    else:
        yield value


def contract_values(contract: dict[str, Any]) -> set[str]:
    """Every number a draft may cite: numeric leaves, numbers inside the contract's own
    sentences, and the two display forms of coverage that the interface itself shows."""
    allowed: set[str] = set()
    for leaf in _walk(contract):
        if isinstance(leaf, bool):
            continue
        if isinstance(leaf, (int, float)):
            canonical = _canonical(repr(leaf) if isinstance(leaf, float) else str(leaf))
            if canonical:
                allowed.add(canonical.lstrip("-"))
        elif isinstance(leaf, str):
            for token in _NUMBER.findall(leaf):
                canonical = _canonical(token)
                if canonical:
                    allowed.add(canonical)
    coverage = (contract.get("evidence_summary") or {}).get("quality", {}).get("coverage")
    if isinstance(coverage, (int, float)):
        allowed.add(str(round(coverage * 100)))
        allowed.add(_canonical(f"{coverage * 100:.1f}") or "")
    allowed.discard("")
    return allowed


# ----------------------------------------------------------------------------
# Draft helpers
# ----------------------------------------------------------------------------

def draft_text(draft: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in SECTIONS:
        value = draft.get(key)
        if isinstance(value, list):
            parts.extend(str(item) for item in value)
        elif value is not None:
            parts.append(str(value))
    return "\n".join(parts)


def numbers_in_text(text: str) -> list[str]:
    seen: list[str] = []
    for token in _NUMBER.findall(text):
        canonical = _canonical(token)
        if canonical and canonical not in seen:
            seen.append(canonical)
    return seen


def forbidden_claims(text: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for pattern, label in _FORBIDDEN:
        for match in pattern.finditer(text):
            clause_start = max(text.rfind(".", 0, match.start()), text.rfind(";", 0, match.start()), text.rfind("\n", 0, match.start())) + 1
            clause = text[clause_start:match.start()]
            if _NEGATION.search(clause):
                continue
            context = text[max(0, match.start() - 60): match.end() + 40].replace("\n", " ").strip()
            findings.append({"term": match.group(0), "label": label, "context": context})
    return findings


def verify(draft_doc: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    draft = draft_doc.get("draft") or {}
    text = draft_text(draft)
    allowed = contract_values(contract)
    cited = numbers_in_text(text)
    unlisted = [number for number in cited if number not in allowed]
    claims = forbidden_claims(text)
    missing_sections = [key for key in SECTIONS if not draft.get(key)]
    expected_sha = contract_sha256(contract)
    recorded_sha = (draft_doc.get("inputs") or {}).get("contract_sha256")
    return {
        "verifier": "liveforever_lab.ai_draft.verify",
        "checked_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "numbers_cited": cited,
        "unlisted_numbers": unlisted,
        "forbidden_claims": claims,
        "missing_sections": missing_sections,
        "contract_sha256_matches": recorded_sha == expected_sha,
        "ok": not unlisted and not claims and not missing_sections and recorded_sha == expected_sha,
    }


# ----------------------------------------------------------------------------
# Prompt and schema for the build-time model run
# ----------------------------------------------------------------------------

def output_schema() -> dict[str, Any]:
    properties: dict[str, Any] = {}
    for key in PROSE_SECTIONS:
        properties[key] = {"type": "string"}
    for key in LIST_SECTIONS:
        properties[key] = {"type": "array", "items": {"type": "string"}, "minItems": 2, "maxItems": 6}
    return {
        "type": "object",
        "properties": properties,
        "required": list(SECTIONS),
        "additionalProperties": False,
    }


def _skill_excerpt() -> str:
    text = SKILL_PATH.read_text(encoding="utf-8")
    start = text.find("## Care Brief Format")
    return text[start:] if start >= 0 else text


def build_prompt(contract: dict[str, Any]) -> str:
    contract_json = json.dumps(contract, indent=2, ensure_ascii=False)
    return "\n".join([
        "You are the bounded AI layer of LiveForever Care Brief, operating under the repository's",
        f"`{SKILL_NAME}` Skill. Write the Care Brief draft for human review from the locked contract below.",
        "",
        "Hard rules (the output is verified mechanically before it can ship):",
        "1. Every number you write must already appear in the contract, with the contract's own rounding",
        "   (for example 3.94, +1.13, +6.42, 36, 37, 73, 85, 95). Never compute, round, or estimate a new value.",
        "2. Do not diagnose, prescribe, recommend starting or stopping anything, or convert the association",
        "   into a causal or clinical claim. Say what the evidence does not establish.",
        "3. Keep the user in control: this is a draft they review before deciding whether to share it.",
        "4. Plain English a patient and a clinician can both read. Each prose section at most 80 words;",
        "   each list 3 to 5 items of at most 25 words. Add the context a general-purpose model would leave",
        "   implicit: concrete alternative explanations and the specific missing measurements.",
        "5. Return only JSON matching the provided schema. No markdown, no commentary.",
        "",
        "Skill guidance that governs this draft:",
        "",
        _skill_excerpt().strip(),
        "",
        "Locked contract (immutable inputs — cite, never alter):",
        "",
        "```json",
        contract_json,
        "```",
    ])


# ----------------------------------------------------------------------------
# Ingestion
# ----------------------------------------------------------------------------

def ingest(result: dict[str, Any], *, model: str, runner: str, prompt_sha256: str, contract: dict[str, Any]) -> dict[str, Any]:
    draft_doc: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "generator": {
            "skill": SKILL_NAME,
            "runner": runner,
            "model": model,
            "mode": "Generated once at build time from the locked contract; the hosted demo makes no live model calls.",
        },
        "inputs": {
            "contract_sha256": contract_sha256(contract),
            "prompt_sha256": prompt_sha256,
        },
        "draft": {key: result.get(key) for key in SECTIONS},
    }
    draft_doc["verification"] = verify(draft_doc, contract)
    return draft_doc


def _print_report(verification: dict[str, Any]) -> None:
    print(f"numbers cited: {len(verification['numbers_cited'])}")
    print(f"unlisted numbers: {verification['unlisted_numbers'] or 'none'}")
    print(f"forbidden claims: {len(verification['forbidden_claims'])}")
    for claim in verification["forbidden_claims"]:
        print(f"  - {claim['label']} ({claim['term']}): …{claim['context']}…")
    print(f"missing sections: {verification['missing_sections'] or 'none'}")
    print(f"contract hash matches: {verification['contract_sha256_matches']}")
    print(f"ok: {verification['ok']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p_prompt = sub.add_parser("prompt", help="print the build-time prompt for the model")
    p_prompt.add_argument("--out", type=Path)
    p_schema = sub.add_parser("schema", help="print the JSON schema the model's response must match")
    p_schema.add_argument("--out", type=Path)
    p_ingest = sub.add_parser("ingest", help="verify a model result and write demo/ai_draft.json")
    p_ingest.add_argument("--result", type=Path, required=True)
    p_ingest.add_argument("--model", required=True)
    p_ingest.add_argument("--runner", required=True)
    p_ingest.add_argument("--out", type=Path, default=DRAFT_PATH)
    sub.add_parser("verify", help="re-verify demo/ai_draft.json against demo/analysis.json")
    args = parser.parse_args(argv)

    contract = load_analysis()["care_brief"]
    if args.command == "prompt":
        text = build_prompt(contract)
        if args.out:
            args.out.write_text(text, encoding="utf-8")
            print(f"wrote {args.out} (sha256 {hashlib.sha256(text.encode('utf-8')).hexdigest()})")
        else:
            print(text)
        return 0
    if args.command == "schema":
        text = json.dumps(output_schema(), indent=2)
        if args.out:
            args.out.write_text(text + "\n", encoding="utf-8")
            print(f"wrote {args.out}")
        else:
            print(text)
        return 0
    if args.command == "ingest":
        raw = args.result.read_text(encoding="utf-8").strip()
        start, end = raw.find("{"), raw.rfind("}")
        result = json.loads(raw[start:end + 1])
        prompt_sha = hashlib.sha256(build_prompt(contract).encode("utf-8")).hexdigest()
        draft_doc = ingest(result, model=args.model, runner=args.runner, prompt_sha256=prompt_sha, contract=contract)
        _print_report(draft_doc["verification"])
        if not draft_doc["verification"]["ok"]:
            print("refusing to write a draft that fails verification", file=sys.stderr)
            return 1
        args.out.write_text(json.dumps(draft_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
        return 0
    if args.command == "verify":
        draft_doc = json.loads(DRAFT_PATH.read_text(encoding="utf-8"))
        verification = verify(draft_doc, contract)
        _print_report(verification)
        return 0 if verification["ok"] else 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
