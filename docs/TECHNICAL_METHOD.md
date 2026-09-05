# Technical Method And Claim Contract

## Analyses

### Lagged within-person comparison

For a binary daily exposure, the engine pairs each exposure day with an outcome a configurable number of days later. The displayed effect is:

```text
mean(outcome | exposure on) - mean(outcome | exposure off)
```

The demo uses a one-day lag so a caffeine-timing decision is paired with the following night's recovery outcome.

### Confidence interval

The default 95% interval uses a deterministic moving-block bootstrap over seven consecutive **available lagged pairs**. Missing calendar days are not imputed; a seven-pair block can therefore span more than seven calendar days. This preserves some short-range ordering, but does not guarantee intact weekly calendar structure. The displayed bounds are the 2.5th and 97.5th percentiles across 3,000 reproducible samples. The estimator and the main synthetic demo's values are unchanged in the September 5 iteration; this description corrects the earlier "seven-day" wording.

For fewer than eight paired observations, when both conditions have at least two observations, the engine falls back to the independent-groups approximation:

```text
effect +/- 1.96 * sqrt(variance_on / n_on + variance_off / n_off)
```

The interval quantifies uncertainty in the observed comparison. It does not make the estimate causal or fully correct for time-varying confounding.

If either condition has only one observation, the descriptive mean difference is retained but interval bounds are `null`; a singleton cannot supply a within-condition variance estimate. If either condition has no paired outcomes, the difference is also `null`. Empty input produces an explicit unavailable comparison, empty dates, and no dated experiment schedule.

### Dose-response correlation

The engine reports Pearson's `r` between a continuous exposure and a lagged outcome. Its 95% interval uses Fisher's z transformation. Correlation remains association, even when lagged.

### Trends

The most recent seven days are compared with the preceding 28-day baseline. At least three recent and ten baseline observations are required before a trend receives an observed status.

### PhenoAge

PhenoAge is calculated only when all nine clinical biomarkers and chronological age are available. Missing inputs produce an error rather than an imputed result. The output is labeled educational and is not presented as a diagnosis, clinical age, or individualized mortality prediction.

## Data-Quality Checks

Before calculation, every analysis entry point validates daily records and returns a date-sorted copy without mutating the caller. Duplicate dates, non-canonical or invalid calendar dates, non-numeric/non-finite values, and invalid lag/window parameters raise errors instead of silently changing the evidence. CSV loading accepts a UTF-8 BOM and blank numeric cells, but rejects missing/duplicate headers and row-width mismatches.

- Calendar coverage across the observation window.
- Minimum paired samples in each condition.
- Condition imbalance.
- Exposure days missing a paired outcome.
- A targeted alcohol-condition difference as a known recovery confounder.
- An unavoidable observational-data penalty.

The quality grade is deterministic. GPT-5.6 cannot raise it or suppress its warnings.

## Care Brief Handoff

Schema `1.1` copies the primary and secondary effects, quality contract, calculation provenance, and claim boundary without recomputing them. It also retains source roles and field coverage, warnings, missing evidence, clinician questions, experiment controls and stop conditions, and the AI contract. Unknown provenance stays `unspecified`; PHI status is `null` unless explicitly supplied. Only the synthetic demo builder supplies the fictional persona and a `contains_phi: false` declaration.

Readiness has three workflow states:

- **Comparison unavailable:** at least one condition lacks a paired outcome.
- **Evidence has review gaps:** an estimate exists, but either condition has fewer than 10 paired observations, an interval is unavailable, the quality score is below 75, or a comparison-source link is missing.
- **Ready to review:** the preceding checks pass. An interval including zero is still explicitly inconclusive; a lower HRV estimate remains lower. This status does not establish clinical relevance, validate provenance, or recommend action.

Optional laboratory and genomic context count as supplied only when a usable snapshot or marker context is present. They do not validate the primary association. Source URLs are caller-supplied references, limited to HTTP(S), rather than evidence of independent source verification.

Markdown export carries a readable summary plus the complete JSON contract; JSON export is the contract itself. The browser requests a local file download only after a user clicks. Printing expands missing-evidence details for the print cycle. No record is uploaded or sent to a clinician by these controls.

The recovery chart uses each outcome date's **previous calendar day** for its condition color. Missing prior-day logs are gray. Horizontal spacing and the rolling mean use actual calendar dates; the mean includes available values in the trailing seven calendar days.

## Derived Annotations

Generated by code:

- Effect sizes, intervals, sample counts, means, trend deltas, correlations, quality score, grade, warnings, PhenoAge, schedule, and fixture-derived marker call.

Generated by GPT-5.6:

- The plain-English question, source-supported scientific context, practical explanation, blind spots, alternative hypotheses, and adaptation of the draft experiment to user constraints.

GPT-5.6 receives `analysis.json` as an immutable calculation contract. It must preserve the values and label any additional interpretation as inference.

## Explicit Claim Boundary

LiveForever may say `observed association`, `promising, not proven`, `inconclusive`, and `replicate before acting`. It must not say an exposure caused an outcome, that a genotype proves a trait, or that the user should change medication, supplements, or clinical care.
