# Break the Barrier Submission Package

## Recommended entry

Submit **LiveForever Care Brief** as a materially evolved version of the existing public prototype. The OpenAI Build Week submission remains preserved at its frozen commit; this branch adds a distinct healthcare workflow focused on patient-to-clinician review.

## Form answers

### Full Name

Bakul Badwal

### Preferred Contact Email

badwalb@gmail.com

### 1-Sentence Bio

UVA Darden MBA candidate, former founder, investor, and applied AI builder developing privacy-first tools that turn complex personal data into trustworthy decisions.

### Teammates

Leave blank. This is a solo submission.

### Healthcare Problem Scope & Impact

People accumulate health information across wearables, laboratory portals, medication and supplement logs, training records, and genomic files, but that history rarely becomes usable during a clinical visit. Patients must compress years of context into a short conversation, while clinicians receive incomplete recollections or unstructured exports that are difficult to review. This wastes limited visit time, obscures potentially relevant trends, and creates an opening for general-purpose AI to produce confident conclusions unsupported by the underlying evidence. LiveForever addresses this barrier by converting longitudinal records into a concise, source-linked personal evidence brief that preserves uncertainty and keeps every calculated result reproducible. Solving this would help patients prepare better questions, help clinicians review relevant context more efficiently, and create a safer bridge between patient-generated data and professional care without allowing AI to diagnose or prescribe.

### Solution summary

LiveForever combines a deterministic evidence engine with bounded AI interpretation. A user asks a question about longitudinal history; tested Python identifies relevant records, calculates trends and uncertainty, and produces an immutable evidence contract. AI then explains the fixed findings, identifies missing context and alternative hypotheses, and prepares questions for clinician review. It cannot change calculated values, diagnose a condition, prescribe treatment, or invent a source. The Care Brief carries the question, source ledger, uncertainty, and clinician questions into a concise document that the user reviews before choosing whether to print or share it. The public demonstration uses only fictional synthetic data, contains no PHI, and transmits nothing.

### Current stage

Working public prototype with a tested Python evidence engine, synthetic longitudinal health data, a bounded AI workflow, a responsive hosted interface, a source-linked Care Brief, technical documentation, and 17 automated tests.

### LinkedIn

https://www.linkedin.com/in/bakulbadwal/

### Public project links

- Demo: https://bakulbadwal.github.io/liveforever-buildweek/#care
- Repository: https://github.com/bakulbadwal/liveforever-buildweek
- Case study: https://github.com/bakulbadwal/liveforever-buildweek/blob/main/CASE_STUDY.md

The form does not provide a repository field. Put the demo and repository URLs on the video's final frame. The optional Google Drive field is not used to determine finalists, so leave it blank unless a later submission package contains crucial context that cannot fit in the video.

## Upload recommendation

Record a new 3.5- to 4.5-minute MP4 using `BREAK_THE_BARRIER_DEMO_SCRIPT.md`. Do not reuse the OpenAI Build Week video as the primary upload: it predates the Care Brief and emphasizes Codex compliance rather than the healthcare barrier, clinical workflow, founder insight, and evolved product.

## Honest boundaries

- This is a working workflow prototype, not an EHR integration, clinical device, diagnostic system, or validated medical intervention.
- All public data belongs to one fictional synthetic persona.
- The demonstrated caffeine signal is deliberately generated and cannot establish real-world clinical efficacy.
- Production use would require consent, identity, deletion, access controls, security review, and clinical workflow validation before accepting PHI.
