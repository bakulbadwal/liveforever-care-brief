# Break the Barrier Extension Provenance

## Preserved starting point

- OpenAI Build Week judged commit: `6978bcdddb418af799d6023c1d4b1b36c2fcf4a7`
- Post-submission presentation redesign base: `cf824e6fd178677b476fe40866c755fe71c0b6d8`
- Preserved submitted interface: `demo/index-buildweek.html`

The original submission, private personal-health prototype, personal records, and private data connectors are not presented as new Break the Barrier work.

## New healthcare workflow

The `break-the-barrier-care-brief` branch adds:

- `src/liveforever_lab/care_brief.py`, a deterministic care-brief contract.
- A locked evidence summary that preserves the original analysis values verbatim.
- A four-source provenance ledger.
- Explicit uncertainty, missing-evidence, clinician-question, privacy, and human-review sections.
- An AI contract with immutable paths, allowed actions, forbidden actions, and a human sharing gate.
- A responsive Care Brief interface and user-controlled print path.
- Six focused care-brief tests.
- A healthcare-specific form package and under-five-minute demo script.

## What did not change

- No personal data was added.
- No synthetic analytical result was altered to improve the story.
- No diagnosis, treatment recommendation, live clinical integration, or validated outcome is claimed.
- No browser-side API key, backend account, database, or automatic health-data transmission was introduced.

## Model-versus-code boundary

Deterministic Python owns effects, intervals, sample counts, data-quality warnings, source status, and the initial experiment design. The AI workflow may explain those fixed inputs, identify missing context and alternative hypotheses, and prepare clinician questions. It may not recompute values, invent evidence, diagnose, prescribe, or imply clinical review.
