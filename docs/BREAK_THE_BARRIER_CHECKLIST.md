# Break the Barrier Submission Checklist

Deadline: **November 1, 2026 at 11:59 PM Eastern**. Resubmissions are allowed; only the most recent entry is evaluated.

## Before recording

- [ ] Confirm the independent `liveforever-care-brief` repository and hosted Care Brief URL load.
- [ ] Confirm the public page shows only Maya Chen's fictional synthetic record.
- [ ] Run all 51 Python tests (`PYTHONPATH=src python3.11 -m unittest discover -s tests`) and `node tests/test_demo_ui.cjs`; confirm `demo/analysis.json` is regenerated.
- [ ] Run `PYTHONPATH=src python3.11 -m liveforever_lab.ai_draft verify` and confirm the cached draft still matches the contract (17 numbers cited, none unlisted, 0 forbidden claims).
- [ ] Confirm the Care brief's AI draft block reads 26 / 26 numbers cited with "Build-time verifier: passed", and leave Trace values off until the script calls for it.
- [ ] Open four tabs: Snapshot, Care brief, Experiment, and Data & methods.
- [ ] Open the recording script (`~/Desktop/Hackathons/1-break-the-barrier/SCRIPT-2026-10-10.md`; `BREAK_THE_BARRIER_DEMO_SCRIPT.md` keeps the reference timings) on the second monitor.

## Record and upload

- [ ] Record a new 3.5- to 4.5-minute walkthrough as MP4.
- [ ] Explain the healthcare barrier, founder insight, working product, AI role, deterministic boundary, privacy model, impact, and honest limitations.
- [ ] Show the repository and demo URLs on the final frame.
- [ ] Keep the uploaded file below 1 GB.
- [ ] Watch the exported MP4 once at normal speed and verify the text is legible and audio is clear.

## Google Form

- [ ] Primary applicant: Bakul Badwal.
- [ ] Preferred email: `badwalb@gmail.com`.
- [ ] Paste the one-sentence bio from `BREAK_THE_BARRIER_SUBMISSION.md`.
- [ ] Leave teammates blank for a solo entry.
- [ ] Paste the Healthcare Problem Scope & Impact paragraph exactly, then reread it once in the form.
- [ ] Upload the new MP4 as the Solution Submission.
- [ ] Add LinkedIn: `https://www.linkedin.com/in/bakulbadwal/`.
- [ ] Leave the supplemental Google Drive field blank unless genuinely crucial context is missing.
- [ ] Review the competition terms and privacy policy yourself before checking acceptance.
- [ ] Submit and save the emailed response receipt.

## Final integrity check

- [ ] Do not claim clinical validation, EHR integration, diagnosis, treatment, or real patient outcomes.
- [ ] Describe the result as a deliberately generated synthetic signal.
- [ ] Describe the Care Brief as user-controlled and clinician-reviewable, not clinician-approved.
- [ ] Confirm the provenance file links the preserved Build Week artifact and identifies the Care Brief extension.
