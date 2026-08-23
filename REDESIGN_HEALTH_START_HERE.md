# Redesign Health / Break the Barrier — Start Here

**Deadline:** November 1, 2026 at 11:59 PM Eastern  
**Status:** Product extension built and committed locally; video and form submission intentionally deferred.  
**Local branch:** `break-the-barrier-care-brief`  
**Core implementation commit:** `13d7dd9` (`Build source-linked LiveForever Care Brief`)

## Official submission form

**[Open the Break the Barrier submission form](https://docs.google.com/forms/d/e/1FAIpQLSc8nLhq33YpQeZ_pcFWJqFYFV6cJq-v8RLKfJ0zEG0KSWBcQA/viewform?pli=1)**

This is the direct Google Form URL. The form may retain a draft under the Google account used to open it, but all paste-ready answers are also preserved locally below.

## What the project is

**Name:** LiveForever Care Brief

**One-line description:** A privacy-first AI workflow that turns fragmented longitudinal health data into a source-linked personal evidence brief for clinician review.

**Core healthcare barrier:** Patients accumulate years of wearable, habit, laboratory, medication, training, and genomic context, but very little of it becomes concise and usable during a short clinical visit.

**Product response:** Deterministic Python owns every calculation, interval, quality check, and source status. A bounded AI layer explains the locked evidence, surfaces missing context and alternative hypotheses, and prepares questions for clinician review. The user reviews the brief and controls whether it is printed or shared.

**Current stage:** Working public prototype with synthetic longitudinal data, a tested Python evidence engine, an immutable Care Brief contract, a bounded AI workflow, a responsive interface, technical documentation, and 17 automated tests.

## What has already been built

- The previously prepared portfolio redesign.
- A deterministic `care_brief` contract generated from the analysis and experiment plan.
- A source ledger covering wearables, habit logs, laboratory context, and genomic hypothesis context.
- Explicit uncertainty, missing-evidence, and clinician-question sections.
- AI permissions and prohibitions, including immutable calculation paths.
- A dedicated responsive Care Brief interface with a user-controlled print flow.
- Updated README, case study, provenance, screenshot, and competition framing.
- Seventeen passing tests and desktop/mobile browser verification.

The public demo contains one fictional persona, Maya Chen, and no PHI. It does not claim clinical validation, diagnosis, treatment, EHR integration, or real patient outcomes.

## Resume this later in five steps

1. Confirm that the OpenAI Build Week repository freeze has ended after the Aug. 25 winners announcement.
2. Push `break-the-barrier-care-brief` to the existing public repository, then merge it into `main` when ready to update the hosted demo.
3. Record the new 3.5- to 4.5-minute MP4 using the prepared script. The old Build Week video does not show the Care Brief and should not be reused as the primary submission.
4. Paste the prepared bio and Healthcare Problem Scope & Impact response into the Google Form.
5. Upload the MP4, review the terms yourself, submit, and retain the emailed receipt.

## Submission files

- [`docs/BREAK_THE_BARRIER_SUBMISSION.md`](docs/BREAK_THE_BARRIER_SUBMISSION.md) — exact paste-ready form answers and positioning.
- [`docs/BREAK_THE_BARRIER_DEMO_SCRIPT.md`](docs/BREAK_THE_BARRIER_DEMO_SCRIPT.md) — timed screen order and narration.
- [`docs/BREAK_THE_BARRIER_CHECKLIST.md`](docs/BREAK_THE_BARRIER_CHECKLIST.md) — final recording and submission checklist.
- [`docs/BREAK_THE_BARRIER_PROVENANCE.md`](docs/BREAK_THE_BARRIER_PROVENANCE.md) — what existed before and what this extension added.
- [`docs/liveforever-care-brief.png`](docs/liveforever-care-brief.png) — current Care Brief hero image.
- [`README.md`](README.md) — public product and technical overview.
- [`CASE_STUDY.md`](CASE_STUDY.md) — product rationale and tradeoffs.

## Video versus deck

Use a **new product-demo video** as the one required upload. It demonstrates the working product and the healthcare workflow more strongly than a standalone deck. A short deck is optional and useful only as visual support inside the video or for later conversations; the form accepts one primary MP4, PDF, or PPTX upload, and its optional Drive material is not used to determine finalists.

## Repository strategy

Keep this as an evolution of the existing LiveForever repository rather than creating a fork or duplicate repository. The branch and provenance file separate the healthcare extension from the frozen OpenAI submission while preserving one coherent product history. A fork is designed mainly for contributing back to someone else's repository and adds no value here.
