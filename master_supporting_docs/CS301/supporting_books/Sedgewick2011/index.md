# Index: Algorithms, 4th ed. (Robert Sedgewick & Kevin Wayne) (Sedgewick2011)

**Source:** `master_supporting_docs/CS301/supporting_books/Sedgewick2011/book.pdf` — 969 PDF pages. Metadata `/Title` confirms "Algorithms, Fourth Edition" (Addison-Wesley, 2011).
**Indexed:** 2026-08-11
**Extraction method:** text-layer (`pypdf`). The text layer is clean for body prose, but **two artifacts matter when quoting**: (a) section and subsection headings are letter-spaced in the extraction (`L i n k e d l i s t s`, `d e ﬁ n e`), so heading strings will not match a naive grep; (b) minus signs and some symbols extract as XML entities (`/H11002` for `−`). Do not paste extracted text verbatim into a slide without re-reading the page.

**Printed↔PDF page offset: `pdf_page = printed_page + 13`.** Verified at nine independent points (printed 64, 172, 243, 362, 396, 458, 518, 604, 638) by reading each page's footer, which carries the printed number. The offset is constant across the whole body — no inserted plates. Front matter (cover, copyright, contents, preface) is roman-numbered and occupies PDF pages 1–20.

**Scope of this pass:** full **chapter and section-level** map for Chapters 1–6 (every section start page below is taken from the book's own Contents, PDF pp. 7–8). **Page-verified spot anchors** are marked ✅ — these were read directly and may be cited page-precisely. Everything else is section-range granularity: cite the section, not a specific page, until verified. Extend this file as later weeks need page-precise anchors.

**Language caveat (important for CS301):** this book's code is **Java**. CS301 is a **C** course. Cite it for *definitions, cost analysis, algorithm structure, and diagrams* — not for implementation syntax. Where the syllabus wants C, the notation registry in `.claude/rules/knowledge-base-CS301.md` governs, not Sedgewick's Java.

## Chapter Index

| Chapter | Pages (printed) | Summary | Key Terms/Definitions | CS301 weeks |
|---------|------------------|---------|------------------------|-------------|
| 1 — Fundamentals | 3–242 | The programming model, data abstraction (the ADT), the three collection ADTs, cost analysis, and union-find as a worked case study | data type, abstract data type, API, client/implementation, linked list, order of growth, union-find | 1, 2, 3, 5, 6, 7 |
| 2 — Sorting | 243–360 | Elementary sorts, then mergesort/quicksort with their analyses, priority queues and heapsort, and a survey of sorting applications | selection/insertion/shell sort, mergesort, quicksort, partition, priority queue, binary heap, stability | 8, 9 |
| 3 — Searching | 361–514 | Symbol tables as the unifying ADT, then three implementations compared: BSTs, balanced (red–black) trees, and hash tables | symbol table, BST, red–black BST, hash function, separate chaining, linear probing, load factor | 10, 11 |
| 4 — Graphs | 515–694 | Undirected and directed graphs, their representations and traversals, minimum spanning trees, and shortest paths | adjacency list, DFS, BFS, connected components, MST, Prim, Kruskal, Dijkstra | 12 |
| 5 — Strings | 695–852 | String sorts, tries, substring search, regular expressions, data compression | radix sort, LSD/MSD, trie, KMP, Huffman | 9 (radix sort only) |
| 6 — Context | 853–932 | Relations to other fields; reductions and intractability | reduction, NP-completeness | — (beyond syllabus) |

## Section-level map (start pages, from the book's Contents)

**Ch. 1 Fundamentals:** 1.1 Basic Programming Model **p.8** · 1.2 Data Abstraction **p.64** · 1.3 Bags, Queues, and Stacks **p.120** · 1.4 Analysis of Algorithms **p.172** · 1.5 Case Study: Union-Find **p.216**

**Ch. 2 Sorting:** 2.1 Elementary Sorts **p.244** · 2.2 Mergesort **p.270** · 2.3 Quicksort **p.288** · 2.4 Priority Queues **p.308** · 2.5 Applications **p.336**

**Ch. 3 Searching:** 3.1 Symbol Tables **p.362** · 3.2 Binary Search Trees **p.396** · 3.3 Balanced Search Trees **p.424** · 3.4 Hash Tables **p.458** · 3.5 Applications **p.486**

**Ch. 4 Graphs:** 4.1 Undirected Graphs **p.518** · 4.2 Directed Graphs **p.566** · 4.3 Minimum Spanning Trees **p.604** · 4.4 Shortest Paths **p.638**

**Ch. 5 Strings:** 5.1 String Sorts **p.702** · 5.2 Tries **p.730** · 5.3 Substring Search **p.758** · 5.4 Regular Expressions **p.788** · 5.5 Data Compression **p.810**

**Ch. 6 Context:** **p.853**. Index **p.933**.

## ✅ Page-verified anchors (safe to cite page-precisely)

| Printed page | What is there | Verified wording / content | Useful for |
|---|---|---|---|
| **p.64** | Section 1.2 opener, **the data-type definition** | "A data type is a set of values and a set of operations on those values." Continues into *data abstraction* as the process of defining and using data types. | **Week 1** — the ADT contract. This is the cleanest one-sentence ADT definition in either CS301 book. |
| **p.120** | Section 1.3 opener | Introduces bag, queue, stack as three collection types differing only in "which object is to be removed or examined next." | **Weeks 3, 5** — stack/queue ADTs; **Week 1** as the motivating example of one contract, several structures. |
| **p.142** | "Linked lists" subsection, with a formal **Definition** | "A linked list is a recursive data structure that is either empty (null) or a reference to a node…" Framed as "our first example of building a data structure not directly supported by the language." | **Weeks 1, 6, 7** — the linked-list definition and the node-chain framing. |
| **p.172** | Section 1.4 opener | Opens on "How long will my program take? Why does my program run out of memory?" and notes such questions are "much too vague to be answered precisely" without a model. | **Week 2** — motivating cost analysis; also **Week 1**'s "it felt fast is not an argument". |
| **p.187** | **Order-of-growth classification table** | Tabulates constant `1`, logarithmic `log N`, linear `N`, linearithmic `N log N`, quadratic `N²`, cubic `N³` — each with a description, a code framework, and an example (binary search for logarithmic, mergesort for linearithmic). | **Week 2** — the orders-of-growth table; **Week 0** for the cost-comparison motivation. |

## Notes and cautions

- **Cross-check before citing a page not in the ✅ table.** Section start pages above come from the book's own Contents and are reliable *as section starts*; they do not license "p.396 says X" for arbitrary X.
- **Symbol tables (3.1) are the book's name for what CS301 calls a lookup table / dictionary.** The expression-processor thread's identifier table maps onto §3.1 (list-based) → §3.4 (hash-based), which is exactly the Week 6 → Week 10 payoff in `knowledge-base-CS301.md`.
- **Balanced trees are red–black here, not AVL.** The CS301 syllabus specifies **AVL** trees and AVL rotations (Week 11). Sedgewick §3.3 covers red–black BSTs and 2–3 trees; the *balancing motivation* transfers, the *specific rotations do not*. Use `Wirth2004` §4.5 for AVL proper — Wirth does AVL explicitly.
- **No coverage of:** infix/postfix/prefix conversion as a syllabus topic in its own right (Week 4 — Dijkstra's two-stack algorithm appears inside §1.3 but its page was not verified in this pass), Tower of Hanoi, file organization (Week 10's sequential/direct/indexed-sequential material), or polynomial manipulation via linked lists (Week 7).

## Cross-references

- `.claude/rules/textbook-grounding.md` — the invariant this index satisfies.
- `.claude/rules/knowledge-base-CS301.md` — Anchor Textbooks table; notation registry that overrides this book's Java conventions.
- `master_supporting_docs/CS301/supporting_books/Wirth2004/index.md` — the companion index; covers AVL trees and pointer/dynamic-allocation material this book treats only in Java terms.
