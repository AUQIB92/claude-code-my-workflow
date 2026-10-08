---
name: knowledge-base-JKSSB
description: Course-scoped knowledge base for Computer Awareness (JKSSB) — exam blueprint, source-trust tiers, terminology/notation registry, real-PYQ evidence, misconception traps, and content-generation rules. Loaded automatically when editing this course's slides, notes, or practice sets.
course_code: "JKSSB"
course_name: "Computer Awareness (JKSSB)"
term: "JKSSB recruitment cycle 2025-2026"
level: "competitive-exam prep (post-secondary; no formal programme)"
status: active
schema_version: 2
kb_version: 0.11.0
last_updated: 2026-10-08
lectures_recorded: 58
paths:
  - "syllabi/JKSSB.md"
  - "Slides/JKSSB/**/*.tex"
  - "Slides/JKSSB/**/*.md"
  - "Quarto/JKSSB/**/*.qmd"
  - "Notes/JKSSB/**"
  - "CompetitiveExam/JKSSB/**"
  - "InstructorHandouts/JKSSB/**"
  - "master_supporting_docs/JKSSB/**"
---

# Course Knowledge Base: Computer Awareness (JKSSB)

<!-- Bootstrapped 2026-10-06 by /syllabus + deep source research, before any deck
     existed. Unlike the CS301/CS401 KBs (which track notation across a 12-week
     semester), this is an EXAM-PREP KB: its centre of gravity is the exam
     blueprint, the source-trust hierarchy, and the near-neighbour trap registry
     mined from real JKSSB papers. Everything here governs how student-facing
     content is generated so it is (a) scoped to the official syllabus, (b)
     traceable to an authoritative source, and (c) tuned to the item formats
     JKSSB actually uses. -->

---

## 0. Operating Contract (read this first, every session)

**Precedence.** This file > general teaching-skill defaults > model priors. If a
content request conflicts with a rule here, follow the rule and say so in one line.

**Before writing any student-facing content:**
1. Read §2 (exam blueprint) + §4 (terminology) — every claim must fit the target
   post's scope and use the exam-recognised wording.
2. Read §3 (source-trust tiers) — cite only per the tier rules; never invent a
   paper number, key date, or page.
3. Read §6 (trap registry) + §8 (anti-patterns) — the distractors must come from
   real JKSSB behaviour, not generic textbook guesses.
4. Never reproduce a JKSSB item verbatim as "practice" without labelling it as a
   real PYQ with its source; never present a generated item as a real PYQ.
5. Include a video reference only when the user supplies its URL. If no URL is
   available, omit the reference from the slides, Notes, and syllabus; never add
   a pending/missing-link placeholder. Add the reference later when supplied.

**After a lesson/practice set is finalized (same session):**
- Append the observed traps to §6; add any new exact-term decision to §4.
- Add source rows to §3 when a new paper/key is ingested.
- Update frontmatter `last_updated`, `lectures_recorded`, `kb_version`.

**Write rules.**
- One fact per row. Every row gets a stable ID (`SRC-03`, `TRM-07`, `TRAP-02`…).
  IDs are never reused; retire with `[superseded by TRAP-11]`.
- Never invent a page, a paper serial, an answer-key date, or a cut-off. Unknown → `TBD`.
- Record only what a source actually says. No aspirations, no "likely question".

**Curation caps** (keep loadable): sources ≤ 30 · terms ≤ 60 · traps ≤ 40 ·
anti-patterns ≤ 20 · design principles ≤ 12.

---

## 1. Course Profile

| Field | Value |
|---|---|
| Audience level | Competitive-exam candidates (post-secondary; no formal programme) |
| Target exams | JKSSB Junior Assistant · Website Operator · Computer Instructor/Operator · allied JKSSB clerical/technical posts |
| Default difficulty | **`intro`→`core`** — recall/classification dominant (L1/L2), one-step application (L3) in the technical blocks. Never L4/L5 unless the target notification demands it |
| Exam target | JKSSB OMR written test (Computer Awareness section) + skill/typing test where applicable |
| Instruction language | Natural Indian **Hinglish** narration; simple Hindi for explanation, **exact English exam terminology preserved verbatim** (abbreviations, full forms, software names, protocols, commands, shortcuts) |
| Content formats | Explanation-only video (no MCQs in-video) → 3 derived artifacts: Revision Slides, Detailed Notes, MCQs+PYQs |
| Source of truth | `syllabi/JKSSB.md` (66-lesson arc) over the source docx; official JKSSB notices/papers over everything |

---

## 2. Exam Blueprint (the scope every artifact must fit)

<!-- Verified against official sources 2026-10-06. Re-verify against the target-post
     notification each cycle — marks/negative-marking/sections change by post. -->

| Post | Paper | Items | Marks | Time | Sections | Penalty |
|---|---|---|---|---|---|---|
| Junior Assistant | JA 2026 (held 19-Apr-2026; Notification 08/2025 dt. 27.09.2025) | 80 | 80 | 80 min | 4 × 20: Gen English · Gen Awareness (J&K UT) · Numerical & Reasoning · **Basic Concepts of Computer** | −¼ (0.25) per wrong |
| Website Operator | WO 2026 (provisional key 08-02-2026) | 80 | 80 | 80 min | multi-section; computer block ≈ Q61–80 | −¼ per wrong |
| Computer Instructor/Operator | CI 2025 (final key 16-02-2025) | 120 | 120 | 120 min | multi-section | −¼ of the item's marks per wrong; blank = no penalty |

**Official Junior Assistant computer scope (Unit IV, 20 marks) — verbatim:**
(i) Fundamentals of computer sciences · (ii) Hardware & Software · (iii) Input and
output devices · (iv) Operating system · (v) M.S Word, M.S Excel, M.S Access and
PowerPoint Presentation · (vi) E-mail & Internet.

**Official "Computer Applications" scope (10-mark annexure, another post) — broader:**
basic applications & components · fundamentals · hardware & software **+ concept of
open-source technologies** · input/output devices · MS Word/Excel/Access/PowerPoint,
PDF, Internet and E-mail · **computer virus & latest anti-virus** · **terms and
abbreviations used in IT** · **role of IT in governance**.

**Depth ratio to hold across every set:** ~50% L1 (direct recall), ~35% L2
(contrast/classification/matching), ~15% L3 (one-step application / short scenario).

**Mandatory item formats per MCQ set:** ≥1 NOT/EXCEPT/incorrect-statement item,
≥1 near-neighbour distractor set, ≥1 exact abbreviation/shortcut/command/full-form
item, ≥1 statement-evaluation (I/II/III…) item, and a "why the other options are
wrong" rationale for every item.

---

## 3. Source Registry & Trust Tiers

<!-- A claim's authority = its tier. Higher tier always wins. Never cite a lower
     tier for a fact a higher tier can settle. -->

**Tier 1 — Authoritative (JKSSB itself).** Official notices, syllabus PDFs, question
booklets, provisional & final answer keys. A Tier-1 answer key **supersedes every
other source** on a disputed item.

| ID | Source | What it settles | Location / URL |
|----|--------|-----------------|----------------|
| SRC-01 | JKSSB notification & syllabus, Junior Assistant / Jr. Steno — **Notification No. 08 of 2025 dt. 27.09.2025**, Notice dated 23.12.2025 | The official JA computer scope (Unit IV) + "Computer Applications" annexure | `https://jkssb.nic.in/Pdf/Syllabus_JrAsstt_Steno_23122025.pdf` |
| SRC-02 | JKSSB PYQ index | Which papers exist per year/post | `https://jkssb.nic.in/QP.html` |
| SRC-03 | **Junior Assistant 2026 paper** (eOffice booklet, 24 pp; computer block Q61–80) | Real JA item formats, concepts, traps | `https://jkssb.nic.in/Pdf/JuniorAssistant.pdf` → `master_supporting_docs/JKSSB/official_papers/JuniorAssistant_2026.pdf` |
| SRC-04 | **Website Operator 2026 paper** (16 pp; computer block ≈ Q61–80) | WO item formats, foundational concepts | `https://jkssb.nic.in/Pdf/WebsiteOperator.pdf` → `master_supporting_docs/JKSSB/official_papers/WebsiteOperator_2026.pdf` |
| SRC-05 | **Computer Instructor-Operator 2025 paper** (24 pp, 120 items; booklet instructions pp. 1–2) | Technical-post depth; penalty rule confirmed | `https://jkssb.nic.in/Pdf/COMPUTER%20INSTRUCTOR%20-OPERATOR.pdf` → `master_supporting_docs/JKSSB/official_papers/ComputerInstructorOperator_2025.pdf` |
| SRC-06 | Junior Assistant 2026 **final answer key** | Settles disputed JA items | `https://jkssb.nic.in/Pdf/FinalAnswerKeyJunior_Assistant_24062026.pdf` |
| SRC-07 | Website Operator 2026 provisional key | Provisional only — mark status | `https://jkssb.nic.in/Pdf/PROVISIONAL_ANSWERKEY_WEBSITEOPERATOR_08022026.pdf` |
| SRC-08 | Computer Instructor/Operator 2025 final key | Settles disputed CI items | `https://jkssb.nic.in/Pdf/Final_Answer_Key_16022025_24042025.pdf` |
| SRC-14 | Local official-paper store + source index | Offline copies of all Tier-1 papers + the download/read procedure | `master_supporting_docs/JKSSB/index.md` (papers in `official_papers/`) |

**Derived / internal artifacts (not external authority).**

| ID | Artifact | Use | Note |
|----|----------|-----|------|
| SRC-15 | **`JKSSB_Computer_Awareness_MCQ_Book.tex`** — internal original MCQ bank (11 chapters, 220 Q; labels `Sanfoundry` / `JKSSB official` / `original synthesis`) | Ready practice inventory to split into per-lesson `CompetitiveExam/JKSSB/` sets | `master_supporting_docs/JKSSB_Computer_Awareness_MCQ_Book.tex` — title page says "200" but **220** questions present (**fix**) |

**Tier 2 — Canonical MCQ banks.** Broad practice inventory; **never authoritative on
a JKSSB-specific fact**, and answers can be contested. Use to *compose* practice and
mine distractors, then re-scope to the JKSSB syllabus and re-verify.

| ID | Source | Use | Rules |
|----|--------|-----|-------|
| SRC-09 | **Sanfoundry** (`sanfoundry.com`) — Computer Fundamentals, Operating System, Data Structures, Networking, DBMS, Cyber Security MCQ banks | Practice-item composition + distractor mining | (a) Filter to the JKSSB syllabus scope; do **not** import engineering-depth (L4/L5) material. (b) Re-word into JKSSB item formats (§2). (c) Re-verify every answer; Sanfoundry keys are not authoritative — label `[Adapted: Sanfoundry]`. (d) Never present an unverified Sanfoundry item as a JKSSB PYQ. |
| SRC-10 | Standard CS/IT MCQ compilations (Testbook, GeeksforGeeks quizzes, etc.) | Same as SRC-09 | Same rules as SRC-09; lowest trust within Tier 2. |

**Tier 3 — Reference/exposition only.** General/standard treatment. Cite concepts,
never invent a page or a paper number.

| ID | Source | Use |
|----|--------|-----|
| SRC-11 | Government scheme/portal pages (Digital India, e-NAM, NeGP/e-Kranti/NeGD) | Governance-unit facts; prefer the .gov/.nic.in page over aggregators |
| SRC-12 | Vendor documentation (Microsoft Office support, RFCs for networking) | Exact shortcut/command/behaviour; tie to the *prescribed Office version* |
| SRC-13 | PSU textbook treatments (e.g., a standard Computer Fundamentals text) | Concept exposition; `unindexed` until `/index-textbook` runs |

**Source-verification state machine** (mirrors `.claude/rules/textbook-grounding.md`):
`unindexed` → `/index-textbook` never ran (no page cites permitted) ·
`indexed YYYY-MM-DD` → page cites permitted · `verified YYYY-MM-DD` → `/verify-claims`
checked the citations · `stale` → source replaced/re-issued after last verify.

---

## 4. Terminology & Notation Registry

<!-- The exam is written in exact English; the narration is Hinglish. Preserve the
     English term; explain in Hindi. These rows are the terminology contract. -->

| ID | Decision | Use (exact) | Avoid | Reason |
|----|----------|-------------|-------|--------|
| TRM-01 | Never translate exam terms | `full form`, `abbreviation`, `RAM`, `ROM` in English, always | Hindi transliteration of an abbreviation | Questions test the exact abbreviation/full form |
| TRM-02 | Spell vendor names exactly | `MS Word` / `Microsoft Word`; `Powerpoint Presentation` if quoting the syllabus | `M.S. Word`, `MSWORD`, `PPT` in prose | Matches syllabus & options |
| TRM-03 | Always give the full form on first mention | "POP3 — Post Office Protocol version 3" | `POP3` alone | Direct-recall items ask the expansion |
| TRM-04 | Preserve the paper's own option wording when quoting a PYQ | quote verbatim, then analyse | silently "fixing" a defective option | Defective options are teaching material (see §8) |
| TRM-05 | Number bases | subscript in prose ($10_{10}$, $1010_2$); no `0x` in running text | `0x0A`, `1010b` | Exam writes plain binary/hex |
| TRM-06 | Units | Use the paper's convention: `1024` ladder for KB/MB/GB/TB unless the option says otherwise | silently switching 1000 vs 1024 | A recurring trap; state which convention an option assumes |
| TRM-07 | Generations are ordinals | "third generation" for ICs, "fourth" for microprocessors | "Gen-3", "3rd gen (microprocessor)" | Textbook/JKSSB standard |
| TRM-08 | `Section Break` vs `Page Break` | Always both words, with the header/footer use-case attached | "page divide", "section page" | A repeated MS-Word trap (§6) |
| TRM-09 | File-format vs extension | Say "extension" and "format" separately; never conflate | "PNG file format is an extension" | Extension-vs-format is an explicit trap |
| TRM-10 | Networking addresses | `IPv4` = 32-bit, `IPv6` = 128-bit (never 256-bit) | "IPv6 is 256-bit" | A real distractor in JA 2026 Q78 |
| TRM-11 | Security verbs | `encryption` (confidentiality) vs `digital signature` (authenticity/integrity) — distinct | treating signature = encryption | A real trap in JA 2026 Q76 |
| TRM-12 | Hinglish policy | Simple Hindi explanation; keep every technical noun/verb in English | full-Hindi technical narration | Matches the course's stated delivery |

---

## 5. Real-PYQ Evidence Registry

<!-- Verbatim observations from official booklets (2026-10-06 pass). These anchor the
     trap registry (§6). Provenance label each item can carry in a practice set. -->

| ID | Paper / item | Concept tested | Source |
|----|--------------|----------------|--------|
| PYQ-01 | JA 2026 Q61 | ALU works via binary data + logic-gate operations | SRC-03 |
| PYQ-02 | JA 2026 Q62 | von Neumann; immediate addressing; cache hit ratio; data hazards even with register addressing; virtual memory vs cache | SRC-03 |
| PYQ-03 | JA 2026 Q63 | RAM volatility; ROM read/write claim; cache faster than main memory; CPU does not access secondary storage directly | SRC-03 |
| PYQ-04 | JA 2026 Q64 | Program Counter holds address of *current* instruction (claim); interrupts; Instruction Register; equal clock cycles claim | SRC-03 |
| PYQ-05 | JA 2026 Q65 | two's-complement overflow detection; zero extension; BCD = 4 bits/digit; byte-addressability & EA vs instruction length | SRC-03 |
| PYQ-06 | JA 2026 Q66 | hardware vs system software classification (device driver = software; OS = system software) | SRC-03 |
| PYQ-07 | JA 2026 Q67 | quad-core/2.4 GHz/16 GB/1 TB SSD scenario — diagnose inefficiency (multithreading/memory), not "slow CPU" | SRC-03 |
| PYQ-08 | JA 2026 Q68 | input vs output classification: light pen (I), punch-card reader (I), plotter (O), sound card (O), digitizer tablet (I), drum printer (O), scanner (I) | SRC-03 |
| PYQ-09 | JA 2026 Q69 | device↔description matching: haptic gloves, tactile display, voice response unit (VRU), data glove | SRC-03 |
| PYQ-10 | JA 2026 Q70 | deadlock recovery by resource preemption | SRC-03 |
| PYQ-11 | JA 2026 Q71 | priority inversion; priority inheritance; round-robin does not avoid inversion; starvation persists | SRC-03 |
| PYQ-12 | JA 2026 Q72 | MS Word NOT-correct: content control; first-line vs hanging indent in a style; Navigation Pane; Track Changes metadata | SRC-03 |
| PYQ-13 | JA 2026 Q73 | Section Break (not Page Break) enables different headers/footers | SRC-03 |
| PYQ-14 | JA 2026 Q74 | nested `IF` behaviour on blank / non-numeric input | SRC-03 |
| PYQ-15 | JA 2026 Q75 | `COUNTIFS` vs `SUMPRODUCT` for multi-criterion counting | SRC-03 |
| PYQ-16 | JA 2026 Q76 | email filters/rules; digital signature ≠ encryption; POP3 downloads to local; BCC | SRC-03 |
| PYQ-17 | JA 2026 Q77 | SmartArt conversion — which content type CANNOT convert without re-entry | SRC-03 |
| PYQ-18 | JA 2026 Q78 | TCP ordering/no-timing guarantee; UDP; IPv6 128-bit + 40-byte header; ICMP role | SRC-03 |
| PYQ-19 | JA 2026 Q79 | BGP (inter-domain, not intra-LAN); ICMP; IPv6 vs NAT; HTTP/3 uses QUIC (not TCP) | SRC-03 |
| PYQ-20 | JA 2026 Q80 | IaaS responsibility model — provider manages networking hardware | SRC-03 |
| PYQ-21 | WO 2026 Q61 | OS = layer providing a user-friendly interface | SRC-04 |
| PYQ-22 | WO 2026 Q62 | OS resident in primary storage while running | SRC-04 |
| PYQ-23 | WO 2026 Q63 | multitasking = run >1 program at a time | SRC-04 |
| PYQ-24 | WO 2026 Q64 | open-source mobile OS = Android | SRC-04 |
| PYQ-25 | WO 2026 Q65 | control unit controls operation sequence & data flow | SRC-04 |
| PYQ-26 | WO 2026 Q66 | open-source licence = view/change/share source | SRC-04 |
| PYQ-27 | WO 2026 Q67 | highest transfer rate = SSD | SRC-04 |
| PYQ-28 | WO 2026 Q68 | firmware that initialises hardware & loads OS = BIOS | SRC-04 |
| PYQ-29 | WO 2026 Q69 | large engineering drawings = plotter | SRC-04 |
| PYQ-30 | WO 2026 Q70 | magnetic ink = MICR | SRC-04 |
| PYQ-31 | WO 2026 Q71 | generation that introduced ICs = third | SRC-04 |
| PYQ-32 | WO 2026 Q72 | smallest unit of data = bit | SRC-04 |
| PYQ-33 | WO 2026 Q73 | decimal 10 = binary 1010 | SRC-04 |
| PYQ-34 | WO 2026 Q74 | ISP full form = Internet Service Provider | SRC-04 |
| PYQ-35 | WO 2026 Q75 | `@` separates user name and domain name | SRC-04 |
| PYQ-36 | WO 2026 Q76 | secure email transmission protocol = SSL/TLS | SRC-04 |
| PYQ-37 | WO 2026 Q77 | Word feature combining letters + address DB = Mail Merge | SRC-04 |
| PYQ-38 | WO 2026 Q78 | Excel formula must start with `=` | SRC-04 |
| PYQ-39 | WO 2026 Q79 | query retrieving data on a condition = Select Query | SRC-04 |
| PYQ-40 | WO 2026 Q80 | slide-show from beginning = F5 | SRC-04 |
| PYQ-41 | CI 2025 Q1 | ASCII decimal for `$` = 36 | SRC-05 |
| PYQ-42 | CI 2025 Q2 | binary `11010101.01` = 213.25 | SRC-05 |
| PYQ-43 | CI 2025 Q3 | UTF-8 is variable-length, ASCII-compatible | SRC-05 |
| PYQ-44 | CI 2025 Q4 | decimal 278 → binary `100010110` | SRC-05 |
| PYQ-45 | CI 2025 Q5 | mainframe vs supercomputer statement evaluation | SRC-05 |
| PYQ-46 | CI 2025 Q6 | Word "remove document window split" shortcut | SRC-05 |
| PYQ-47 | CI 2025 Q7 | Mail Merge (Word) | SRC-05 |

**Provenance labels a practice item may carry:** `[PYQ <post> <year> Q<n>, key:final|provisional]`
· `[PYQ-adapted]` · `[Adapted: Sanfoundry]` · `[Original]`. **Never** `[PYQ]` on an
unverified or generated item.

---

## 6. Trap & Misconception Registry

<!-- The highest-value table for this course. Every row is a distractor JKSSB actually
     uses or a belief candidates actually hold. Distractors for new practice items
     MUST be drawn from here. -->

| ID | The trap / misconception | The correct distinction | Evidence |
|----|--------------------------|-------------------------|----------|
| TRAP-01 | "RAM is non-volatile / retains data without power" | RAM is **volatile**; ROM is non-volatile | PYQ-03 |
| TRAP-02 | "ROM allows normal read **and write**" | ROM is read-only in normal operation (write needs special process) | PYQ-03 |
| TRAP-03 | "CPU directly accesses secondary storage" | CPU ↔ main memory; secondary storage goes through main memory/OS | PYQ-03 |
| TRAP-04 | "Program Counter stores the address of the **current** instruction being executed" | PC holds the address of the **next** instruction to fetch | PYQ-04 |
| TRAP-05 | "Interrupt is processed only after the **entire program** completes" | Interrupts are handled at instruction boundaries, mid-program | PYQ-04 |
| TRAP-06 | "All machine instructions take the same number of clock cycles" | Cycle count varies by instruction | PYQ-04 |
| TRAP-07 | "two's-complement overflow = carry out of the MSB" | Overflow test = wrong sign after adding same-signed operands; carry ≠ overflow | PYQ-05 |
| TRAP-08 | "zero extension is used for **signed** (negative) widening" | Zero-extension for unsigned; sign-extension for signed | PYQ-05 |
| TRAP-09 | "BCD packs a decimal number as plain binary" | BCD encodes **each decimal digit in 4 bits** | PYQ-05 |
| TRAP-10 | "device driver is hardware" | Device driver is **software**; OS is **system software** | PYQ-06 |
| TRAP-11 | "slow quad-core program must be a slow CPU" | Diagnose the stated bottleneck (multithreading/memory/disk I/O), not raw clock | PYQ-07 |
| TRAP-12 | "plotter/printer are input" / "sound card is input" | Plotter & drum printer & sound card are **output**; light pen, punch-card reader, digitizer, scanner are **input** | PYQ-08 |
| TRAP-13 | "Page Break changes headers/footers" | **Section Break** enables different headers/footers; Page Break does not | PYQ-13 |
| TRAP-14 | "`COUNTIFS` counts across two ranges" vs "`SUMPRODUCT` needs `--`" | `COUNTIFS(range1,crit1,range2,crit2)` for AND-count; `SUMPRODUCT((r1>=x)*(r2>=y))` also works | PYQ-15 |
| TRAP-15 | "digital signature **encrypts** the body so only recipient reads it" | Digital signature = authenticity/integrity; **encryption** provides confidentiality | PYQ-16 |
| TRAP-16 | "BCC hides sender and recipients from **each other**" | BCC hides recipients from **each other**; sender always knows; To/Cc visible to all | PYQ-16 (option wording) |
| TRAP-17 | "POP3 keeps mail synced on the server" | POP3 **downloads** to the local machine (typically removes from server); IMAP syncs | PYQ-16 |
| TRAP-18 | IPv6 = **256-bit** | IPv6 = **128-bit** (header fixed at 40 bytes) | PYQ-18 |
| TRAP-19 | "ICMP transfers application data" | ICMP is a control/diagnostic protocol (no ports, no data transfer) | PYQ-18, PYQ-19 |
| TRAP-20 | "BGP routes within a single local network" | BGP is **inter-domain** (between autonomous systems); OSPF/RIP are intra-domain | PYQ-19 |
| TRAP-21 | "HTTP/3 relies on TCP" | HTTP/3 uses **QUIC over UDP** | PYQ-19 |
| TRAP-22 | "IaaS provider manages the OS/data" | IaaS provider manages **infrastructure (networking/storage hardware)**; customer manages OS, runtime, apps, data | PYQ-20 |
| TRAP-23 | "open-source = freeware = shareware" | Open-source (view/change/share source) ≠ freeware (free cost) ≠ shareware (trial) | PYQ-24, PYQ-26 |
| TRAP-24 | "firmware that loads the OS = device driver / kernel" | **BIOS/UEFI** initialises hardware and boots the OS | PYQ-28 |
| TRAP-25 | "MICR/OCR/OMR interchangeable" | MICR = magnetic ink characters; OCR = printed text; OMR = marks | PYQ-30 |
| TRAP-26 | ICs introduced in 4th generation | ICs → **third** generation (microprocessors → fourth) | PYQ-31 |
| TRAP-27 | "smallest unit = byte/nibble" | Smallest unit = **bit**; 8 bits = 1 byte | PYQ-32 |
| TRAP-28 | "`@` separates domain and host" | `@` separates **user name** and **domain name** | PYQ-35 |
| TRAP-29 | "mail merge combines letters with a database = track changes/autocorrect" | **Mail Merge** | PYQ-37, PYQ-47 |
| TRAP-30 | "Excel formula can start with `+` or `%`" | A formula must start with `=` (Autosum/locale quirks aside) | PYQ-38 |
| TRAP-31 | Query types confused | **Select** query retrieves on a condition; Update/Append/Delete modify | PYQ-39 |
| TRAP-32 | Slide-show shortcut confused with F7 (spell check) / F9 | **F5** starts from beginning; Shift+F5 from current | PYQ-40 |
| TRAP-33 | 1000 vs 1024 ladder | State the convention; JKSSB options usually assume 1024 | general (docx audit) |
| TRAP-34 | "extension = format" | `.png` is an extension; PNG is the format | TRM-09 |

---

## 7. Running Examples, Applications & Datasets

| ID | Running device/scenario | Source | Lessons | Purpose |
|----|-------------------------|--------|---------|---------|
| EX-01 | The **office desktop** spine story (quad-core PC + MS Office + printer + internet + email), threaded across units | JA/WO 2026 items | Units 1–11 | One concrete machine carries every topic — a student can answer recall *and* the L3 scenario items (PYQ-07) about the same device |
| EX-02 | The **device-classification drill** (input/output/memory/storage table re-derived every unit) | PYQ-08, PYQ-67–70 | Units 2–4 | Repeatedly classifying real devices is the single highest-yield skill in the block |
| EX-03 | The **abbreviation/full-form ladder** (every abbreviation encountered, with expansion) | WO 2026 Q74; docx | all units | Direct-recall full-form items are the single most common JKSSB computer format |

---

## 8. Anti-Patterns (Don't Do This)

| ID | Anti-pattern | What happens | Correction |
|----|-------------|--------------|-----------|
| AP-01 | Present a generated/original MCQ as a real PYQ | Erodes trust; violates source integrity | Label `[Original]` / `[Adapted: Sanfoundry]`; reserve the PYQ label for verbatim official items |
| AP-02 | Reproduce a **defective** JKSSB option as fact (e.g. Q76-BCC wording, Q64-PC wording) | Teaches a wrong "fact" that a later key may not sustain | Quote verbatim, **flag the defect**, teach the stable concept; check the final key (SRC-06/08) |
| AP-03 | Import Sanfoundry's engineering depth (L4/L5) into a general post's set | Wastes time on material JKSSB doesn't ask general posts | Filter to §2 scope; reserve depth for technical-post tags |
| AP-04 | Generalise Website Operator/Computer Instructor depth to every post | Over-scopes the general candidate | Tag each item Core-General / Current-General / Technical-Post / Version-Sensitive |
| AP-05 | Show MCQs/questions **inside** the explanation video | Contradicts the course's explanation-only contract | Video teaches; MCQs live only in `CompetitiveExam/JKSSB/` |
| AP-06 | Narrate technical terms in Hindi | Removes the exact exam vocabulary the student must recognise | Hinglish narration, English terms (TRM-12) |
| AP-07 | Use a lower-tier source to "settle" something a Tier-1 source answers | Introduces drift from the official answer | Tier-1 key always wins (§3) |
| AP-08 | Cite a page from an `unindexed` book | Hallucination risk | Chapter-level only until `/index-textbook` runs (§3) |
| AP-09 | Quote an answer key date or cut-off from memory | Factual error | Only from SRC-06/07/08; else `TBD` |

---

## 9. Design Principles

| ID | Principle | Evidence / origin | Confidence |
|----|-----------|-------------------|-----------|
| DP-01 | Teach the **near-neighbour contrast** for every key term, not the term alone — "what it is / what it is not / nearest confusion" | Every JKSSB item is a distractor-trap (§6) | working |
| DP-02 | Build a device-classification reflex and an abbreviation ladder as reusable drills | PYQ-08, PYQ-32, PYQ-74 patterns | working |
| DP-03 | Hold the 50/35/15 L1/L2/L3 mix; keep L4/L5 technical-only | docx PYQ calibration + JA depth | working |
| DP-04 | Mine distractors from §6, not from imagination | Real-option flavour is what trains the candidate | tentative |
| DP-05 | One spine machine (EX-01) makes L3 scenario items concrete | PYQ-07 scenario format | tentative |

---

## 10. Toolchain & Code Pitfalls

| ID | Tool | Trap | Fix |
|----|------|------|-----|
| TC-01 | PDF text extraction | JKSSB papers are **scanned images**; PyMuPDF `get_text()` returns only the eOffice stamp, not the questions | Render pages to PNG (`page.get_pixmap(dpi=130)`) and read visually; OCR unavailable on this machine |
| TC-02 | `jkssb.nic.in` | Blocks some fetchers (transport error) | Download via `Invoke-WebRequest`/`curl`; the site is reachable from the shell even when the fetch tool fails |
| TC-03 | Provenance labels | Easy to lose in LaTeX/Quarto build | Store the label as a field/comment carried through compilation |

---

## 11. Open Items & Change Log

| Date | KB ver. | Change | Follow-up needed |
|------|---------|--------|------------------|
| 2026-10-06 | 0.1.0 | KB bootstrapped from official JA/WO/CI papers + official syllabus; real-PYQ + trap registries seeded; Sanfoundry registered as Tier-2 | Ingest CI 2025 computer block fully (only Q1–7 read); ingest WO Q1–60; `index` a PSU fundamentals text for page-cited exposition; register official papers in `CompetitiveExam/Books/index.md` |
| 2026-10-06 | 0.1.1 | Stored all four official papers + source index in `master_supporting_docs/JKSSB/`; registered the pre-existing internal MCQ book (`SRC-15`, 11 ch / 220 Q) | Fix the MCQ book's title-page count (says 200, has 220); split it into per-lesson `CompetitiveExam/JKSSB/` sets; consider a download script for the answer keys |
| 2026-10-11 | 0.2.1 | Added the no-placeholder rule for video references; removed unsupplied Lesson 49–50 references from lesson artifacts and syllabus | Add video links to materials only when supplied |
| 2026-10-07 | 0.3.0 | Built Unit 2 (lessons 04, 05, 06, 59): slides + notes + MCQ/answer sets; published to the course hub. Supplied videos for 04/05/06 (Concepts That Click channel); 59 intentionally has no video yet | Ingest the CI 2025 computer block (Q8+) and WO Q1–60; index a PSU fundamentals text for page cites |
| 2026-10-07 | 0.4.0 | Built Unit 3 (lessons 07, 08, 09, 10, 11): slides + notes + MCQ/answer sets; published to the course hub. No video links yet (to be supplied) | Add Unit 3 video links when supplied; same source-ingest follow-ups as 0.3.0 |
| 2026-10-08 | 0.5.0 | Built Unit 4 (lessons 12, 13, 14, 15, 16, 65): slides + notes + MCQ/answer sets; published to the course hub. No video links yet (to be supplied) | Add Unit 4 video links when supplied |
| 2026-10-08 | 0.6.0 | Built Unit 5 (lessons 17, 18, 19, 20, 21, 45, 46, 52, 60): slides + notes + MCQ/answer sets; published to the course hub. No video links yet (to be supplied) | Add Unit 5 video links when supplied |
| 2026-10-08 | 0.7.0 | Built Unit 6 (lesson 51): slides + notes + MCQ/answer set; published to the course hub. No video links yet (to be supplied) | Add Unit 6 video links when supplied |
| 2026-10-08 | 0.8.0 | Built Unit 11 (lessons 47, 57): slides + notes + MCQ/answer sets; published to the course hub. No video links yet (to be supplied) | Add Unit 11 video links when supplied |
| 2026-10-08 | 0.9.0 | Built Unit 7 (lessons 22-33, 54, 55, 61): slides + notes + MCQ/answer sets; published to the course hub. No video links yet (to be supplied) | Add Unit 7 video links when supplied |
| 2026-10-08 | 0.10.0 | Built Unit 8 (lessons 34-39, 53, 63): slides + notes + MCQ/answer sets; published to the course hub. No video links yet (to be supplied) | Add Unit 8 video links when supplied |
| 2026-10-08 | 0.11.0 | Built Unit 9 (lessons 40, 41, 62): slides + notes + MCQ/answer sets; published to the course hub. No video links yet (to be supplied) | Add Unit 9 video links when supplied |

<!-- Not yet captured: the full CI 2025 computer block (Q8 onward) and the non-computer
     sections of WO/JA; the exact WO section structure; the cut-off figures. Add as
     sources are read. -->
