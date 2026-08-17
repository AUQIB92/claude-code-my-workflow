---
name: publish-course-hub
description: Regenerate a course hub page's data-driven regions (weekly-lecture rail, progress ribbon, assignments table, competitive-exam table) from the syllabus + what's actually published in docs/, instead of hand-editing docs/courses/<code>/index.html every time a new week ships. Use when user says "update the course hub", "sync the course page", "regenerate the CS401 hub", "the course page is out of date", "publish this week to the hub", or after any /deploy that adds/changes a lecture's slides, notes, assignment, or GATE set. NOT for the page's editorial content (hero copy, prerequisites prose, assessment table, footer) — those stay hand-owned; this skill only touches the four marked regions.
argument-hint: "[CourseCode], e.g. CS401 (docs/courses/CourseCode/index.html and syllabi/CourseCode.md must both already exist)"
allowed-tools: ["Read", "Grep", "Glob", "Edit", "Write", "Bash"]
effort: medium
---

# `/publish-course-hub` — Regenerate the Data-Driven Regions of a Course Hub Page

Closes a real drift risk: `docs/courses/<code>/index.html` is ~400+ lines of hand-crafted HTML, and four of its regions (the weekly-lecture rail, the progress ribbon, the assignments table, the competitive-exam table) are pure derived data — they should never be hand-typed, because the moment a new week ships and someone forgets to update the "published" badge or the progress percentage, the hub page silently lies about what's actually available. This skill regenerates exactly those four regions from ground truth (`syllabi/<CODE>.md` + a scan of what's actually in `docs/`) and leaves everything else on the page — hero copy, prerequisites prose, the assessment table, the footer — untouched, because that content is genuinely editorial and should stay hand-owned.

## The marker convention

Each of the four regions is bounded by an HTML comment pair:

```html
<!-- publish-course-hub:ribbon:start -->
...regenerated content...
<!-- publish-course-hub:ribbon:end -->
```

Four marker pairs total: `ribbon`, `hero-chips`, `rail`, `assignments-table`, `practice-table` (five — the hero's "N / 12 lectures published" chip is its own tiny region inside the hero, separate from the ribbon). This skill only ever replaces the content **between** a `:start`/`:end` pair — never anything outside it. If a page doesn't have the markers yet (first run on a page that predates this skill), do Phase 1 (Adopt) once; every run after that is Phase 2 (Regenerate) only.

## Phase 0: Pre-Flight

1. Confirm `syllabi/<CODE>.md` exists (the weekly-schedule table is the ground truth for topics/readings) and `docs/courses/<CODE-lowercase>/index.html` exists (nothing to regenerate if the hub page doesn't exist yet — that's a bigger, editorial task, not this skill's job).
2. Read the syllabus's weekly-schedule table in full: `| Week | Topic | Readings | ... | Deliverable |` (or the course's equivalent columns — CS401 and CS301 both use this shape; adapt column names if a course's syllabus differs).

## Phase 1: Determine what's actually published (the scan)

For each week `NN` in the syllabus (matched to lecture file stems by the established `NN-topic-slug` numeric-prefix convention used everywhere in this repo — `Slides/<CODE>/NN-*.tex`, `Notes/<CODE>/NN-*-notes.tex`, etc.):

- **Slides published?** `docs/slides/<CODE>/NN-*.pdf` exists.
- **Notes published?** `docs/notes/<CODE>/NN-*-notes.pdf` exists.
- **Assignment published?** `docs/assignments/<CODE>/NN-*-assignment.pdf` exists (a written assignment). Also check for `NN-*-coding-assignment.pdf` (a coding assignment) — a week can have either, both, or neither.
- **Practice set published?** `docs/competitive-exam/<CODE>/NN-*-questions.pdf` (+ matching `-answers.pdf`) exists.

A week counts as **"Published"** (for the rail badge and the progress ribbon) if its slides exist — slides are the anchor artifact; notes/assignment/practice are additive links shown when present, omitted when not (never a dead link to a file that doesn't exist).

**Never invent a week's topic or readings.** If the syllabus has fewer/more weeks than lecture files on disk, or a week's Slides file's own title doesn't match the syllabus's stated topic, surface the mismatch to the user rather than silently picking one source over the other.

## Phase 2a: Adopt (first run only, page has no markers yet)

If `docs/courses/<CODE-lowercase>/index.html` doesn't yet contain `<!-- publish-course-hub:rail:start -->`, insert the five marker pairs around the **existing, current** content of each region, changing nothing about what's currently there — this run is pure instrumentation, not regeneration. Locate the insertion points structurally:

- **`hero-chips`**: the `<span class="chip-glass">N / 12 lectures published</span>` line inside `<div class="hero-chips">`.
- **`ribbon`**: the `<div class="ribbon"> ... </div>` block immediately after `<main id="main" ...>`.
- **`rail`**: the `<div class="rail"> ... </div>` block inside `<section id="lectures">`.
- **`assignments-table`**: the `<div class="table-card"> ... </div>` block inside `<section id="assignments">`.
- **`practice-table`**: the `<div class="table-card"> ... </div>` block inside `<section id="practice">`.

After adopting, proceed immediately to Phase 2b so the first run also verifies the markers were placed correctly (regenerating from the scan should reproduce content identical to what was just wrapped, if the page was already in sync — a good self-check).

## Phase 2b: Regenerate (every run)

For each of the five regions, generate fresh HTML from the Phase 1 scan and replace the content strictly between its marker pair:

**`hero-chips`** — recompute `"<published count> / <total weeks> lectures published"`.

**`ribbon`** — recompute the summary line (`"weeks 1–K published in full"` or the exact published-week list if there are gaps), the percentage (`published / total`, rounded), and the `data-fill="<percentage>"` attribute. Match the existing prose style exactly (see either current hub page for the sentence shape).

**`rail`** — one `<div class="rail-item">` per syllabus week, in week order:
- Published: `<span class="badge">Week NN</span><span class="badge badge-accent">Published</span>`, `rail-actions` with a link per artifact that actually exists (Slides always; Notes/Assignment/Coding/Practice only if present — never a dead link), `rail-body` with the syllabus's topic as `h3`, a one-sentence `rail-text` distilled from the syllabus's topic description, and `rail-readings` from the syllabus's Readings column.
- Not yet published: `<div class="rail-item dim">`, `<span class="badge badge-muted">Week NN</span><span class="badge badge-muted">In progress</span>`, no `rail-actions` block, same `rail-body`/`rail-readings` pattern (topic and readings are known from the syllabus even before the lecture ships).

**`assignments-table`** — one `<tr>` per week with a published written and/or coding assignment, linking each that exists.

Every row must end with a **Submit cell** linking to the hand-owned `#submit` section on the same page, and the `<thead>` must carry a matching final `<th>Submit</th>`:

```html
<td><a class="btn-sm ghost" href="#submit">Submit &uarr;</a></td>
```

This cell is generated, not hand-typed, precisely because the table is regenerated wholesale — a Submit button added by hand inside the markers would be silently wiped on the next run. The `#submit` section it points at lives *outside* every marker pair and is never touched by this skill. If a course hub has no `#submit` section yet, omit the cell and the header rather than emitting a dead anchor.

**`practice-table`** — one `<tr>` per week with a published GATE practice set, linking questions + answers.

## Phase 3: Write and verify

1. Apply the five region replacements via `Edit` (exact string match on the marker-delimited block — never a broader diff that could touch editorial content outside the markers).
2. **Tag balance check**: re-run the same `<div>`/`<section>`/`<table>`/`<tr>`/`<a>` open-vs-close count check `/publish-course-hub` output must pass (see `docs/courses/cs301/index.html`'s own build history for the exact Python one-liner pattern) — a marker-bounded splice that breaks HTML structure is worse than stale content.
3. **Link resolution check**: every `href` generated in this run must resolve to a real file under `docs/` (same check as the initial `docs/courses/cs301/index.html` build: resolve each relative link from the page's own directory, confirm the file exists).
4. Report: weeks published vs. total, which regions changed, and any syllabus/disk mismatches surfaced in Phase 1.

## Cross-references

- `.claude/skills/deploy/SKILL.md` — the skill that changes what's in `docs/`; run `/publish-course-hub <CODE>` after any `/deploy` that adds a new week's materials.
- `.claude/skills/syllabus/SKILL.md` — owns the weekly-schedule table this skill treats as ground truth for topics/readings.
- `docs/courses/cs401/index.html`, `docs/courses/cs301/index.html` — the two existing hub pages; the exact HTML shape (`rail-item`, `chip-glass`, `table-card`, badge classes) this skill's generated fragments must match.
- `.claude/rules/single-source-of-truth.md` — the general principle (Beamer/syllabus as source, everything else derived) this skill applies to the course hub page specifically.
