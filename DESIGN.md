---
name: LiveForever Care Brief
description: A clinical handoff that behaves like a quick reference handbook — paper, ink rules, condensed caps, and color only as state.
colors:
  paper: "#ffffff"
  ground: "#ebe9e3"
  ground-2: "#f4f3ef"
  ink: "#101315"
  ink-2: "#363c40"
  muted: "#6b7276"
  hair: "#d8d5cd"
  rule: "#101315"
  spine: "#15181b"
  spine-2: "#22262a"
  tab-ink: "#e9e7e1"
  tab-muted: "#9aa0a4"
  signal: "#0f6b57"
  signal-soft: "#e3f0ea"
  caution: "#a86f06"
  caution-soft: "#fbf2dc"
  warn: "#a8351f"
  ai: "#2b5aa5"
  day-on: "#101315"
  day-off: "#ffffff"
  band-text: "#c9ced2"
  band-rule: "#3a4045"
  chart-grid: "#e3e1da"
typography:
  display:
    fontFamily: "Barlow Condensed, Arial Narrow, Impact, sans-serif"
    fontSize: "80px"
    fontWeight: 700
    lineHeight: 0.92
    letterSpacing: "-0.02em"
    fontFeature: "tabular-nums"
  display-sm:
    fontFamily: "Barlow Condensed, Arial Narrow, Impact, sans-serif"
    fontSize: "60px"
    fontWeight: 700
    lineHeight: 0.95
    letterSpacing: "-0.015em"
    fontFeature: "tabular-nums"
  headline:
    fontFamily: "Barlow Condensed, Arial Narrow, Impact, sans-serif"
    fontSize: "46px"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "-0.01em"
  headline-sm:
    fontFamily: "Barlow Condensed, Arial Narrow, Impact, sans-serif"
    fontSize: "36px"
    fontWeight: 600
    lineHeight: 1.02
    letterSpacing: "-0.01em"
    fontFeature: "tabular-nums"
  title:
    fontFamily: "Barlow Condensed, Arial Narrow, Impact, sans-serif"
    fontSize: "30px"
    fontWeight: 600
    lineHeight: 1.05
    letterSpacing: "-0.005em"
  title-sm:
    fontFamily: "Barlow Condensed, Arial Narrow, Impact, sans-serif"
    fontSize: "26px"
    fontWeight: 600
    lineHeight: 1.05
    letterSpacing: "-0.005em"
  title-xs:
    fontFamily: "Barlow Condensed, Arial Narrow, Impact, sans-serif"
    fontSize: "24px"
    fontWeight: 600
    lineHeight: 1.05
    letterSpacing: "-0.005em"
  text-xl:
    fontFamily: "Barlow, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "20px"
    fontWeight: 600
    lineHeight: 1.2
  text-lg:
    fontFamily: "Barlow, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.45
  text-md:
    fontFamily: "Barlow, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.5
  body:
    fontFamily: "Barlow, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.5
  body-sm:
    fontFamily: "Barlow, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
  label-lg:
    fontFamily: "Barlow Condensed, Arial Narrow, Impact, sans-serif"
    fontSize: "13px"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.1em"
  label:
    fontFamily: "Barlow Condensed, Arial Narrow, Impact, sans-serif"
    fontSize: "12px"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.1em"
  mono-lg:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.5
  mono:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    fontSize: "12px"
    fontWeight: 500
    lineHeight: 1.3

rounded:
  none: "0px"
  point: "50%"
spacing:
  hair: "1px"
  rule: "1.5px"
  box: "2px"
  xs: "8px"
  sm: "12px"
  md: "20px"
  lg: "28px"
  xl: "36px"
  gutter: "40px"
components:
  button:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0 16px"
    height: "40px"
  button-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0 16px"
    height: "40px"
  button-primary-hover:
    backgroundColor: "{colors.signal}"
    textColor: "{colors.paper}"
  button-on-band:
    backgroundColor: "transparent"
    textColor: "{colors.paper}"
    rounded: "{rounded.none}"
    padding: "0 16px"
    height: "40px"
  panel:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "24px 28px 26px"
  band-dark:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.none}"
    padding: "22px 36px 24px"
  memory-box:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "16px 20px 18px"
  warning:
    backgroundColor: "{colors.caution-soft}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "12px 14px 12px 40px"
  claim-pill:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.caution}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0 9px"
    height: "26px"
  trace-chip:
    backgroundColor: "{colors.signal-soft}"
    textColor: "{colors.signal}"
    typography: "{typography.mono}"
    rounded: "{rounded.none}"
    padding: "3px 7px"
  nav-tab:
    backgroundColor: "transparent"
    textColor: "{colors.tab-muted}"
    rounded: "{rounded.none}"
    padding: "0 20px 0 56px"
    height: "52px"
  nav-tab-active:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink}"
  segmented:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0 14px"
    height: "36px"
  segmented-active:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
---

# Design System: LiveForever Care Brief

## Overview

**Creative North Star: "The Quick Reference Handbook"**

The interface is a printed clinical checklist page, not a health dashboard. Everything sits on white paper inside a warm grey ground, framed by hairline-to-ink rules and a binder-dark spine of numbered bleed tabs. Titles, labels, tabs, and every large numeral are set in Barlow Condensed; running text is Barlow; contract paths and formulas are the system monospace. Numerals are tabular everywhere they are compared. Items and their values are joined by dotted leaders, the way a checklist joins a step to its response.

Color is state, never decoration. Four hues exist and each carries exactly one meaning: signal green for a locked or verified value and the observed effect, caution amber for quality warnings and the "association only" claim pill, warn red for prohibitions, and one blue for the bounded AI layer's kicker. Everything else is ink on paper. Dark bands (the title band, the sheet footer, the privacy band, the memory item's head bar, the filled cutoff days) are ink with paper text; inside them the labels are paper-toned, not green. Tinted cards, accent stripes, and gradients were rejected and do not appear in the build.

Density is high and even: 1.5px ink rules between major blocks, 1px hairlines between rows, square corners, and soft ambient lifts on the paper sheets so the page reads as sheets lying on a desk rather than floating UI. The one signature interaction is an x-ray: the "Trace values" toggle in the top bar reveals, under every locked number, the exact contract path it came from.

**Key Characteristics:**
- Paper on warm grey ground, ink text, binder-dark spine with numbered tabs
- Barlow Condensed for headings, labels, tabs, and large numerals; Barlow for text; ui-monospace for paths
- Uppercase condensed labels tracked 0.08–0.12em; headings in sentence case
- Tabular numerals on every number that can be compared
- 1.5px ink rules, 1px hairlines, 2px box border on the memory item, radius 0
- Dotted leaders (2px dotted) between an item and its value
- Color only as state: signal, caution, warn, ai
- Trace-values reveal: a mono chip on signal-soft under every `[data-trace]` element

## Colors

A near-monochrome paper-and-ink palette with four semantic hues that are each permitted one job.

### Primary
- **Signal Green** (`signal`, #0f6b57): the locked/verified state. The primary effect numeral, the observed-signal headline, the 7-day mean line in the chart (`stroke="#0f6b57"`, 2.25 wide), the active tab's number, the check square on the memory item's head bar, the disclosure carets, source links, focus outlines, the demo-badge dot, and primary-button hover. Its soft tint (`signal-soft`, #e3f0ea) exists for exactly one purpose: the background of the trace chip.

### Secondary
- **Caution Amber** (`caution`, #a86f06): quality warnings and the "association only" claim pill. The warning box is a 1.5px caution border on `caution-soft` (#fbf2dc) with a filled caution "!" square; the readiness status square is caution by default, signal when reviewable, muted when insufficient.
- **Warn Red** (`warn`, #a8351f): prohibition only. The "AI may not" column heading, its square marker, and its list bullets; the error-state title. It never fills a surface in the build.
- **Bounded-AI Blue** (`ai`, #2b5aa5): one job, the kicker and its 26x2px dash on the Bounded AI band. No fills, no borders, no text beyond that kicker.

### Neutral
- **Paper** (`paper`, #ffffff): every panel, the sheet, buttons at rest, the "usual" schedule day, hollow chart points.
- **Ground** (`ground`, #ebe9e3): the page background behind the sheets and the fill of the active bleed tab, so the active tab reads as flush with the page. **Ground 2** (`ground-2`, #f4f3ef) is the hover wash on journey steps and the trace toggle.
- **Ink** (`ink`, #101315): body text, all ink rules (`rule` is the same value and is used for every 1.5px structural border), dark bands, filled controls, filled chart points, cutoff days (`day-on`). **Ink 2** (`ink-2`, #363c40) is secondary text and ledes; **Muted** (`muted`, #6b7276) is metadata, dotted-leader labels, table heads, and the chart's axis labels and grid text.
- **Hair** (`hair`, #d8d5cd): every 1px row divider, the dotted leader on paper, the legend top rule. **Chart grid** (#e3e1da) is the SVG's gridline stroke.
- **Spine** (`spine`, #15181b) and **Spine 2** (`spine-2`, #22262a): the binder sidebar and its internal rules/hover. **Tab Ink** (`tab-ink`, #e9e7e1) and **Tab Muted** (`tab-muted`, #9aa0a4) are the tab text at rest and the tab number; tab-muted also colors the "timing unavailable" chart point and legend key.
- **Band text** (#c9ced2) and **Band rule** (#3a4045): the running text and the dotted-leader rules inside dark bands (the sheet footer's text is the slightly lighter #d5d9dc; the band leader dots are #3f4549). These are hardcoded in the stylesheet rather than tokenized; treat them as the dark-band greys and do not introduce new ones.

### Named Rules
**The One-Job Rule.** Each hue has exactly one meaning and appears only where that meaning is true: signal = locked/verified/the observed effect, caution = a quality warning or the association-only claim, warn = a prohibition, ai = the bounded model's kicker. A hue used for emphasis, grouping, or decoration is a defect.

**The Paper Label Rule.** Inside a dark band, labels are paper-toned (`tab-ink` at 0.8 opacity or `tab-muted`), never signal green. Green in a black bar is reserved for the memory item's check square.

**The Ink-Rule Rule.** Structure is drawn in ink, not tint. Panels and major blocks are separated by 1.5px `rule`; rows by 1px `hair`. No panel carries a colored side stripe, a tinted fill, or a colored top border.

## Typography

**Display Font:** Barlow Condensed 500/600/700 (with Arial Narrow, Impact, sans-serif)
**Body Font:** Barlow 400–700 (with ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif)
**Label/Mono Font:** ui-monospace, SFMono-Regular, Menlo, Consolas, monospace

**Character:** A condensed grotesk for everything that names or measures, a wide grotesk for everything that explains. Headings and numerals are tight and vertical; labels are small caps-style uppercase with wide tracking; text is set at 15px on 1.5. Fonts load from Google Fonts via `<link>` and fall back to system stacks. `font-synthesis: none` is set at the root.

### Hierarchy
- **Display numeral** (700, 80px / 60px ≤1040 / 46px ≤680, line-height 0.92, -0.02em, tabular): the Snapshot primary effect, in signal. The care brief's observed signal is the same voice at 60px (46px ≤680), line-height 0.95, -0.015em; readiness counts at 36px; support metrics, quality stats, and PhenoAge-style context values at 46px / 30px, 700, tabular. The whole ramp is fourteen steps — display 80 / 60 / 46 / 36 / 30 / 26 / 24, text 20 / 17 / 16 / 15 / 14, label 13 / 12 — and no other size is used.
- **Headline (h1)** (600, 46px / 36px ≤680, line-height 1, -0.01em): view titles, sentence case, max-width 880px. On the care brief the h1 drops to 30px because the document below is the content.
- **Title band (h2)** (600, 36px / 30px ≤680, line-height 1.02, -0.01em, max 24ch): the question inside the black title band.
- **Section title (h2/h3)** (600, 24–30px, line-height 1.05, -0.005em): panel heads (24px), numbered brief blocks and panels (26px), readiness and the AI band (30px). Sentence case throughout; `text-wrap: balance`.
- **Body** (400, 15px base; 16–17px for ledes and result copy, 14px for notes and table text, line-height 1.45–1.55): max line length 58–78ch depending on block (`max-width` 58ch, 62ch, 68ch, 72ch, 76ch, 78ch observed).
- **Label** (600, 12–13px, uppercase, 0.08–0.12em tracking): kickers (13px, 0.12em, with a 26x2px ink dash), document labels (12px, 0.12em), field labels and table heads (12–13px, 0.1em), legends, footer, schedule key (12px, 0.06–0.08em). Tabs are the same voice at 16px/0.07em (14px in the horizontal strip).
- **Mono** (500, 12–13px, line-height 1.3–1.5): trace chips and locked contract paths (12px, the paths with a 1px ink border), formulas (13px).

### Named Rules
**The Condensed-Caps Label Rule.** Anything that names a field, a section number, a control, or a status is Barlow Condensed, uppercase, 600, tracked 0.08–0.12em. Headings are not uppercased: they are Barlow Condensed in sentence case. (The direction contract said "caps for titles"; the build uppercases labels only and keeps every h1–h4 in sentence case. The build is canonical.)

**The Tabular Rule.** Any numeral that could be compared to another (effects, intervals, counts, coverage, dates in leaders, table cells) is set with `font-variant-numeric: tabular-nums`.

**The Interval Rule.** A large numeral never stands alone; the interval and sample sit beside or beneath it in body or label type. This is a product commitment rendered as a type pattern, not a style option.

## Layout

The shell is a two-column grid: a 236px sticky binder spine (full viewport height) and a fluid page. Page content is centered at `max-width: 1300px` with 32px top / 40px side / 60px bottom padding; the sticky top bar is 66px tall with 40px side padding and a 1.5px ink bottom rule over a 96% paper backdrop-blur.

Inside the page, panels are paper sheets with 1.5px ink borders and shared internal rhythm: 24–28px panel padding on Snapshot/Experiment/Data views, 36px horizontal padding on every band and block of the care sheet, 20px gutters between panels and layout columns. Section bars and toolbars are 60–66px tall. Rows are 12–18px tall blocks separated by 1px hairlines; large-numeral cells are 200px minimum height on Snapshot and 128px for journey steps. Two-column layouts use ratio grids (1.65fr/0.75fr overview; 1.15fr/2fr result band; 1.55fr/0.75fr title band; 1.15fr/0.85fr signal row; 1.45fr/1fr data) with a minimum of 300–360px on the narrow column. Checklists and question lists run in two equal columns separated by a hairline.

Breakpoints, in order: 1140px (title band and signal row stack), 1040px (all two- and three-column grids collapse, the AI ledger columns stack with hairline tops, the display numeral drops to 60px), 880px (the spine becomes a horizontal, scrollable numbered tab strip 60px tall; brand copy and the spine footnote hide; top bar goes static; side padding drops to 20px; the schedule becomes an auto-fill grid of 96px minimum cells), and 680px (top bar wraps, side padding 14px, sheet padding 20px, 2x2 metric grids, single-column readiness, table text 13px with wrapping cells).

Print shows the brief alone: spine, top bar, care title bar, AI band, footer, and the other views are hidden; the sheet loses its border and shadow; dark bands force `print-color-adjust: exact`; the title band, signal, blocks, questions, and footer avoid page breaks; trace chips are hidden.

## Elevation & Depth

Depth is drawn, not lit. Structure comes from ink rules and dark bands; shadows exist only as three soft, low-opacity lifts that make a paper sheet read as lying on the ground rather than as elevated UI. Nothing glows, nothing has a hover shadow, and nothing uses tonal layering beyond the paper/ground/ground-2 trio.

### Shadow Vocabulary
- **Sheet lift** (`--shadow-sheet`: `0 1px 0 rgba(16,19,21,0.12), 0 22px 44px -28px rgba(16,19,21,0.5)`): the care sheet only, the printed document at the center of the product.
- **Card lift** (`--shadow-card`: `0 1px 0 rgba(16,19,21,0.08), 0 14px 30px -24px rgba(16,19,21,0.35)`): every other paper panel (workspace, reading, schedule, controls, quality, context, method, result band, journey, quality strip, AI band).
- **Memory-item lift** (`0 10px 26px -18px rgba(16,19,21,0.55)`): the boxed "Values locked by code" item, so it sits a little proud of the sheet it is on.

### Named Rules
**The Resting-Lift Rule.** Shadows are static properties of paper surfaces, not responses to state. Hover and active states change fill and ink (paper inverts to ink, ink to signal), never elevation.

## Shapes

Square everywhere. `border-radius` is 0 on every panel, button, badge, pill, tab, chip, day cell, status square, check square, and marker; the only round form in the build is the chart's data points (SVG circles) and their 11px legend key (`border-radius: 50%`). The 7-day-mean line key is a flat 18x2.5px signal rule.

Borders carry the form language: 1.5px ink on panels, buttons, badges, the trace toggle, the segmented control, the decision-rule box, the warning box (in caution), and the claim pill (in caution); 2px ink on the memory item; 1px ink on locked-path chips; 1px hairline between rows and around the spine footnote (in spine-2). Dotted leaders are `2px dotted` in hair on paper and #3f4549 on ink, drawn as a flex-grown `::after` pulled up 3px to sit on the baseline. Status and state are shown with small filled squares (8–14px): signal, caution, muted, or currentColor. Section numbers in the spine are two-digit CSS counters (`decimal-leading-zero`); numbered blocks and questions carry a 24px condensed numeral in a fixed 40–44px gutter.

## Components

The controls feel like the printed handbook they sit in: square, ink-bordered, condensed caps, inverting on hover rather than lifting or tinting.

### Buttons
- **Shape:** square (0 radius), 1.5px ink border, 40px min height, 0 16px padding, Barlow Condensed 13px/600 uppercase 0.08em, 8px icon gap.
- **Default:** paper fill, ink text. **Hover:** inverts to ink fill, paper text (160ms ease-out on background and color).
- **Primary (`.button.primary`):** ink fill, paper text. **Hover:** signal fill and signal border.
- **On a dark band:** transparent fill, paper text and border; hover inverts to paper fill, ink text.
- **Focus:** 2px signal outline, 3px offset (global for buttons, links, summaries).
- **Disclosure button (`.method-details summary`):** styled as the primary button; hover to signal; native marker hidden.

### Chips
- **Claim pill:** paper fill, 1.5px caution border, caution text, 26px, condensed caps 12px/0.1em. Only ever says "association only" or a sibling claim label; caution is the meaning.
- **Demo badge:** paper, 1.5px ink border, 34px, condensed caps 12px, with an 8px signal square before the text. Reads "Synthetic care workflow" and stays visible in the top bar on every view.
- **Locked-path chip (`.ai-paths li`):** paper, 1px ink border, mono 12px, 5px 8px padding; the immutable contract paths in the AI ledger.
- **AI draft block (`.ai-draft`):** sits under the contract ledger inside the Bounded AI band, above a 1.5px ink rule; blue kicker "AI draft · cached at build time", title-sm heading, a 14px provenance paragraph (model, runner, date, Skill, "no live model calls"), and a boxed check card (2px ink border, memory-item lift) carrying a display-sm count in signal ("26" with "/ 26" in muted) over the label "numbers cited match the locked contract" and a 12px label-case verifier line (signal when passed, warn when failed). The draft's eight sections run in a two-column grid of hairline-ruled items with 13px muted uppercase headings, 16px prose and 15px square-bulleted lists. Empty state: one paragraph stating that no cached draft is included and how to generate one.
- **Verified number mark (`mark.cite`):** every number inside the draft, wrapped at render time. At rest: signal text, 600 weight, tabular, a 2px dotted signal underline, transparent background. `mark.cite.bad` (a number absent from the contract): warn text with a 2px solid warn underline. With `body.trace-on`: `.ok` marks fill with signal-soft and 4px side padding and the underline turns solid, so the model's citations read as the same chips the locked values show.
- **Trace values motion:** on toggle, chips stagger in at 45ms per element (`--i` set by script), a 2px signal scan line sweeps the viewport once over 820ms with a soft glow, and the chart's 7-day mean path draws itself in over 1100ms on view entry. All three are disabled by `prefers-reduced-motion`.
- **Trace chip (`[data-trace]::after`):** signal text on signal-soft, mono 12px/500, 3px 7px, `width: fit-content`, prefixed with an arrow ("→ "); hidden at rest, block when `body.trace-on`, hidden in print.

### Cards / Containers
- **Corner Style:** square.
- **Background:** paper on ground.
- **Shadow Strategy:** card lift on panels, sheet lift on the care sheet (see Elevation & Depth).
- **Border:** 1.5px ink; internal 1.5px ink between major blocks (section bars, readiness, signal row, block heads, table heads, list tops), 1px hair between rows and adjacent cells.
- **Internal Padding:** 24–28px on view panels; 28–36px on care-sheet bands and blocks; 16–22px on nested boxes.
- **Dark band variant:** ink fill, paper text, band greys for secondary text and leaders; used for the care title band, the sheet footer, the privacy band, the memory item's head bar, and the chart tooltip (ink, paper text, 13px, 10px 12px).

### Inputs / Fields
- **Segmented control (HRV / Sleep):** 1.5px ink frame, 36px buttons at 0 14px, condensed caps 13px, 1.5px ink dividers; active segment inverts to ink/paper. No radius, no shadow.
- **Trace toggle:** same body as the demo badge with a 10px hollow square mark; pressed state inverts to ink/paper and fills the mark with signal.
- **Checklist control (`.check`):** 22px ink square, paper check glyph, 700, in a 24px gutter beside 15px text rows divided by hairlines.
- The product has no text inputs; do not invent a field style.

### Navigation
- **Binder spine:** 236px, spine fill, sticky. Brand row (36px tab-ink monogram square, 20px condensed name, 12px tab-muted subtitle) over a 1px spine-2 rule. Tabs are 52px tall, condensed 16px/600/0.07em, tab-muted text, with a two-digit counter at left in 12px/0.1em at 0.8 opacity.
- **Hover:** tab-ink text on spine-2. **Active:** ink text on ground, flush with the page, counter in signal at full opacity.
- **Footnote:** 13px tab-muted text in a 1px spine-2 box pinned to the bottom, always stating that records are synthetic.
- **Mobile (≤880px):** the spine becomes a horizontal, scroll-hidden tab strip with the monogram at left; tabs 60px tall, 14px, nowrap.

### Dotted-Leader Row
A flex row (13–16px vertical padding, 1px hair bottom) with a label cell (condensed caps 12–12.5px, muted or ink) whose `::after` grows to fill the gap as a 2px dotted rule, and a right-aligned tabular value (Barlow 600, 14–15.5px). On ink bands the label is tab-muted and the leader #3f4549. Used for reading facts, title-band facts, source ledger rows, and data source rows; tracks in `.trace-on` wrap so the chip drops beneath.

### Memory Item (`.care-lock`)
The boxed thing that may not be changed. 2px ink border, paper body, its own lift. Head bar is a two-cell grid: a 52px signal square with a paper check glyph (22px/700), then an ink bar carrying the title in condensed caps 19px/600/0.08em. Body copy 15.5px on 1.5, 16px 20px 18px padding. The only place signal green sits inside a black bar.

### Warning Box
1.5px caution border on caution-soft, 14px text, 40px left padding making room for a 14px filled caution square carrying a condensed "!" in paper. Stacked warnings are 8px apart under a condensed-caps h4 with a 10px caution square before it.

### Decision Rule Box
1.5px ink border, 16px 18px 18px padding, condensed-caps 12.5px/0.1em label above 15px text; used for the predefined decision rule on the Experiment view.

### Schedule Day Cell
Seven-column grid of 100px-minimum cells divided by hairlines; day label in condensed 16px/600. Cutoff days fill with `day-on` (ink) and paper text; usual days stay `day-off` (paper). The key uses 12px squares with 1.5px ink borders; "timing unavailable" is tab-muted.

### Recovery Timeline Chart
SVG on paper: gridlines #e3e1da, axis and tick text muted 11.5px, points are circles with a 1.75 ink stroke, filled ink for cutoff nights, hollow (paper) for usual, tab-muted fill and stroke when timing is unavailable; the 7-day mean is a 2.25 signal line. Focused points take a 3px signal stroke; the tooltip is an ink box with paper text.

### Trace Values (signature interaction)
The x-ray reveal. The top-bar toggle sets `body.trace-on`; every `[data-trace]` element (primary effect, supporting metrics, coverage and balance facts, warnings, source rows, and the care brief's locked numbers) reveals a mono chip beneath it reading "→ <contract path>" via `::after`, entering with `trace-in` (220ms, opacity + 3px rise). View switches use `view-in` (260ms, opacity + 6px rise). Both use `--ease-out: cubic-bezier(0.16, 1, 0.3, 1)`; all hover transitions are 160ms on the same curve; `prefers-reduced-motion` collapses every animation and transition to 0.01ms.

## Do's and Don'ts

### Do:
- **Do** draw structure with 1.5px `rule` between blocks and 1px `hair` between rows; keep every corner at 0 radius except SVG data points.
- **Do** set every name, field label, tab, control, and status in Barlow Condensed uppercase 600 tracked 0.08–0.12em, and every heading in Barlow Condensed sentence case.
- **Do** set every comparable numeral in `tabular-nums`, and show its interval and sample beside it.
- **Do** join an item to its value with a 2px dotted leader; on ink bands use the band leader grey (#3f4549), never signal.
- **Do** use signal only for locked/verified state, caution only for quality warnings and the claim pill, warn only for prohibitions, ai only for the Bounded AI kicker.
- **Do** invert on hover (paper to ink, ink to signal for primary) at 160ms ease-out; keep shadows static.
- **Do** attach a `data-trace` contract path to every rendered locked number so the Trace values toggle can reveal it.
- **Do** keep the synthetic-data labels (demo badge, spine footnote, persona subtitle) visible on every view.

### Don't:
- **Don't** tint a card or panel; the only tinted fills in the build are `caution-soft` inside a warning box and `signal-soft` inside a trace chip.
- **Don't** add a colored side stripe, top border, or accent bar to a panel; ink rules are the only structure.
- **Don't** use green, amber, red, or blue for emphasis, grouping, icons, or headings outside their single meaning; do not add a fifth hue.
- **Don't** set labels inside a dark band in signal; they are `tab-ink` or `tab-muted`.
- **Don't** uppercase headings or use a script, serif, or rounded typeface anywhere.
- **Don't** introduce radius, gradients, glows, or hover elevation.
- **Don't** show a numeral without its interval and sample, or render copy that is not in the contract or the templates.
- **Don't** introduce text inputs, tinted status pills, or avatar imagery; the build has none.
