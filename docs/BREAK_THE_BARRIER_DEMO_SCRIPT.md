# LiveForever Care Brief — Demo Script

Target length: **3:45 to 4:20**. Record a clean screen walkthrough; camera bubble is optional. Upload the resulting MP4 directly to the form.

## 0:00–0:35 — The barrier

**Show:** Snapshot view, with the full interface visible.

“People accumulate years of health context across wearables, laboratory portals, habit logs, and genomic files, but very little of it becomes useful during a short clinical visit. Patients arrive with memory and screenshots; clinicians receive either too little context or an unstructured data dump. LiveForever turns one longitudinal question into traceable evidence and a concise brief for review.”

## 0:35–1:20 — The working evidence engine

**Show:** Primary result, supporting metrics, then toggle HRV to Sleep and hover one chart point.

“This public prototype follows Maya Chen, a completely fictional persona. Her question is whether stopping caffeine by 2 PM is associated with next-day recovery. Tested Python pairs each habit day with the following night, calculates the effect and uncertainty, and checks coverage, sample size, balance, and possible confounders. Here the synthetic record shows a 3.94 millisecond HRV difference across 73 paired nights, with the interval and supporting sleep and resting-heart-rate results visible. This is labeled as an association, not a causal or clinical conclusion.”

## 1:20–2:35 — The Care Brief

**Show:** Open Care brief. Scroll slowly from the header through evidence, uncertainty, and clinician questions.

“The Break the Barrier extension is this Care Brief. It converts the same fixed analysis into a patient-controlled clinical handoff. The question and numerical signal appear first. Every source has a ledger entry explaining what it contributed. Uncertainty and missing evidence stay attached instead of disappearing into a disclaimer. The AI prepares questions a clinician can review, such as whether the pattern is meaningful in the broader history and what other context could better explain it.”

**Pause over the locked-values callout.**

“The core safety design is a separation of authority. Deterministic code owns every value, sample count, warning, and source. AI can explain the evidence, surface missing context, and organize the brief, but it cannot alter a number, invent a source, diagnose, or prescribe. The user reviews the draft and chooses whether to print or share it; this demo transmits nothing.”

## 2:35–3:15 — Better next action

**Show:** Experiment view and the balanced 14-day schedule.

“When the evidence is worth revisiting, LiveForever proposes a balanced replication plan rather than a recommendation. Controls, pause conditions, and the decision rule are defined before the retest. A clinician can help determine whether the experiment is appropriate or should change.”

## 3:15–3:50 — Trust and implementation

**Show:** Data & methods, connected data, quality warnings, then open calculation provenance.

“The demonstration runs with no login, API key, database, or personal health information. All records are synthetic. The public repository includes the Python engine, immutable care-brief contract, bounded AI Skill, technical method, and 17 automated tests. A production version would need secure connectors, consent and deletion controls, access management, and clinical validation before accepting PHI.”

## 3:50–4:15 — Close

**Show:** Return to Care brief, then end on a slide or browser tab with the URLs below.

“LiveForever is designed to help people bring a better question and a traceable signal into care, while leaving medical judgment where it belongs. I’m Bakul Badwal, a former founder, investor, UVA Darden MBA candidate, and applied AI builder. Thank you.”

Final frame:

- **LiveForever Care Brief**
- `bakulbadwal.github.io/liveforever-buildweek/#care`
- `github.com/bakulbadwal/liveforever-buildweek`
- Bakul Badwal · UVA Darden MBA '27
