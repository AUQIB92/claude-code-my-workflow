# Computer Awareness (JKSSB) — Competitive Exam Preparation

Competitive-exam prep · self-paced (video + slide course) · 66 lessons across 12 units

Source: `syllabi/JKSSB_Computer_Awareness_Prompt2Render_Animation.docx` — a 66-lesson Prompt2Render command book ("JKSSB Computer Awareness") calibrated against the JKSSB Previous Year Question Papers index and the Junior Assistant 2026 / Website Operator 2026 / Computer Instructor-Operator 2025 papers.

---

## Course description

This course prepares candidates for the Computer Awareness component of JKSSB recruitment examinations (Junior Assistant, Website Operator, Computer Instructor/Operator and allied posts). It covers the full examiner-visible surface of computer fundamentals — hardware, memory, storage, I/O, software, operating systems, the MS Office suite, the internet, email, networking, cybersecurity and e-governance — at the recall/classification/one-step-application depth at which JKSSB actually tests it. Candidates leave able to answer direct-recall, definition, classification, comparison, matching, sequence, statement and NOT/EXCEPT items, recognise the nearest-confusing concept in each distractor set, and apply the exact exam-recognised abbreviation, shortcut or command.

---

## Prerequisites

None. Basic familiarity with using a computer or smartphone (files, folders, a browser, email, MS Word/Excel) is helpful context but is not assumed or tested.

---

## Target posts & exam context

| Post | Reference paper | Computer block |
|------|-----------------|----------------|
| Junior Assistant | 2026 paper (final key 24-06-2026) | ~20-question block: CPU architecture, addressing, BCD, instruction execution, processes, deadlock, Office statements, Excel logic, email, TCP/IP, routing, cloud IaaS |
| Website Operator | 2026 paper (provisional key 08-02-2026) | Foundational OS, open-source, BIOS, memory, binary, email, Word, Excel, Access, PowerPoint |
| Computer Instructor / Operator | 2025 paper (final key 16-02-2025) | Adds HTML/DHTML/XML/JavaScript/VBScript/ASP.NET, multimedia, CISC/RISC, compiler phases, Linux administration, CLI utilities, firewall types, DES, Internet governance, copyright, ARPANET |

**Depth ratio (observed JKSSB pattern):** ~50% Level 1 direct recall, ~35% Level 2 contrast/classification/matching, ~15% Level 3 short one-step application. Level 4/5 multi-step problem-solving is optional and only where the target notification explicitly demands it.

**Before calling any lesson "current," verify against the target-post notification:** exact syllabus, marks, negative marking, language, practical-test requirement, and the prescribed Office/software version. Technical-post depth (Units 2, 6, 9) is Core-General for technical posts but Extended/Technical-only for general posts — see Unit 12.

---

## Learning objectives

By the end of this course, candidates will be able to:

- Define and recall core computer-fundamentals terminology — data, information, hardware, software, firmware, driver, humanware (Units 1, 5)
- Classify computers, memory types, storage media, software, ports, devices and printers by type/category (Units 1–5)
- Distinguish nearest-neighbour, commonly confused terms using the exam-recognised wording — RAM vs ROM, compiler vs interpreter, POP vs IMAP, virus vs worm, physical vs logical port (all units)
- Identify a component's function/role and match technology → role and platform → purpose (Units 2–11)
- Recall and apply exact commands, keyboard shortcuts, function keys, abbreviations and file extensions across Windows, MS Office and networking (Units 5, 7, 8, 9)
- Sequence processes correctly — instruction cycle, boot, mail-server flow, data transmission, e-governance service flow (Units 2, 5, 8, 9, 11)
- Evaluate statement-based, NOT/EXCEPT, assertion–reason and matching items by locating the single defective option (all units)
- Perform one-step application at L3 depth — numeric-base conversion, one-step formula result, addressing-mode identification, RAM/Excel/DMA scenario (Units 1, 2, 7, 9)
- Retrieve the entire course at the 50/35/15 depth ratio in a timed mixed set (Unit 12)

---

## Deliverables — the standard three-artifact set per lesson

Every lesson produces three study artifacts plus one video lesson. The video is the *source*; slides, notes and MCQs are all *derived* from it (single-source-of-truth).

| Deliverable | What it is | Produced by | Path convention |
|-------------|------------|-------------|-----------------|
| **Revision Slides** | Compact, animated, exam-focused deck — every definition, full form, classification, contrast and trap on one scannable pass | `/create-lecture` (Beamer `.tex`) | `Slides/JKSSB/<NN>-<slug>.tex` |
| **Detailed Notes** | Full prose expansion of the slides — worked examples, expanded contrasts, the "what it is / what it is not / where used / nearest confusion" for every distinction | `/lecture-notes` | `Notes/JKSSB/<NN>-<slug>-notes.tex` |
| **MCQs + PYQs** | Practice set: verified real past-year questions (Chain-of-Verification, provenance-labelled) **plus** original exam-pattern questions filling topic gaps, with an answer key and "why the other options are wrong" rationales | `/competitive-exam-questions` | `CompetitiveExam/JKSSB/<NN>-<slug>-questions.tex` · `-answers.tex` |
| *Video lesson* | The 6–10-minute animation-heavy explanation lesson itself (Manim precision layer + realistic 3D only where it aids recognition; Hinglish narration, Kokoro `hm_omega`) | `prompt2render.py new … ` / `build` | `<NN>-<slug>` project slug |

**Deck tag:** every Beamer deck sets `\coursecode{JKSSB}` right after `\input{header}`.

**MCQ provenance rule (non-negotiable).** Original practice questions are never presented as real PYQs. Every set labels each item `[PYQ <post> <year>, key status]`, `[PYQ-adapted]`, or `[Original]`. Ambiguous or defective items are flagged and the stable concept taught, per the docx's source-and-maintenance note.

---

## Course schedule

Legend — `[ ]` = not yet built; `[x]` = shipped. Unit-mastery capstones (lessons 48, 58, 66) are revision/audit artifacts: Slides required, Notes optional, MCQs = the drill set itself.

### Unit 1 — Fundamentals & Data Representation

| # | Lesson | Revision Slides | Detailed Notes | MCQs + PYQs |
|---|--------|:---:|:---:|:---:|
| 01 | What Is a Computer — definition, data, information, IPO, characteristics, applications, limitations | `01-what-is-a-computer` [x] | [x] | [x] |
| 02 | Types of Computers — analog/digital/hybrid, micro/mini/mainframe/super, generation-linked classes | `02-types-of-computers` [x] | [x] | [x] |
| 03 | Bits, Bytes & Units — bit, nibble, byte, word, KB/MB/GB/TB, 1024 convention | `03-bits-bytes-units` [x] | [x] | [x] |
| 49 | Computer Generations & History — 1st–5th generation, C-DAC/PARAM 8000, association traps | `49-computer-generations-history` [x] | [x] | [x] |
| 50 | Data Representation, Number Systems & Logic — binary/decimal/octal/hex, bits/nibbles/bytes, ASCII/Unicode, RGB, basic logic gates | `50-data-representation-number-systems-logic` [x] | [x] | [x] |

Video references: [Lesson 01](https://youtu.be/EdRZK57oqpo), [Lesson 02](https://youtu.be/d6zL3YS69kM), [Lesson 03](https://youtu.be/j_62CGCBElo), [Lesson 49](https://youtu.be/AdcuSz6uBNI), and [Lesson 50](https://youtu.be/KpDK_Ah9_rI).

### Unit 2 — CPU, Hardware & Architecture

| # | Lesson | Revision Slides | Detailed Notes | MCQs + PYQs |
|---|--------|:---:|:---:|:---:|
| 04 | Organization of a Computer — input/output unit, memory, motherboard, buses, instruction cycle | `04-organization-of-computer` [x] | [x] | [x] |
| 05 | CPU, ALU, CU, Registers — control unit, ALU, registers, PC/IP, IR, accumulator, clock, cores, threads | `05-cpu-alu-cu-registers` [x] | [x] | [x] |
| 06 | CPU vs GPU & Microprocessor — serial vs parallel, CPU/GPU, microprocessor vs microcontroller | `06-cpu-gpu-microprocessor` [x] | [x] | [x] |
| 59 | Current CPU Architecture, Data Representation & RISC/CISC — von Neumann, addressing modes, cache-hit ratio, pipelining/data hazards, interrupts, PC/IR, two's-complement overflow, zero extension, BCD, byte-addressability, CISC vs RISC | `59-current-cpu-architecture-risc-cisc` [x] | [x] | [x] |

Video references: [Lesson 04](https://youtu.be/92XQ_n1t_cc), [Lesson 05](https://youtu.be/b6w8uT4GBYQ), and [Lesson 06](https://youtu.be/Vaod5Ox7lzM). Lesson 59 has no video yet.

### Unit 3 — Memory, Storage & Backup

| # | Lesson | Revision Slides | Detailed Notes | MCQs + PYQs |
|---|--------|:---:|:---:|:---:|
| 07 | Computer Memory Hierarchy — registers, cache, RAM, ROM, virtual memory ordering | `07-memory-hierarchy` [x] | [x] | [x] |
| 08 | RAM, ROM & Cache — RAM/DRAM/SRAM, ROM/PROM/EPROM/EEPROM, cache levels | `08-ram-rom-cache` [x] | [x] | [x] |
| 09 | Virtual Memory — virtual vs physical, allocation, paging/segmentation awareness | `09-virtual-memory` [x] | [x] | [x] |
| 10 | Storage Devices — HDD/SSD, magnetic/optical/flash/tape/cloud, CD/DVD/Blu-ray, random vs sequential access | `10-storage-devices` [x] | [x] | [x] |
| 11 | Backup Types — backup vs storage, full/incremental/differential/image/file, 3-2-1, offline/off-site, RAID vs backup | `11-backup-types` [x] | [x] | [x] |

### Unit 4 — I/O, Peripherals & Multimedia

| # | Lesson | Revision Slides | Detailed Notes | MCQs + PYQs |
|---|--------|:---:|:---:|:---:|
| 12 | Input Devices — keyboard, mouse, trackball, touchpad, joystick, light pen, stylus/tablet, touchscreen, scanner, webcam, microphone, biometrics | `12-input-devices` [x] | [x] | [x] |
| 13 | OCR, OMR, MICR — plus barcode, QR, RFID, biometric identification | `13-ocr-omr-micr` [x] | [x] | [x] |
| 14 | Output Devices — monitors, projector, speakers, headphones, plotters, MFP, hard vs soft copy | `14-output-devices` [x] | [x] | [x] |
| 15 | Printers & Displays — dot matrix, inkjet, laser, thermal, impact vs non-impact, page printers | `15-printers-displays` [x] | [x] | [x] |
| 16 | Computer Ports — USB/USB-C, HDMI, DisplayPort, VGA, Ethernet/RJ-45, audio, SATA, logical ports | `16-computer-ports` [x] | [x] | [x] |
| 65 | Current Multimedia, GUI & Media Formats — sampling, quantization, compression, synchronization; WYSIWYG, dialogue boxes; PNG/MP4/MP3; plotter; impact vs non-impact | `65-current-multimedia-gui-media-formats` [x] | [x] | [x] |

### Unit 5 — Software, Operating Systems, Windows & Utilities

| # | Lesson | Revision Slides | Detailed Notes | MCQs + PYQs |
|---|--------|:---:|:---:|:---:|
| 17 | Hardware, Software & Firmware — hardware, software, firmware, driver, humanware | `17-hardware-software-firmware` [ ] | [ ] | [ ] |
| 18 | Software Categories — system/application/utility/programming/embedded/middleware; proprietary/open-source/freeware/free/public-domain/commercial | `18-software-categories` [ ] | [ ] | [ ] |
| 19 | Operating System — kernel, GUI/CLI, boot, process/memory/file/device management, multitasking/time-sharing | `19-operating-system` [ ] | [ ] | [ ] |
| 20 | Windows Explorer — drives, folders, paths, extensions, hidden files, copy/move/delete, Recycle Bin | `20-windows-explorer` [ ] | [ ] | [ ] |
| 21 | Keyboard Shortcuts — high-yield Ctrl/Alt/Shift/Function-key combinations | `21-keyboard-shortcuts` [ ] | [ ] | [ ] |
| 45 | Open Source — source code, open source vs proprietary, freeware/free software/public domain/commercial | `45-open-source` [ ] | [ ] | [ ] |
| 46 | Firmware, BIOS, UEFI & Drivers — firmware, BIOS, UEFI, device drivers | `46-firmware-bios-uefi-drivers` [ ] | [ ] | [ ] |
| 52 | OS PYQ Traps & System Utilities — device driver as software, DMA/CPU bypass, RTOS, system vs application vs utility, DOS/UNIX/Linux distros, internal vs external hardware, `Winword`/Run, exact OS recognition | `52-os-pyq-traps-system-utilities` [ ] | [ ] | [ ] |
| 60 | Current OS, Processes, Linux & Utilities — deadlock recovery by preemption, priority inversion/inheritance, starvation, preemptive priority scheduling, RTOS, Linux kernel, `/root` vs `/home`, file systems, Windows Store, WordPad vs Notepad, Disk Cleanup, Defragmenter + SSD caution, Imaging Fax, `xcopy /s` | `60-current-os-processes-linux-utilities` [ ] | [ ] | [ ] |

### Unit 6 — Programming & Data Structures

| # | Lesson | Revision Slides | Detailed Notes | MCQs + PYQs |
|---|--------|:---:|:---:|:---:|
| 51 | Programming Foundations, Compiler & Data Structures — machine/assembly/high-level languages, assembler/compiler/interpreter, source/object/machine code, algorithm/flowchart, debugging, OOP, stack & LIFO, basic data-structure identification | `51-programming-foundations-compiler-data-structures` [ ] | [ ] | [ ] |

### Unit 7 — Office Applications & File Formats

| # | Lesson | Revision Slides | Detailed Notes | MCQs + PYQs |
|---|--------|:---:|:---:|:---:|
| 22 | MS Word Fundamentals — interface, editing, formatting, tables, images, headers/footers, page/section breaks, views, printing | `22-ms-word-fundamentals` [ ] | [ ] | [ ] |
| 23 | MS Word High-Yield — Find/Replace, spell check (F7), spell/grammar tools, hyperlinks, styles, comments, Track Changes, mail merge, PDF export | `23-ms-word-high-yield` [ ] | [ ] | [ ] |
| 24 | Excel Structure — workbook/worksheet/row/column/cell/range, formula bar, name box | `24-excel-structure` [ ] | [ ] | [ ] |
| 25 | Excel Formulas — formulas, operators, relative `A1`, absolute `$A$1`, mixed references | `25-excel-formulas` [ ] | [ ] | [ ] |
| 26 | Excel Functions — SUM/AVERAGE/COUNT/COUNTA/MAX/MIN/IF, AutoSum, error values | `26-excel-functions` [ ] | [ ] | [ ] |
| 27 | Excel Data Tools — sort, filter, tables, charts, PivotTables, protection, print | `27-excel-data-tools` [ ] | [ ] | [ ] |
| 28 | Access Database Basics — database/DBMS, MS Access, table/field/record, data types, validation/index | `28-access-database-basics` [ ] | [ ] | [ ] |
| 29 | Access Keys & Relationships — primary/foreign/composite keys, relationships, junction table, referential integrity, `.mdb` vs `.accdb` | `29-access-keys-relationships` [ ] | [ ] | [ ] |
| 30 | Access Queries, Forms & Reports — Table → Query → Form → Report, lookup, SQL awareness | `30-access-queries-forms-reports` [ ] | [ ] | [ ] |
| 31 | PowerPoint Basics — slides, placeholders, layouts, themes, templates, Slide Master, views/notes/handouts | `31-powerpoint-basics` [ ] | [ ] | [ ] |
| 32 | PowerPoint Animation & Transition — animation vs transition, Morph, F5/Shift+F5/Alt+F5/Esc | `32-powerpoint-animation-transition` [ ] | [ ] | [ ] |
| 33 | PDF & File Formats — PDF fixed-layout, editable source vs scan, DOCX/XLSX/PPTX/CSV/TXT/PNG, OCR, PDF/A, e-sign/redaction awareness | `33-pdf-file-formats` [ ] | [ ] | [ ] |
| 54 | Office Shortcut & Product Trap Lab — Word F7, Ctrl+H, Ctrl+K, Ctrl+X/V, Print Layout, Track Changes; PPT F5/Shift+F5/Alt+F5/Esc, handouts, Slide Master, orientation; Excel formula palette, `$A$1`; Access vs Word/Excel/MS-DOS; exact shortcut near-neighbours | `54-office-shortcut-product-trap` [ ] | [ ] | [ ] |
| 55 | File Formats & Named Technology Associations — PNG as image format, PDF behaviour, DOCX/XLSX/PPTX/CSV/TXT, `.mdb` vs `.accdb`, Firefox/Mozilla, C-DAC/PARAM, browser vs PDF reader vs remote-support, extension-vs-format trap | `55-file-formats-named-technology` [ ] | [ ] | [ ] |
| 61 | Current Office, Email & Statement Evaluation — Word content controls, Navigation Pane, first-line/hanging indents, Track Changes & metadata, Section vs Page Break; Excel nested IF, COUNTIFS, SUMPRODUCT, blank/non-numeric behaviour; email filters/rules, digital signature vs encryption, POP3 download, BCC privacy; PowerPoint SmartArt conversion | `61-current-office-email-statement-eval` [ ] | [ ] | [ ] |

### Unit 8 — Internet, Web & Email

| # | Lesson | Revision Slides | Detailed Notes | MCQs + PYQs |
|---|--------|:---:|:---:|:---:|
| 34 | Internet, WWW & Browser — Internet/WWW/website/webpage/homepage, browser vs search engine, client/server/ISP | `34-internet-www-browser` [ ] | [ ] | [ ] |
| 35 | URL, DNS, HTTP & HTTPS — URL anatomy, scheme/subdomain/domain/TLD, DNS, IP, HTTP/HTTPS/TLS | `35-url-dns-http-https` [ ] | [ ] | [ ] |
| 36 | Web Browsing, Search, Upload & Download — crawling/indexing/ranking, cookies/cache/history, upload/download/conversion | `36-web-browsing-search-upload-download` [ ] | [ ] | [ ] |
| 37 | Email Basics — address, To/Cc/Bcc, subject/body, attachment, folders, reply/forward, webmail vs client | `37-email-basics` [ ] | [ ] | [ ] |
| 38 | SMTP, POP & IMAP — SMTP/POP3/IMAP, mail-server flow, spam/phishing/spoofing, encryption/SSL-TLS | `38-smtp-pop-imap` [ ] | [ ] | [ ] |
| 39 | E-Banking — online banking, UPI, ATM PIN vs UPI PIN vs CVV, OTP/MFA, QR/collect-request safety | `39-e-banking` [ ] | [ ] | [ ] |
| 53 | Networking Legacy Services & Web Standards — packet vs circuit switching, Telnet, FTP, SMTP/POP/IMAP, W3C, DHTML, URL/DNS/IP, IPv4 vs IPv6, seven OSI layers, physical vs logical ports, service-role matching, negative stems | `53-networking-legacy-services-web-standards` [ ] | [ ] | [ ] |
| 63 | Current Web, HTML, JavaScript, VBScript & ASP.NET — HTML h1/marquee/ASCII-text document, valid tags/attributes; DHTML/XML/Java; JS string concatenation; VBScript `Dim`; Netscape/JS history; ASP.NET `Session`; meta-search engines (Dogpile) | `63-current-web-html-javascript-vbscript-aspnet` [ ] | [ ] | [ ] |

### Unit 9 — Networking

| # | Lesson | Revision Slides | Detailed Notes | MCQs + PYQs |
|---|--------|:---:|:---:|:---:|
| 40 | Networking Basics — network/node/host/client/server, PAN/LAN/MAN/WAN/WLAN/intranet, topologies, media, NIC/hub/repeater/bridge/switch/router/gateway/modem/AP/firewall | `40-networking-basics` [ ] | [ ] | [ ] |
| 41 | Networking Protocols — TCP/UDP/IP/DNS/DHCP/HTTP/HTTPS/FTP/Telnet/SMTP, OSI 7 layers, IPv4/IPv6, ports | `41-networking-protocols` [ ] | [ ] | [ ] |
| 62 | Current Internet, Networking & Cloud IaaS — TCP guarantees/ordering vs UDP, ICMP, BGP inter-domain routing, IPv6 address space/no-broadcast, HTTP/3 & QUIC vs TCP, DNS & `.org`/PIR/ICANN, ARPANET/packet switching, router assertion–reason, IaaS responsibility model | `62-current-internet-networking-cloud-iaas` [ ] | [ ] | [ ] |

### Unit 10 — Cybersecurity & IT Law

| # | Lesson | Revision Slides | Detailed Notes | MCQs + PYQs |
|---|--------|:---:|:---:|:---:|
| 42 | Malware — malware umbrella; virus/worm/Trojan/ransomware/spyware/adware/rootkit/keylogger/bot/backdoor/logic bomb/cryptojacking | `42-malware` [ ] | [ ] | [ ] |
| 43 | Hacking, Phishing & Spoofing — hacking, phishing, spoofing, social engineering, vulnerability/exploit | `43-hacking-phishing-spoofing` [ ] | [ ] | [ ] |
| 44 | Cybersecurity Prevention — antivirus/signatures/real-time/quarantine, firewall, patching, MFA, backup, incident response, CIA triad | `44-cybersecurity-prevention` [ ] | [ ] | [ ] |
| 56 | Cybersecurity, IT Act & Security Controls — IT Act 2000, malware umbrella, virus/worm/Trojan/ransomware, antivirus brands as historical distractors, anti-phishing, encryption, SSL/TLS, firewall, quarantine, patching, MFA, "which control does what" matching | `56-cybersecurity-it-act-security-controls` [ ] | [ ] | [ ] |
| 64 | Current Cybersecurity, Cryptography & Cyber Law — parasitic/file-infector virus, DES 64-bit block size, packet-filtering vs stateful/application/proxy firewalls, phishing vs ransomware/DDoS/hacking, Internet-governance concerns, privacy/data protection, Copyright Act section matching, encryption vs digital signature | `64-current-cybersecurity-cryptography-cyber-law` [ ] | [ ] | [ ] |

### Unit 11 — Governance & Integration

| # | Lesson | Revision Slides | Detailed Notes | MCQs + PYQs |
|---|--------|:---:|:---:|:---:|
| 47 | Humanware & IT Governance — humanware/users/operators/administrators; IT governance basics | `47-humanware-it-governance` [ ] | [ ] | [ ] |
| 57 | Digital Platforms & E-Governance Recognition — e-NAM & agricultural marketing, G2C/G2G/G2B/G2E, Digital India, NeGP/e-Kranti/NeGD distinctions, citizen portal, electronic records, authentication, named-platform matching | `57-digital-platforms-e-governance` [ ] | [ ] | [ ] |

### Unit 12 — Mastery, Retrieval & Audit

| # | Lesson | Revision Slides | Detailed Notes | MCQs + PYQs |
|---|--------|:---:|:---:|:---:|
| 48 | MCQ Masterclass — full-course rapid revision with direct-recall, contrast, classification and trap revision | `48-mcq-masterclass` [ ] | optional | drill set (this lesson *is* the MCQ artifact) |
| 58 | PYQ-Calibrated Final Retrieval & Audit — full-course mixed revision at 50% L1 / 35% L2 / 15% L3; negative-stem audit, defective-option audit, answer-rationale rules | `58-pyq-calibrated-final-retrieval-audit` [ ] | optional | drill set |
| 66 | Current-Paper Depth Audit & Technical-Post Routing — latest-paper revision workflow; tag items Core-General / Current-General / Technical-Post / Version-Sensitive; official source ledger | `66-current-paper-depth-audit-technical-post-routing` [ ] | optional | audit checklist |

---

## Exam blueprint & how the three deliverables map to it

This is a competitive-exam prep course, not a graded semester course — there is no internal assessment. The "assessment" is the live JKSSB paper. The three artifacts map to the three study needs:

| Study need | Artifact | Skill |
|------------|----------|-------|
| Fast last-mile recall of every definition/full form/shortcut/trap | **Revision Slides** | `/create-lecture` |
| Deep first-pass learning with worked examples and expanded contrasts | **Detailed Notes** | `/lecture-notes` |
| Simulated exam practice in the exact JKSSB item formats | **MCQs + PYQs** | `/competitive-exam-questions` |

**Item formats every MCQ set must include** (per the docx PYQ-calibration block): at least one NOT/EXCEPT/incorrect-statement item, one near-neighbour distractor set, one exact abbreviation/shortcut/command item, and a "why the other options are wrong" rationale for each item.

**Optional quality gates before a lesson ships:** `/verify-claims` (factual/citation audit of every PYQ claim), `/proofread`, and `/qa-notes` (Notes-vs-slides parity).

---

## Source & maintenance note

Calibrated against the researched JKSSB blueprint, the PYQ depth analysis, and the official current-paper sources listed in the source docx:

- JKSSB Previous Year Question Papers index — <https://jkssb.nic.in/QP.html>
- Junior Assistant 2026 paper — <https://jkssb.nic.in/Pdf/JuniorAssistant.pdf>
- Website Operator 2026 paper — <https://jkssb.nic.in/Pdf/WebsiteOperator.pdf>
- Computer Instructor/Operator 2025 paper — <https://jkssb.nic.in/Pdf/COMPUTER%20INSTRUCTOR%20-OPERATOR.pdf>
- Final answer keys (Junior Assistant 2026, Website Operator 2026 provisional, Computer Instructor/Operator 2025)

Before calling any lesson "current," check the exact target-post notification for syllabus, marks, negative marking, language, practical-test requirements and prescribed Office/software version. Verify every answer against the printed options and later official key notices; do not reproduce defective items as facts. Generated practice is never claimed to be an actual PYQ.

---

## Lesson → artifact work-list (hand to the build skills)

Each row is self-contained: hand the **Slides deck name** to `/create-lecture`, then run `/lecture-notes` and `/competitive-exam-questions` on the result. Quarto is not required. The video lesson is produced independently via the `prompt2render.py new "<NN> <Title>"` command from the source docx.

| # | Deck name (`JKSSB/NN-slug`) | Objective(s) | Source section (docx) |
|----|------------------------------|--------------|-----------------------|
| 01 | `JKSSB/01-what-is-a-computer` | Define computer, data, information, IPO, characteristics, applications, limitations | What Is a Computer |
| 02 | `JKSSB/02-types-of-computers` | Classify analog/digital/hybrid and size classes | Types of Computers |
| 03 | `JKSSB/03-bits-bytes-units` | Recall bit/nibble/byte/word and unit ladder (1024 convention) | Bits Bytes and Units |
| 04 | `JKSSB/04-organization-of-computer` | Identify units, memory, buses; trace instruction cycle | Organization of a Computer |
| 05 | `JKSSB/05-cpu-alu-cu-registers` | Name CPU functional units and registers (PC/IP, IR, accumulator) | CPU ALU CU Registers |
| 06 | `JKSSB/06-cpu-gpu-microprocessor` | distinguish CPU vs GPU, serial vs parallel, microprocessor vs microcontroller | CPU GPU Microprocessor |
| 07 | `JKSSB/07-memory-hierarchy` | Order the memory hierarchy | Computer Memory Hierarchy |
| 08 | `JKSSB/08-ram-rom-cache` | Classify RAM/DRAM/SRAM and ROM/PROM/EPROM/EEPROM; cache levels | RAM ROM Cache |
| 09 | `JKSSB/09-virtual-memory` | Distinguish virtual vs physical memory, allocation | Virtual Memory |
| 10 | `JKSSB/10-storage-devices` | Classify storage media and access modes | Storage Devices |
| 11 | `JKSSB/11-backup-types` | Classify full/incremental/differential/image/file; 3-2-1; RAID vs backup | Backup Types |
| 12 | `JKSSB/12-input-devices` | Identify and classify input devices | Input Devices |
| 13 | `JKSSB/13-ocr-omr-micr` | Match OCR/OMR/MICR/barcode/QR/RFID to purpose | OCR OMR MICR |
| 14 | `JKSSB/14-output-devices` | Classify output devices; hard vs soft copy | Output Devices |
| 15 | `JKSSB/15-printers-displays` | Classify printers by mechanism; impact vs non-impact | Printers Displays |
| 16 | `JKSSB/16-computer-ports` | Match ports (USB-C/HDMI/VGA/Ethernet…) to use | Computer Ports |
| 17 | `JKSSB/17-hardware-software-firmware` | Define hardware/software/firmware/driver/humanware | Hardware Software Firmware |
| 18 | `JKSSB/18-software-categories` | Classify software and licensing models | Software Categories |
| 19 | `JKSSB/19-operating-system` | State OS functions; kernel/GUI/CLI/boot/management | Operating System |
| 20 | `JKSSB/20-windows-explorer` | Navigate drives/folders/paths/extensions; file operations | Windows Explorer |
| 21 | `JKSSB/21-keyboard-shortcuts` | Recall high-yield shortcut set | Keyboard Shortcuts |
| 22 | `JKSSB/22-ms-word-fundamentals` | Word interface and core document operations | MS Word Fundamentals |
| 23 | `JKSSB/23-ms-word-high-yield` | Find/Replace, F7, styles, Track Changes, mail merge, PDF | MS Word High Yield |
| 24 | `JKSSB/24-excel-structure` | Workbook/worksheet/cell/range anatomy | Excel Structure |
| 25 | `JKSSB/25-excel-formulas` | Build formulas; distinguish relative/absolute/mixed references | Excel Formulas |
| 26 | `JKSSB/26-excel-functions` | Apply core functions; read error values | Excel Functions |
| 27 | `JKSSB/27-excel-data-tools` | Sort/filter/tables/charts/PivotTables | Excel Data Tools |
| 28 | `JKSSB/28-access-database-basics` | Define database objects; data types | Access Database Basics |
| 29 | `JKSSB/29-access-keys-relationships` | Distinguish key types; relationship/integrity | Access Keys Relationships |
| 30 | `JKSSB/30-access-queries-forms-reports` | Sequence Table→Query→Form→Report | Access Queries Forms Reports |
| 31 | `JKSSB/31-powerpoint-basics` | Slides/placeholders/layouts/themes/Slide Master/views | PowerPoint Basics |
| 32 | `JKSSB/32-powerpoint-animation-transition` | distinguish animation vs transition; exact F5 key set | PowerPoint Animation Transition |
| 33 | `JKSSB/33-pdf-file-formats` | PDF behaviour; format identification | PDF File Formats |
| 34 | `JKSSB/34-internet-www-browser` | distinguish Internet/WWW/webpage; browser vs search engine | Internet WWW Browser |
| 35 | `JKSSB/35-url-dns-http-https` | Parse URLs; DNS/IP; HTTP vs HTTPS | URL DNS HTTP HTTPS |
| 36 | `JKSSB/36-web-browsing-search-upload-download` | Search pipeline; cookies/cache/history; upload/download | Web Browsing Search Upload Download |
| 37 | `JKSSB/37-email-basics` | Email fields and operations | Email Basics |
| 38 | `JKSSB/38-smtp-pop-imap` | Match SMTP/POP3/IMAP to role; mail flow | SMTP POP IMAP |
| 39 | `JKSSB/39-e-banking` | distinguish PIN/OTP/CVV/MFA; safe-payment rules | E Banking |
| 40 | `JKSSB/40-networking-basics` | Classify networks/topologies/devices | Networking Basics |
| 41 | `JKSSB/41-networking-protocols` | Match protocols to layers/roles; ports | Networking Protocols |
| 42 | `JKSSB/42-malware` | Classify malware types | Malware |
| 43 | `JKSSB/43-hacking-phishing-spoofing` | distinguish attacks | Hacking Phishing Spoofing |
| 44 | `JKSSB/44-cybersecurity-prevention` | Map controls to threats; CIA triad | Cybersecurity Prevention |
| 45 | `JKSSB/45-open-source` | distinguish licensing models | Open Source |
| 46 | `JKSSB/46-firmware-bios-uefi-drivers` | distinguish firmware/BIOS/UEFI/driver | Firmware BIOS UEFI Drivers |
| 47 | `JKSSB/47-humanware-it-governance` | Define humanware; IT governance | Humanware IT Governance |
| 48 | `JKSSB/48-mcq-masterclass` | Full-course rapid recall (capstone) | MCQ Masterclass |
| 49 | `JKSSB/49-computer-generations-history` | Recollect generations and key associations | Computer Generations and History |
| 50 | `JKSSB/50-data-representation-number-systems-logic` | Convert bases; recall ASCII/RGB/gates | Data Representation Number Systems and Logic |
| 51 | `JKSSB/51-programming-foundations-compiler-data-structures` | distinguish language levels/tools; stack & LIFO | Programming Foundations Compiler and Data Structures |
| 52 | `JKSSB/52-os-pyq-traps-system-utilities` | Resolve OS/utility/DMA/Winword traps | Operating System PYQ Traps and System Utilities |
| 53 | `JKSSB/53-networking-legacy-services-web-standards` | Resolve legacy-service and web-standard traps | Networking Legacy Services and Web Standards |
| 54 | `JKSSB/54-office-shortcut-product-trap` | Exact Office shortcuts and product-category traps | Office Shortcut and Product Trap Lab |
| 55 | `JKSSB/55-file-formats-named-technology` | Format↔association matching | File Formats and Named Technology Associations |
| 56 | `JKSSB/56-cybersecurity-it-act-security-controls` | IT Act + security-control matching | Cybersecurity IT Act and Security Controls |
| 57 | `JKSSB/57-digital-platforms-e-governance` | Named-platform and G2x matching | Digital Platforms and E-Governance Recognition |
| 58 | `JKSSB/58-pyq-calibrated-final-retrieval-audit` | Mixed retrieval at 50/35/15 (capstone) | PYQ-Calibrated Final Retrieval and Audit |
| 59 | `JKSSB/59-current-cpu-architecture-risc-cisc` | von Neumann, addressing, hazards, BCD, RISC/CISC | Current CPU Architecture Data Representation and RISC CISC |
| 60 | `JKSSB/60-current-os-processes-linux-utilities` | Deadlock/priority/Linux/utility depth | Current Operating System Processes Linux and Utilities |
| 61 | `JKSSB/61-current-office-email-statement-eval` | Advanced Office/email statement evaluation | Current Office Email and Statement Evaluation |
| 62 | `JKSSB/62-current-internet-networking-cloud-iaas` | Modern networking/cloud assertions | Current Internet Networking and Cloud IaaS |
| 63 | `JKSSB/63-current-web-html-javascript-vbscript-aspnet` | Web scripting/markup recall | Current Web HTML JavaScript VBScript and ASP NET |
| 64 | `JKSSB/64-current-cybersecurity-cryptography-cyber-law` | Crypto/cyber-law matching | Current Cybersecurity Cryptography and Cyber Law |
| 65 | `JKSSB/65-current-multimedia-gui-media-formats` | Multimedia/UI/media-format recall | Current Multimedia GUI and Media Formats |
| 66 | `JKSSB/66-current-paper-depth-audit-technical-post-routing` | Depth routing + source ledger (capstone) | Current Paper Depth Audit and Technical-Post Routing |

---

*No JKSSB textbook or PYQ compilation has been indexed yet, so no reading is page-verified. To ground lessons in citable pages, drop a source into `master_supporting_docs/JKSSB/` and run `/index-textbook`; to upgrade PYQ provenance, register the official papers in `CompetitiveExam/Books/index.md`. See `.claude/rules/knowledge-base-JKSSB.md` (to be created when the first deck is built).*
