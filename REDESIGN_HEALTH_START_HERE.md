# Redesign Health / Break the Barrier — Start Here

**Deadline:** November 1, 2026 at 11:59 PM Eastern

**Status:** Product extension published independently; video and form submission intentionally deferred.

**Repository:** `bakulbadwal/liveforever-care-brief`

**Core implementation commit:** `13d7dd9` (`Build source-linked LiveForever Care Brief`)

**Latest demo iteration commit:** `d3c665a` (`Ship a cached, verified AI draft and show the verification on the page`)

## Official submission form

**[Open the Break the Barrier submission form](https://docs.google.com/forms/d/e/1FAIpQLSc8nLhq33YpQeZ_pcFWJqFYFV6cJq-v8RLKfJ0zEG0KSWBcQA/viewform?pli=1)**

This is the direct Google Form URL. The form may retain a draft under the Google account used to open it, but all paste-ready answers are also preserved locally below.

## What the project is

**Name:** LiveForever Care Brief

**One-line description:** A privacy-first AI workflow that turns fragmented longitudinal health data into a source-linked personal evidence brief for clinician review.

**Core healthcare barrier:** Patients accumulate years of wearable, habit, laboratory, medication, training, and genomic context, but very little of it becomes concise and usable during a short clinical visit.

**Product response:** Deterministic Python owns every calculation, interval, quality check, and source status. A bounded AI layer explains the locked evidence, surfaces missing context and alternative hypotheses, and prepares questions for clinician review. The user reviews the brief and controls whether it is printed or shared.

**Current stage:** Working public prototype with synthetic longitudinal data, a tested Python evidence engine, an immutable Care Brief contract, a bounded AI workflow with a cached AI draft verified against the contract at build time, a Trace values switch that reveals the contract path behind each locked number, a responsive interface in the quick-reference-handbook design, technical documentation, and 51 automated tests.

## What has already been built

- The previously prepared portfolio redesign.
- A deterministic `care_brief` contract generated from the analysis and experiment plan.
- A source ledger covering wearables, habit logs, laboratory context, and genomic hypothesis context.
- Explicit uncertainty, missing-evidence, and clinician-question sections.
- AI permissions and prohibitions, including immutable calculation paths.
- A dedicated responsive Care Brief interface with a user-controlled print flow.
- Updated README, case study, provenance, screenshot, and competition framing.
- The October 10 handbook redesign (recorded in `DESIGN.md`), the Trace values switch, and the cached AI draft (`demo/ai_draft.json`) with its deterministic verifier (`src/liveforever_lab/ai_draft.py`).
- Fifty-one passing Python tests, the Node browser-code checks, and desktop/mobile browser verification.

The public demo contains one fictional persona, Maya Chen, and no PHI. It does not claim clinical validation, diagnosis, treatment, EHR integration, or real patient outcomes.

## Resume this later in five steps

1. Open the independent public demo and verify the Care Brief is still the default view.
2. Record the new 3.5- to 4.5-minute MP4 using the prepared script. The dated recording script lives locally at `~/Desktop/Hackathons/1-break-the-barrier/SCRIPT-2026-10-10.md`; `docs/BREAK_THE_BARRIER_DEMO_SCRIPT.md` keeps the reference timings. The old Build Week video does not show the Care Brief and should not be reused as the primary submission.
3. Paste the prepared bio and Healthcare Problem Scope & Impact response into the Google Form.
4. Upload the MP4, review the terms yourself, submit, and retain the emailed receipt.
5. If the product changes before November 1, resubmit the form; only the most recent entry is evaluated.

## Submission files

- [`docs/BREAK_THE_BARRIER_SUBMISSION.md`](docs/BREAK_THE_BARRIER_SUBMISSION.md) — exact paste-ready form answers and positioning.
- [`docs/BREAK_THE_BARRIER_DEMO_SCRIPT.md`](docs/BREAK_THE_BARRIER_DEMO_SCRIPT.md) — reference screen order and timings; the current recording script is local at `~/Desktop/Hackathons/1-break-the-barrier/SCRIPT-2026-10-10.md`.
- [`docs/BREAK_THE_BARRIER_CHECKLIST.md`](docs/BREAK_THE_BARRIER_CHECKLIST.md) — final recording and submission checklist.
- [`docs/BREAK_THE_BARRIER_PROVENANCE.md`](docs/BREAK_THE_BARRIER_PROVENANCE.md) — what existed before and what this extension added.
- [`docs/liveforever-care-brief-hero.png`](docs/liveforever-care-brief-hero.png) — README hero image: the Care brief as served by the live demo on 2026-10-10.
- [`docs/liveforever-care-brief-v2.png`](docs/liveforever-care-brief-v2.png) — current desktop Care Brief viewport in the handbook design, captured 2026-10-10 (the same capture as `docs/liveforever-care-brief-2026-10-10.png`).
- [`docs/liveforever-care-brief-ai-draft-2026-10-10.png`](docs/liveforever-care-brief-ai-draft-2026-10-10.png) — the cached AI draft block with Trace values on.
- [`docs/liveforever-care-brief-mobile.png`](docs/liveforever-care-brief-mobile.png) — current mobile Care Brief screenshot (390px wide, captured 2026-10-10).
- [`README.md`](README.md) — public product and technical overview.
- [`CASE_STUDY.md`](CASE_STUDY.md) — product rationale and tradeoffs.

## Video versus deck

Use a **new product-demo video** as the one required upload. It demonstrates the working product and the healthcare workflow more strongly than a standalone deck. A short deck is optional and useful only as visual support inside the video or for later conversations; the form accepts one primary MP4, PDF, or PPTX upload, and its optional Drive material is not used to determine finalists.

## Repository strategy

Use an independent public repository for the Break the Barrier product while retaining the original Git history and explicit provenance. This keeps the frozen OpenAI submission and its deployment untouched, gives the healthcare workflow its own `main` branch and Pages URL, and still makes the evolution auditable. This is a new repository, not a GitHub fork; forks are primarily for contributing back to someone else's repository.
