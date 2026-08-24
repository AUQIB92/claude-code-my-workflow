---
name: render-lecture-video
description: Render a coherent sequence of an already-authored TikZ figure progression (a "Step 1, Step 2, Step 3..." trace already sitting in a Notes or trace-execution file) into a silent, captioned animated GIF. Use when user says "animate this trace", "make a GIF of the stack-growth figures", "render this step sequence as a video", "turn these diagrams into an animation", or invokes `/render-lecture-video <CODE>/<lecture> "<sequence name>"`. NOT a narration/video-generation tool — every on-screen caption is copied verbatim from the sequence's own already-authored `\caption{}` text, never LLM-generated, so there is no hallucination-fidelity question for this skill to solve. NOT for a mechanism with no existing step-diagram sequence to animate — author the figures first (by hand, or once `/trace-execution` has real output to point at).
argument-hint: "<CODE>/<lecture> \"<sequence name>\""
allowed-tools: ["Read", "Write", "Grep", "Glob", "Bash"]
effort: medium
disable-model-invocation: true
---

# Render Lecture Video

Turns an already-authored sequence of step-diagrams (the kind `/trace-execution` produces, or the kind already hand-authored in a Notes file before that skill existed) into a silent, captioned animated GIF — the proven toolchain from this session's proof of concept (`xelatex` → `pdftoppm` → `ffmpeg`), generalized to any sequence and any step count, plus real burned-in captions the PoC didn't have.

**MVP scope.** No audio narration, no LLM-generated captions, no CoVe fidelity-checking of anything — every caption is copied verbatim from a `\caption{}` that a human already wrote and that already shipped in a compiled PDF. Narration and fidelity-checking are this feature's Phase 3 (Differentiation), explicitly out of scope here.

## Phase 0 — Locate the sequence

Given `<CODE>/<lecture>` and a `"<sequence name>"`:

1. **Check for real `/trace-execution` output first:** `Figures/<CODE>/<lecture>/<sequence>-trace.tex` (the path that skill is documented to produce). If it exists, that file's numbered `tikzpicture` blocks are the sequence — use them.
2. **Otherwise, fall back to the proven retrofit path:** scan `Notes/<CODE>/<lecture>-notes.tex` for a run of `\begin{figure}...\end{figure}` blocks whose `\caption{}` text shares `<sequence name>` as a common prefix (e.g. `"Stack growth, Step"` matches `"Stack growth, Step 1: ..."`, `"Stack growth, Step 2: ..."`, ...). Order by the step number in each caption, not by file position (they're expected to already be in order, but don't assume it silently).
3. If neither path finds a sequence, halt with a clear message naming both paths checked — do not guess at a different sequence the user didn't ask for.

## Phase 1 — Extract, compile, rasterize

Do all per-frame work in a scratch working directory, not in `Figures/<CODE>/<lecture>/` — `/extract-tikz` sets this precedent already (its `Figures/` output is the final SVGs only, never its compile intermediates). Only the finished GIF (Phase 3) lands in `Figures/`.

For each step in the located sequence, in order:

1. Extract its `tikzpicture` block verbatim (read-only against the source file — Notes/ or Figures/ content is never edited by this skill).
2. Write it into a standalone `.tex` file in the scratch directory: `\documentclass[border=6pt]{standalone}`, `\input{<relative-path-to>/Preambles/header}`, the block, `\end{document}` — same shape validated in the PoC (`quality_reports/poc_builds_2026-08-20/animation-compiler/step*.tex`).
3. Compile with `xelatex -interaction=nonstopmode` (one pass is sufficient for a standalone TikZ figure with no cross-references — confirmed in the PoC). Halt and report if any step fails to compile; do not silently skip a broken frame and animate around the gap.
4. Rasterize each compiled PDF to PNG via `pdftoppm -png -r 150` (confirmed available locally — MiKTeX's own copy and a WinGet poppler install both provide it).

## Phase 2 — Burn in captions

For each frame, draw its sequence's own `\caption{}` text (LaTeX-stripped to plain text — drop `\texttt{}`/`\emph{}` wrappers, keep the words) onto the bottom of the PNG using Python's PIL (`ImageFont.truetype("arial.ttf", ...)`, confirmed loadable in this environment). Wrap long captions across 2-3 lines rather than letting them run off the frame edge; leave a visible margin, same discipline `tikz-measurement.md` already asks of any text near a drawn boundary.

**Never invent or paraphrase a caption.** If a step has no `\caption{}` (shouldn't happen given Phase 0's own selection criteria, but check), use its figure label or a plain "Step N" fallback — do not write new descriptive text.

Save each captioned frame as `frame_%02d.png` (`frame_01.png`, `frame_02.png`, ...) in the scratch directory — Phase 3's `ffmpeg` command below globs this exact pattern.

## Phase 3 — Stitch

`ffmpeg -framerate 1/1.2 -i frame_%02d.png -vf "fps=10,scale=<source-width>:-1:flags=lanczos" <sequence>-animation.gif` — same command shape validated in the PoC (each source frame held ~1.2s, 10fps output for smooth GIF playback). Confirm all frames share identical pixel dimensions before stitching (the PoC's 3 frames did, because the source figures shared a fixed-size background rectangle; if a real sequence's frames differ in size, pad to the largest frame's dimensions rather than stretching any frame's aspect ratio).

**Output:** `Figures/<CODE>/<lecture>/<sequence>-animation.gif` — a real, permanent artifact alongside that lecture's other TikZ-derived figures, per `CLAUDE.md`'s existing `Figures/<CODE>/<lecture>/` convention. (The PoC's own output stayed in `quality_reports/poc_builds_2026-08-20/` as an explicitly experimental location; this MVP graduates it to the real figures directory.)

## Verify

Confirm the final `.gif` file exists and its frame count is a small integer multiple of the step count (10fps × ~1.2s/frame × N steps) — a mismatch means a frame silently failed to compile/rasterize and Phase 1 should have halted instead of continuing.

## What This Skill Does NOT Do

- Never generates narration, dialogue, or any caption text not already present in the source `\caption{}` — no LLM is asked to describe what's happening in a frame.
- Never edits `Notes/` or `Figures/*.tex` source content — extraction is read-only.
- Never adds audio (TTS or otherwise) — silent GIF only, this tier.
- Never invents a step sequence that doesn't already exist in the source material — if `/trace-execution` hasn't been run and no hand-authored sequence matches the requested name, this skill halts rather than fabricating figures.

## Cross-references

- [`.claude/skills/trace-execution/SKILL.md`](../trace-execution/SKILL.md) — the skill this one prefers as a source when it has real output; as of this session it has never been invoked (confirmed via `git log` and a repo-wide glob), so the Notes-file fallback in Phase 0 is the load-bearing path today, not a rare edge case.
- [`.claude/skills/extract-tikz/SKILL.md`](../extract-tikz/SKILL.md) — the standalone-compile pattern (`documentclass{standalone}` + shared header) this skill's Phase 1 reuses.
- [`.claude/rules/tikz-measurement.md`](../../rules/tikz-measurement.md) — the boundary-clearance discipline Phase 2's caption placement follows.
- [`.claude/rules/post-flight-verification.md`](../../rules/post-flight-verification.md) — the CoVe mechanism a future Phase 3 (narration-fidelity checking) would reuse; not used by this MVP, which has no generated text to verify.
- `quality_reports/repo_innovator_academic-workload_2026-08-20/REPORT.md` — the originating bet (Developer Magnet) and its full 4-phase build strategy.
