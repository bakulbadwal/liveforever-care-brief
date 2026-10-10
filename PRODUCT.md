# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

- **Primary:** a serious self-tracker with years of wearable, habit, laboratory, and genomic context, preparing for a short clinical visit. Job: turn that history into one answerable question, see how uncertain the signal is, and carry a concise, traceable brief into the conversation.
- **Reviewer:** a clinician glancing at the brief during or before a visit. Job: scan the question, the observed signal, the source ledger, and the uncertainty in seconds; supply the medical judgment the product deliberately does not.
- **Evaluator (current, time-bounded):** Redesign Health's investment team judging the Break the Barrier 2026 entry from a 3–5 minute screen recording plus a barrier statement. They score "highest potential to transform healthcare," "most innovative application of technology," and "greatest impact on patient care," and they are explicitly looking for founders who understand a real problem. *(Source: inventacare.com FAQ, read 2026-09-16.)*

## Product Purpose

LiveForever Care Brief turns fragmented longitudinal health data into a source-linked personal evidence brief for clinician review. It exists because patients compress years of context into a fifteen-minute visit while clinicians receive either recollection or an unstructured export. Success: the person arrives with a better question and a traceable signal; the clinician reviews relevant context faster; medical judgment stays with the clinician.

## Positioning

Deterministic Python owns every number — effect sizes, intervals, lags, sample counts, missingness, quality grades, PhenoAge, the experiment schedule, source status. A bounded AI layer may explain the locked evidence, surface missing context and alternative hypotheses, and prepare clinician questions; it may not alter, recompute, omit, or invent a value or source, diagnose, prescribe, or convert an association into a causal or clinical claim. The boundary is written into the Care Brief contract (`care_brief.ai_contract`: allowed actions, forbidden actions, immutable paths, human gate) and rendered on the page. Most health-AI products ask the user to trust the model's insight; this one is built so they don't have to. It is not a diagnosis engine and is designed not to become one.

## Operating Context

- Static GitHub Pages site at `bakulbadwal.github.io/liveforever-care-brief/#care`; no login, API key, backend, database, or live model call. Public repository `bakulbadwal/liveforever-care-brief`, MIT.
- Four views in one page: **Snapshot** (primary result, supporting metrics, recovery timeline chart with HRV/Sleep toggle), **Care brief** (the document: readiness, observed signal, locked-values callout, source ledger, uncertainty, supporting outcomes, clinician questions, bounded-AI contract ledger, exports), **Experiment** (balanced 14-day retest schedule, predefined controls, decision rule, pause conditions), **Data & methods** (evidence grade, connected data, quality warnings, personal context incl. CYP1A2 and PhenoAge, calculation provenance).
- The brief is exported by the user as Markdown, JSON, or print; nothing is transmitted.
- Evaluation scene: a 1080p screen recording at ~125% zoom, narrated from `SCRIPT-2026-09-19.md`, which cues specific on-screen labels (tab names, "Prepare care brief", "Values locked by code", sections 01 Sources supplied / 02 What remains uncertain / 03 Questions for a clinician, "Show calculation and provenance", "When to pause", Download Markdown / JSON / Print brief, "Inspect the contract").
- Engine: Python 3.11, no runtime dependencies; `PYTHONPATH=src python3.11 -m liveforever_lab.cli` regenerates fixtures and `demo/analysis.json`; 41 unit tests plus a dependency-free Node UI regression (`tests/test_demo_ui.cjs`).

## Capabilities and Constraints

- One question at a time, with exposure, outcome, lag, and minimum sample defined before interpretation. Demo question: does stopping caffeine by 2 PM improve next-day recovery? Result: +3.94 ms HRV across 73 paired nights (95% interval +1.13 to +6.42; 36 cutoff / 37 usual), sleep +0.30 h, resting HR −1.38 bpm, evidence grade B (85/100), 95% calendar coverage, 4 of 4 sources supplied.
- All records belong to **Maya Chen, a fictional persona**; every signal is deliberately generated. No PHI anywhere in the repository, demo, screenshots, or exports.
- Must never claim clinical validation, diagnosis, treatment, EHR integration, or real patient outcomes. Results are labeled "association only"; genomic and laboratory context prioritize questions and never determine recommendations.
- Production would require consent, identity, deletion, access controls, security review, and clinical workflow validation before accepting PHI.
- The bounded AI layer is present in the demo as a cached draft (`demo/ai_draft.json`): generated once at build time from the locked contract under the Skill's prompt, verified by `liveforever_lab.ai_draft` before it can ship (every cited number must exist in the contract at the contract's rounding; affirmative diagnostic, prescriptive, causal, proof, or treatment language is flagged; the draft carries the SHA-256 of its contract). The shipped draft was written by Claude Fable 5.1 on 2026-10-10; the Skill targets GPT-5.6 through Codex; the contract and verifier are model-agnostic. The hosted demo makes no live model calls.
- `demo/analysis.json` is generated output and is not hand-edited. All on-page copy comes from that contract or from `demo/portfolio.js` templates, deep-escaped before render.
- Video constraint: 3–5 minutes, judged in one batch after Nov 1, 2026 (finalists Dec 1).

## Brand Commitments

- Name: **LiveForever Care Brief** (product), **LiveForever** (project). Author: Bakul Badwal, UVA Darden MBA '27.
- Voice: plain, exact, restrained; states limits unprompted ("Draft for clinician review; not medical advice"). Every number is shown with its interval and sample.
- Existing mark: the "LF" monogram in the sidebar. *(Inference, not user-confirmed: no logo file beyond `favicon.svg` exists; the monogram is a placeholder, not a binding asset.)*
- Semantic color meanings already present in the UI and worth preserving as meanings, not hues: green = verified / locked / the signal; coral = negative direction or prohibition; gold = caution and quality warnings; blue = the AI layer and next steps.

## Evidence on Hand

- `demo/analysis.json` — the full generated contract (analysis, plan, care_brief, exports).
- `demo/ai_draft.json` — the cached, verified AI draft with provenance and the verification result.
- `docs/liveforever-care-brief-hero.png`, `docs/liveforever-care-brief-v2.png`, `docs/liveforever-care-brief-mobile.png`, `docs/liveforever-care-brief-2026-09-05.png` — current-look screenshots.
- `CASE_STUDY.md`, `docs/TECHNICAL_METHOD.md`, `docs/BREAK_THE_BARRIER_*.md` — rationale, method, provenance, submission answers.
- Cited literature for CYP1A2 in README (systematic review and meta-analysis links).
- **Absent, do not fabricate:** clinician testimonials, real patient data, outcome metrics, pilot results, partners, pricing, customers.

## Product Principles

1. Code owns the numbers; the model explains them; the person decides. Never blur the three.
2. Uncertainty is part of the interface, not a disclaimer beneath it.
3. One question, one comparison, one next test — no correlation fishing.
4. Restraint is the credibility signal: say what the product is not, unprompted.
5. Everything the clinician sees must trace to a source and a sample.

## Accessibility & Inclusion

- Keyboard-navigable views and chart points (Tab reveals individual observations); `aria-labelledby` on sections and the chart; `.sr-only` announcements; focus-visible outlines; reduced-motion media query; print stylesheet for the brief.
