# JKSSB (Computer Awareness) — Source Index

Course-scoped source material for the JKSSB Computer Awareness course.
Governs the content rules in [`.claude/rules/knowledge-base-JKSSB.md`](../../.claude/rules/knowledge-base-JKSSB.md).
Syllabus: [`syllabi/JKSSB.md`](../../syllabi/JKSSB.md).

**Read this before citing anything as a "PYQ".** Tier-1 (official) always wins; only
verbatim official items may carry the `[PYQ …]` label.

---

## Tier 1 — Official JKSSB sources

Local copies in `official_papers/` (downloaded 2026-10-06 from `jkssb.nic.in`).

| File | What it is | Official URL |
|------|------------|--------------|
| `official_papers/Syllabus_JrAsstt_Steno_23122025.pdf` | **Official syllabus** — Junior Assistant / Junior Stenographer, Notification No. 08 of 2025 dt. 27.09.2025 (Notice dt. 23.12.2025). Contains the JA **Unit IV "Basic Concepts of Computers" (20 marks)** scope and the broader 10-mark **"Computer Applications"** annexure. | `https://jkssb.nic.in/Pdf/Syllabus_JrAsstt_Steno_23122025.pdf` |
| `official_papers/JuniorAssistant_2026.pdf` | **Junior Assistant 2026 question paper** (booklet, 24 pp). Computer block **Q61–Q80**. Scanned images — the eOffice stamp is the only text layer. | `https://jkssb.nic.in/Pdf/JuniorAssistant.pdf` |
| `official_papers/WebsiteOperator_2026.pdf` | **Website Operator 2026 question paper** (16 pp). Computer block **≈ Q61–Q80**. | `https://jkssb.nic.in/Pdf/WebsiteOperator.pdf` |
| `official_papers/ComputerInstructorOperator_2025.pdf` | **Computer Instructor-Operator 2025 paper** (24 pp, **120 items / 120 marks / 120 min**; booklet instructions confirm **−¼ per wrong, blank = no penalty**). | `https://jkssb.nic.in/Pdf/COMPUTER%20INSTRUCTOR%20-OPERATOR.pdf` |

**Answer keys (Tier 1, not yet stored locally):**

| Key | URL | Status |
|-----|-----|--------|
| JA 2026 final key | `https://jkssb.nic.in/Pdf/FinalAnswerKeyJunior_Assistant_24062026.pdf` | final |
| Website Operator 2026 provisional key | `https://jkssb.nic.in/Pdf/PROVISIONAL_ANSWERKEY_WEBSITEOPERATOR_08022026.pdf` | provisional |
| Computer Instructor/Operator 2025 final key | `https://jkssb.nic.in/Pdf/Final_Answer_Key_16022025_24042025.pdf` | final |
| JKSSB PYQ index | `https://jkssb.nic.in/QP.html` | — |

**Download note:** `jkssb.nic.in` blocks some fetchers but is reachable from the
shell — use `Invoke-WebRequest`/`curl`, not the browser-fetch tool.

---

## Tier 2 — MCQ banks & practice sources

| Source | Use | Rules |
|--------|-----|-------|
| **Sanfoundry** — Computer Fundamentals, Operating System, Computer Network and related chapterwise MCQ banks (`sanfoundry.com`) | Practice-item composition and distractor mining | Filter to the JKSSB syllabus scope; do **not** import engineering depth; re-word into JKSSB item formats; re-verify every answer; label `[Adapted: Sanfoundry]`. Sanfoundry keys are **not** authoritative. |
| Other MCQ compilations (Testbook, GfG quizzes) | Same | Lowest trust within Tier 2. |

---

## Internal derived artifact

| File | What it is | Status |
|------|------------|--------|
| `master_supporting_docs/JKSSB_Computer_Awareness_MCQ_Book.tex` | Original, chapterwise MCQ bank (LaTeX book). **11 chapters, 220 questions** with sources, answers and explanations; labels each item `Sanfoundry` / `JKSSB official` / `original synthesis`. | Draft — title page says "200 original MCQs" but 220 questions are present (**mismatch to fix**); not yet split into per-lesson `CompetitiveExam/JKSSB/` files |

---

## How to read the scanned papers in this environment

OCR is **not** available on this machine (no Tesseract/pytesseract/easyocr). The
question papers are image-only PDFs, so `PyMuPDF` `get_text()` returns just the
eOffice stamp. Render pages to images and read them visually:

```python
import fitz
doc = fitz.open("official_papers/JuniorAssistant_2026.pdf")
doc[17].get_pixmap(dpi=130).save("JA_p18.png")   # 0-indexed → page 18
```

---

## Registering new sources

When a new paper/key/edition is added:

1. Drop the file under `official_papers/` (or `supporting_papers/`).
2. Add a row above with post, item range, and URL.
3. Add a `SRC-nn` row to §3 of `.claude/rules/knowledge-base-JKSSB.md` and log it in §11.
4. If it changes an answer, mark the affected `TRAP-nn`/`PYQ-nn` rows before editing.

*Official JKSSB notices and question papers are Government of J&K publications.
Kept here for offline, source-grounded course generation.*
