# Care Brief engineering iteration — September 5, 2026

This work strengthens the **pending Break the Barrier 2026 entry**. It is a post-Build-Week iteration in the independent `liveforever-care-brief` repository, based on commit `e112fa9cf8c1b4beb2bb3a76496e1b09368ef2ea`. It is not represented as work in the original judged Build Week submission. Historical submission documents, screenshots, `demo/index-buildweek.html`, and the original submission commit remain untouched.

## Design and order

1. Reproduce and correct the evidence-handoff defects.
2. Add deterministic review readiness, honest provenance, source coverage, and local exports to the existing interface.
3. Check synthetic failure cases, preserve the main demo's results, and document the pending-entry boundary.

## Changes and rationale

| Files | Before | After |
|---|---|---|
| `src/liveforever_lab/care_brief.py` | A missing primary estimate crashed numeric formatting. Negative HRV differences were described as "higher"; every brief claimed a recovery pattern worth retesting. | Schema `1.1` distinguishes unavailable comparisons, early estimates, unavailable intervals, inconclusive intervals, and higher/lower observed HRV. Visit framing follows the actual evidence and leaves clinical relevance open. |
| `src/liveforever_lab/care_brief.py`, `synthetic.py`, `cli.py` | Provenance always said synthetic and PHI-free, including absent context or unspecified inputs. Source ledger entries had no links or field counts. | Only the synthetic builder supplies `DEMO_PROVENANCE`. Other callers default to an unspecified record type, unknown PHI status, and no invented persona. Source rows retain explicit roles, actual field counts, availability, and HTTP(S) references. Missing optional context is not counted as supplied or linked. |
| `src/liveforever_lab/care_brief.py` | The handoff was viewable/printable only; individual quality warnings lived outside the Care Brief. | `export_care_brief()` returns complete JSON or readable Markdown with the full JSON contract attached. Primary/secondary effects, warnings, sources, uncertainty, missing evidence, clinician questions, calculation provenance, plan schedule/controls/stop conditions, and AI boundaries survive export. Text generation does not write or transmit files. |
| `demo/portfolio.js`, `portfolio.css` | No export controls or clear evidence-readiness summary. The Care Brief omitted supporting-outcome sample counts and explicit warning text. | Local Markdown/JSON download buttons, accessible request status, readiness summary, source inspection links, visible warnings, and a supporting-outcomes table. The existing visual design remains in place. Printed briefs expand missing-evidence details for the print cycle. |
| `src/liveforever_lab/analysis.py`, `planner.py` | Empty analysis crashed; a singleton could yield false interval precision. Input duplicates silently replaced a day's record, and invalid/non-finite input could corrupt calculations or JSON. | Empty analysis produces a complete unavailable contract and no dated schedule. Singleton conditions retain the descriptive difference with null interval bounds. Shared public-engine input validation rejects duplicate dates, malformed dates, non-finite values, ambiguous CSV headers/rows, and invalid parameters; it sorts a copy without changing the caller's records. UTF-8 BOMs and blank numeric cells are supported. |
| `src/liveforever_lab/analysis.py`, `demo/portfolio.js` | The chart claimed prior-day timing but colored observations with the same day's exposure; the "7-day" line averaged seven available rows. | `prior_day_caffeine_cutoff_2pm` uses the exact previous calendar day. Missing exposure context is gray. Chart spacing and the trailing mean use calendar dates. Null/absent metrics and empty timelines show unavailable states instead of zero, NaN, or an exception. |
| `demo/portfolio.js`, `care_brief.py` | Dynamic strings were concatenated into HTML; source references had no allowed-scheme boundary. | Display strings are escaped; source URLs are restricted to HTTP(S); Markdown escapes presentation text and uses a fence long enough to safely retain a complete contract. These are output boundaries, not a general data-import interface. |
| `README.md`, `docs/TECHNICAL_METHOD.md`, `docs/README.md` | Instructions and test counts covered the initial print-only brief; bootstrap wording implied seven uninterrupted calendar days. | Current export/review instructions, test commands, local failure-case preview, precise readiness rules, and correct "seven consecutive available pairs" bootstrap wording. Historical submission documents remain unchanged. |

The input-validation helper and relevant regression cases were aligned with the parallel September 5 work in the public Build Week repository, read only as an implementation reference. Care Brief preserves its intentional empty-contract behavior and explicit provenance, which differ from that repository's empty-input API.

## Main demonstration preserved

Regenerated the synthetic payload with `PYTHONPATH=src python3.11 -m liveforever_lab.cli`. A direct JSON comparison against the baseline commit confirmed exact equality for:

- Primary HRV: **+3.94 ms**, 95% interval **+1.13 to +6.42**, **36 / 37** paired observations.
- Sleep: **+0.30 h**, 95% interval **+0.05 to +0.56**, **37 / 38** observations.
- Resting heart rate: **−1.38 bpm**, 95% interval **−2.26 to −0.45**, **37 / 38** observations.
- All dose-response values, trends, quality fields (**B, 85/100**), genomic/laboratory context, and the full experiment plan.

The synthetic input fixtures have no diff. Changes to `demo/analysis.json` add provenance, coverage, the lag-correct chart field, the revised Care Brief, and pre-generated Markdown. The underlying bootstrap estimator and its random seed are unchanged. The only intentional numerical-contract change is for degenerate singleton inputs, which now have no claimed interval precision.

## Validation performed

- Baseline suite: **17 tests passed** before edits. Reproduced the missing-condition `TypeError` and the "−3.94 ms higher" wording before repairing them.
- Final Python suite: `PYTHONPATH=src python3.11 -m unittest discover -s tests -v` — **41 tests passed**. Covers lag pairing, exact synthetic results, zero/negative/inconclusive/missing/small samples, no-record contracts, unknown provenance, missing context, source schemes, export integrity, no mutation, duplicates/non-finite values, canonical dates, CSV ambiguity/BOMs, and analysis parameters.
- `node --check demo/portfolio.js` — passed.
- `node tests/test_demo_ui.cjs` — passed using only the installed Node standard library. Verifies the actual download Blob contents and filenames against the full JSON/Markdown payload, MIME types, escaped strings, missing context/outcomes, empty charts, and absent-export behavior.
- `git diff --check` — passed.
- All four source links in the regenerated brief point to existing checked-in fixture paths. The Markdown contract appendix decodes to exactly the JSON Care Brief.
- In-app browser at **1280 px** and **390 × 844**: no page-width overflow; Care Brief readiness, warnings, source links, and export controls visible. Both export buttons produced their correctly named request status with no console errors. HRV/Sleep toggling and keyboard chart details worked; focus moved to the selected view heading.
- Browser failure scenarios via `tests/preview_scenarios.py`: negative data displayed **3.94 ms lower** with neutral styling; the small case showed **4 / 1** observations and no interval; missing-condition data showed an unavailable comparison; empty data showed **0 / 4** sources, unavailable metrics/chart, and no fabricated schedule. No console errors were observed.
- New settled desktop screenshot: [`liveforever-care-brief-2026-09-05.png`](liveforever-care-brief-2026-09-05.png). Earlier screenshots are preserved.

## Limits and remaining validation

- This remains a synthetic, static workflow prototype. No live model, external health service, private health repository, or real health record was used. No new dependencies were installed.
- Readiness is a transparent workflow heuristic, not a validated clinical score, a source-authenticity check, or a recommendation to act. It requires both conditions to reach 10 paired observations, an available interval, quality score at least 75, and linked comparison sources; optional context is reported separately.
- Source links are explicit references rather than independently verified clinical records. Public fixture links use the repository's `main` branch and can change if those fixtures change later.
- The seven-pair moving-block bootstrap still compresses calendar gaps; it is not a full time-series or confounding model. The correction here is accurate labeling, not a new estimator.
- The in-app browser's download-event observer timed out for the Markdown Blob even though the control reached its request status. Native save completion was therefore **not** claimed. Export bytes, filenames, and MIME types are verified independently by the JavaScript regression check. A native save-dialog/PDF-printer workflow was not automated.
- JSON export contains the complete contract. Markdown intentionally repeats that contract in an appendix for traceability, so it is longer than the screen summary. No user-selected omission of sources or warnings is offered.
- Public publication, submission, and clinical/workflow efficacy validation remain separate from this local engineering iteration. This worker did not commit, push, or deploy the changes.
