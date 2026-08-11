# Index: Algorithms and Data Structures (Niklaus Wirth) (Wirth2004)

**Source:** `master_supporting_docs/CS301/supporting_books/Wirth2004/book.pdf` — 179 PDF pages. Title page reads "Algorithms and Data Structures / © N. Wirth 1985 / (Oberon version: August 2004)".
**Indexed:** 2026-08-11
**Extraction method:** text-layer (`pypdf`), clean throughout. Minor artifacts: intra-word spaces from justified setting (`structur e`, `e ngineering`) and `ü`→`�` in "Zürich". Body text is otherwise faithful.

**Printed↔PDF page offset: `printed_page = pdf_page + 4`** (equivalently `pdf_page = printed_page − 4`). Verified at six points spanning the whole file (PDF 1→printed 5, 10→14, 50→54, 100→104, 150→154, 179→183) by reading the printed number in each page's header. Constant throughout; printed range is **5–183**.

**Which edition this is — read before citing.** The indexed artifact is the **August 2004 Oberon revision** of Wirth's 1985 text, distributed free by the author. Its page numbers do **not** match the 1985 Prentice-Hall print edition. Cite as `Wirth2004` and use these page numbers only for this PDF; if a student holds the print edition, give them the section number (`§4.2`), which is stable across both.

**Scope of this pass:** **complete section-level map, all five chapters** (extracted by regex over numbered section openers across the whole body, PDF pp. 6–179). This book is short enough that a full pass was cheap. Page-verified spot anchors are marked ✅.

**Language caveat (important for CS301):** the code is **Oberon** (Pascal-family), not C. `NEW(p)` is Oberon's allocator, not `malloc`. Cite this book for *concepts, structure, and analysis* — pointers, dynamic allocation, list and tree algorithms, AVL balancing — and translate all syntax to C per the notation registry in `.claude/rules/knowledge-base-CS301.md`. Wirth's `^` dereference and `POINTER TO` declarations must never appear on a CS301 slide.

## Chapter Index

| Chapter | Pages (printed) | Summary | Key Terms/Definitions | CS301 weeks |
|---------|------------------|---------|------------------------|-------------|
| 1 — Fundamental Data Structures | 11–44 | Data types and their representation in store; arrays, records, sets, files; closes with searching (linear, binary, string search) | data type, array, record, set, sequence/file, linear search, binary search, KMP, Boyer–Moore | 1, 3, 8 |
| 2 — Sorting | 45–86 | Sorting arrays (straight insertion/selection/exchange), advanced methods (Shell, tree, partition/quick, median), then sorting sequences (merge variants, polyphase) | straight insertion, straight selection, straight exchange, diminishing increment, tree sort, partition sort, merge sort, polyphase | 8, 9 |
| 3 — Recursive Algorithms | 87–108 | When recursion helps and when it does not; backtracking; eight queens; stable marriage; optimal selection | recursion, backtracking, when-not-to-use-recursion | 4 |
| 4 — Dynamic Information Structures | 109–176 | **The core chapter for CS301.** Recursive data types, pointers and dynamic allocation, linear lists, tree structures and traversal, **balanced (AVL) trees**, optimal search trees, B-trees, priority search trees | pointer, dynamic allocation, linear list, binary tree, tree search/insertion/deletion, **balanced tree, AVL, rotation**, B-tree | 1, 6, 7, 11 |
| 5 — Key Transformations (Hashing) | 177–183 | Hash functions, collision handling, and the analysis of key transformation | hash function, collision, key transformation, load factor | 10 |

## Section-level map (verified start pages, printed)

**Ch. 1 Fundamental Data Structures** — 1.1 Introduction **p.11** · 1.2 The Concept of Data Type **p.12** · 1.3 Primitive Data Types **p.14** · 1.4 Standard Primitive Types **p.15** (1.4.1 Integer p.15 · 1.4.2 REAL p.15 · 1.4.3 BOOLEAN p.16 · 1.4.4 CHAR p.16 · 1.4.5 SET p.17) · 1.5 The Array Structure **p.18** · 1.6 The Record Structure **p.20** · 1.7.1 Representation of Arrays **p.22** · 1.7.2 Representation of Records **p.23** · 1.7.3 Representation of Sets **p.24** · 1.8 The File or Sequence **p.24** (1.8.1 Elementary File Operators p.25 · 1.8.2 Buffering Sequences p.28 · 1.8.3 Buffering between Concurrent Processes p.29 · 1.8.4 Textual Input and Output p.31) · 1.9 Searching **p.33** (1.9.1 Linear Search **p.34** · 1.9.2 Binary Search **p.34** · 1.9.3 Table Search p.36 · 1.9.4 Straight String Search p.37 · 1.9.5 Knuth–Morris–Pratt p.38 · 1.9.6 Boyer–Moore p.41)

**Ch. 2 Sorting** — 2.1 Introduction **p.45** · 2.2 Sorting Arrays **p.46** (2.2.1 Straight Insertion **p.46** · 2.2.2 Straight Selection **p.48** · 2.2.3 Straight Exchange **p.50**) · 2.3 Advanced Sorting Methods **p.52** (2.3.1 Insertion Sort by Diminishing Increment p.52 · 2.3.2 Tree Sort p.53 · 2.3.3 Partition Sort **p.57** · 2.3.4 Finding the Median p.60 · 2.3.5 A Comparison of Array Sorting Methods **p.62**) · 2.4 Sorting Sequences **p.63** (2.4.1 Straight Merging p.63 · 2.4.2 Natural Merging p.66 · 2.4.3 Balanced Multiway Merging p.71 · 2.4.4 Polyphase Sort p.74 · 2.4.5 Distribution of Initial Runs p.81)

**Ch. 3 Recursive Algorithms** — 3.1 Introduction **p.87** · 3.2 When Not To Use Recursion **p.88** · 3.3 Two Examples of Recursive Programs **p.90** · 3.4 Backtracking Algorithms **p.94** · 3.5 The Eight Queens Problem **p.97** · 3.6 The Stable Marriage Problem **p.101** · 3.7 The Optimal Selection Problem **p.105**

**Ch. 4 Dynamic Information Structures** — 4.1 Recursive Data Types **p.109** · 4.2 Pointers **p.111** · 4.3 Linear Lists **p.115** (4.3.1 Basic Operations **p.115** · 4.3.2 Ordered Lists and Reorganizing Lists p.118 · 4.3.3 Topological Sorting ~p.122) · 4.4 Tree Structures **p.126** (4.4.1 Basic Concepts and Definitions **p.126** · 4.4.2 Basic Operations on Binary Trees **p.132** · 4.4.3 Tree Search and Insertion **p.135** · 4.4.4 Tree Deletion **p.139** · 4.4.5 Analysis of Tree Search and Insertion **p.140**) · 4.5 **Balanced Trees p.142** (4.5.1 Balanced Tree Insertion **p.143** · 4.5.2 Balanced Tree Deletion **p.147**) · 4.6 Optimal Search Trees **p.150** · 4.7 B-Trees **p.156** (4.7.1 Multiway B-Trees p.158 · 4.7.2 Binary B-Trees p.165) · 4.8 Priority Search Trees **p.171**

**Ch. 5 Key Transformations (Hashing)** — 5.1 Introduction **p.177** · 5.2 Choice of a Hash Function **p.177** · 5.3 Collision Handling **p.178** · 5.4 Analysis of Key Transformation **p.180**

## ✅ Page-verified anchors (safe to cite page-precisely)

| Printed page | What is there | Verified content | Useful for |
|---|---|---|---|
| **p.111** | §4.2 Pointers, opening paragraph | The defining property of recursive structures is **their ability to vary in size**; therefore "it is impossible to assign a fixed amount of storage" at compile time, so a compiler "cannot associate specific addresses" to their components. The resolution is **dynamic allocation** — allocating store to components *when they come into existence during program execution, instead of at translation time* — with the compiler reserving fixed storage to hold **the address** of the dynamically allocated component instead of the component itself. | **Week 1** — this is precisely the deck's "why the stack is not enough" argument and the "a pointer is a variable whose value is an address" definition, from a canonical source. The strongest single anchor in either book for Week 1. |

## Notes and cautions

- **This book is the AVL source for CS301.** §4.5 (pp. 142–149) does balanced-tree insertion and deletion explicitly, which the syllabus requires in Week 11 and which `Sedgewick2011` does *not* cover (Sedgewick uses red–black BSTs instead).
- **§4.2 is the pointer/dynamic-allocation anchor**, and §4.1 (recursive data types, p.109) is its motivation. Together they back Week 1's entire Act 2/Act 3.
- **Wirth writes "key transformation" for hashing.** The syllabus says "hashing"; §5 is the same topic. Wirth does not use the syllabus's "open hashing / closed hashing" terminology — see the anti-pattern note in `knowledge-base-CS301.md` requiring both names be defined wherever that pair appears.
- **No coverage of:** stacks and queues as named ADTs (Wirth builds lists directly — use `Sedgewick2011` §1.3 for Weeks 3 and 5), expression conversion (Week 4), graphs (Week 12), or file organization schemes (Week 10). Wirth's Ch. 2 §2.4 covers *external/sequence* sorting, which is adjacent to but not the same as the syllabus's file-organization topic.

## Cross-references

- `.claude/rules/textbook-grounding.md` — the invariant this index satisfies.
- `.claude/rules/knowledge-base-CS301.md` — Anchor Textbooks table; notation registry that overrides this book's Oberon syntax.
- `master_supporting_docs/CS301/supporting_books/Sedgewick2011/index.md` — companion index; covers stacks/queues/graphs/symbol tables this book omits.
