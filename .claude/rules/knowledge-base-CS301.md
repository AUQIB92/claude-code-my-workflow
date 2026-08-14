---
paths:
  - "Slides/CS301/**/*.tex"
  - "Quarto/CS301/**/*.qmd"
---

# Course Knowledge Base: Data Structures (PCC CS-301)

<!-- Starter KB bootstrapped 2026-08-10 while setting up the CS301 course from
     syllabi/Data-Structures.pdf, before any lecture .tex existed in
     Slides/CS301/. Entries below are therefore *projected forward* from
     syllabi/CS301.md's 12-week arc, not back-filled from authored decks.
     Symbols are marked (new) in the week that first introduces them and
     (projected) where no deck has confirmed them yet — flip (projected) to
     (confirmed) as each week's deck is authored, the way
     knowledge-base-CS401.md tracks its own registry. -->

## Course Profile

| Field | Value |
|---|---|
| Audience level | `undergrad` (B.Tech CSE, semester 3) |
| Programme position | semester 3 of 8 |
| Default difficulty | **`intro`** — explicit override (derived default would be `core` from `undergrad` + semester 3 per `.claude/rules/difficulty-levels.md`); set 2026-08-13 per instructor request |
| Exam target | GATE CS (via `/competitive-exam-questions`) |
| Implementation language | **C** — the notation registry below overrides any anchor book's language (Sedgewick is Java, Wirth is Oberon) |

## Anchor Textbooks

| Book (ShortName) | Index | Weeks/Lectures Backed | Page-Verified? |
|-------------------|-------|------------------------|-----------------|
| Horowitz & Sahni, *Fundamentals of Data Structures*, 2nd ed., 2008 (HorowitzSahni2008) | `master_supporting_docs/CS301/supporting_books/HorowitzSahni2008/index.md` — **not built; no PDF supplied.** Primary text per the institute syllabus. | Weeks 1–12 (the spine of the course) | **No — chapter-level attribution only** |
| Aho, Hopcroft & Ullman, *Data Structures and Algorithms*, 1st ed., 1983 (AhoHopcroftUllman1983) | `master_supporting_docs/CS301/supporting_books/AhoHopcroftUllman1983/index.md` — **not built; no PDF supplied.** Second prescribed text. | Weeks 1, 3–12 (ADT framing, sorting, trees, graphs) | **No — chapter-level attribution only** |
| Knuth, *TAOCP Vol. 1: Fundamental Algorithms* (Knuth1997v1) | `master_supporting_docs/CS301/supporting_books/Knuth1997v1/index.md` — **not built.** Reference, not a spine text. Note: sorting/searching live in **Vol. 3**, not Vol. 1 — the syllabus lists only Vol. 1, so Week 8–9 references to Knuth must name Vol. 3 explicitly rather than silently reusing the Vol. 1 entry. | Weeks 1–2 (reference depth); Weeks 8–9 via Vol. 3 | **No — chapter-level attribution only** |
| Neapolitan & Naimipour, *Foundations of Algorithms*, Jones & Bartlett, 2010 (Neapolitan2010) | `master_supporting_docs/CS301/supporting_books/Neapolitan2010/index.md` — **not built.** Strongest of the listed books on complexity analysis. | Weeks 2, 8–9 (analysis, divide-and-conquer) | **No — chapter-level attribution only** |
| Morin, *Open Data Structures: An Introduction*, UBC Press, 2013 (Morin2013) | `master_supporting_docs/CS301/supporting_books/Morin2013/index.md` — **not built, but the cheapest one to build.** **Openly licensed and freely downloadable** — this is the first book to run `/index-textbook CS301/Morin2013` against when a page-verified anchor is wanted, since it needs no purchased PDF. | Weeks 3–12 (all structures; strong on lists, hashing, trees, graphs) | **No — but unblocked; open licence, index whenever** |
| *Data Structures with C*, Schaum's Outline Series (SchaumsC) | `master_supporting_docs/CS301/supporting_books/SchaumsC/index.md` — **not built.** Problem source rather than exposition; useful for `/create-assignment` and `/scaffold-exercises`. | Weeks 3–12 (worked problems) | **No — chapter-level attribution only** |
| **Sedgewick & Wayne, *Algorithms*, 4th ed., 2011 (Sedgewick2011)** | `master_supporting_docs/CS301/supporting_books/Sedgewick2011/index.md` — ✅ **BUILT 2026-08-11.** Full chapter+section map; offset `pdf = printed + 13` verified at 9 points. Code is **Java** — cite for definitions/analysis, never syntax. | Weeks 1–3, 5–12 (ADT, collections, analysis, sorting, symbol tables, BST, hashing, graphs) | ✅ **Yes — page-verified anchors at pp. 64, 120, 142, 172, 187** |
| **Wirth, *Algorithms and Data Structures* (Oberon rev., 2004 / ©1985) (Wirth2004)** | `master_supporting_docs/CS301/supporting_books/Wirth2004/index.md` — ✅ **BUILT 2026-08-11.** Complete section map, all 5 chapters; offset `printed = pdf + 4` verified at 6 points. Code is **Oberon** — cite for concepts, never syntax. **The AVL source** (§4.5), which Sedgewick lacks. | Weeks 1, 3–4, 6–11 (pointers/dynamic allocation, lists, trees, AVL, hashing, sorting) | ✅ **Yes — page-verified anchor at p. 111** |
| **Karumanchi, *Data Structures And Algorithms Made Easy*, CareerMonk, 2017 (Karumanchi2017)** | `master_supporting_docs/CS301/supporting_books/Karumanchi2017/index.md` — ✅ **BUILT 2026-08-11.** Full 21-chapter map, no printed folios in this edition (cite as "p. N (PDF)"). Language-neutral C-style pseudocode (`struct`/pointer fields) throughout. **NOT a Week 1 anchor** — Step 0.5 found zero coverage of "structured programming" or `malloc`/`calloc`/`realloc`/`free`; only the ADT concept is well covered there. Its real strength is depth on Weeks 2–3, 5–12 (its chapters map almost 1:1 onto the rest of the syllabus, and it is the only anchor with dedicated Union-Find, string-matching (KMP/Rabin–Karp/Boyer–Moore), and selection-algorithm (median-of-medians) chapters). | Weeks 2–3, 5–12 (algorithm analysis, stacks/queues, linked lists, trees/AVL, graphs, sorting/searching, hashing) — **not Week 1's C-memory-management content** | ✅ **Yes — page-verified anchors throughout (chapter-boundary-checked at 21 points)** |

<!-- [LEARN:textbook-grounding] UPDATED 2026-08-11 (second pass) — three books are
     now supplied and indexed: Sedgewick2011, Wirth2004, and Karumanchi2017. All
     three carry page-verified anchors (see the ✅ tables in their index.md
     files), so CS301 material may cite specific pages from any of them —
     EXCEPT Karumanchi2017 for Week 1's C-memory-management claims (structured
     programming, malloc/calloc/realloc/free), which Step 0.5 confirmed it does
     not cover at all. Week 1's pointer/malloc/free content stays grounded in
     Wirth2004 or general/standard treatment; Karumanchi2017 is the strongest
     anchor for Weeks 2-3 and 5-12 instead.

     STILL NOT INDEXED: the two institute-prescribed *text* books, Horowitz &
     Sahni and Aho-Hopcroft-Ullman, plus Knuth, Neapolitan, Morin, and Schaum's.
     References to those remain honest *chapter-level* attribution drawn from
     the syllabus's own book list — NOT page-verified, and must not be presented
     as such. Per textbook-grounding.md: phrase them as general/standard
     treatment; never invent a page number.

     NOTE THE MISMATCH: none of the three indexed books is on the institute's
     prescribed list, and the two prescribed texts are still NOT indexed.
     Sedgewick, Wirth, and Karumanchi are legitimate, canonical anchors and are
     safe to cite — but when a claim must be traceable to the *prescribed* text
     for exam or audit purposes, that still requires indexing Horowitz & Sahni.
     Morin2013 remains the cheapest remaining target (openly licensed, no
     purchase needed). -->

<!-- [LEARN:textbook-grounding] Language mismatch is a standing hazard for this
     course: Sedgewick is Java, Wirth is Oberon, and CS301 is taught in C.
     Cite either book for definitions, cost analysis, and algorithm structure —
     never for implementation syntax. Wirth's `NEW(p)`/`POINTER TO`/`^` and
     Sedgewick's Java generics must never reach a CS301 slide; the Notation
     Registry below governs. -->

## Notation Registry

| Rule | Convention | Example | Anti-Pattern |
|------|-----------|---------|-------------|
| Input size | `$n$` always denotes the number of elements in the structure under discussion; state what `$n$` counts at first use in each deck | "for an array of $n$ integers" | Reusing $n$ for two different quantities in one deck |
| Running time | `$T(n)$` for the exact cost function; asymptotic classes only inside `$O(\cdot)$`, `$\Omega(\cdot)$`, `$\Theta(\cdot)$` | $T(n) = 3n + 2 = O(n)$ | Writing $T(n) = O(n)$ and then treating $T(n)$ as exact |
| Asymptotic classes | Math mode with proper spacing; `\log` as an operator, never italic `log` | $O(n \log n)$, $\Theta(n^2)$ | `O(nlogn)`, `O(n*log(n))`, italic $log$ |
| Array indexing | **0-based**, matching C; ranges written `A[0..n-1]` | `A[0]` is the first element | Switching to 1-based mid-deck; `A[1..n]` alongside C code |
| Array elements | `A[i]` in math; `\texttt{A[i]}` in prose | "compare $A[i]$ with $A[j]$" | `A_i` subscript form (reserve subscripts for sequences, not arrays) |
| Identifiers & code | `\texttt{}` for every C identifier, type, and function name in prose | `\texttt{malloc}`, `\texttt{struct node}`, `\texttt{head}` | Bare `malloc` in running prose; italicizing identifiers |
| Node & pointer types | `\texttt{struct node *}` for a node pointer; the list handle is always `\texttt{head}`, the tree handle always `\texttt{root}` | `\texttt{struct node *head = NULL;}` | Renaming `\texttt{head}` to `\texttt{start}`/`\texttt{first}` between decks |
| Null pointer | `\texttt{NULL}` — uppercase, C convention | `\texttt{p->next == NULL}` | `null`, `nil`, `\texttt{0}` as a pointer literal |
| Pointer dereference | Arrow form `\texttt{p->field}` for struct members; `\texttt{*p}` only for whole-object deref | `\texttt{p->data}`, `\texttt{p->next}` | `\texttt{(*p).data}` in slides (correct C, but noise) |
| Stack / queue operations | Verb names in `\texttt{}`: `\texttt{push}`/`\texttt{pop}`/`\texttt{peek}`, `\texttt{enqueue}`/`\texttt{dequeue}`/`\texttt{front}` | "`\texttt{push}` the operator" | Mixing `\texttt{insert}`/`\texttt{delete}` into stack/queue vocabulary |
| ADT vs. implementation | Name the ADT in prose ("a stack"), the implementation in `\texttt{}` ("array-based `\texttt{stack}`"); never conflate | "a queue, implemented here as a circular array" | "the array is a queue" |
| Complexity claims | Always paired with the case: worst / average / best, and the operation named | "search is $O(n)$ worst case" | Bare "binary search is $O(\log n)$" with no case stated |
| Memory diagrams | Stack (automatic) memory grows downward, heap upward, drawn consistently across all decks | Week 1 memory-layout figure sets the orientation | Flipping heap/stack orientation between decks |

## Symbol Reference

| Symbol | Meaning | Introduced |
|--------|---------|------------|
| $n$ | Number of elements in the structure under discussion | **Week 1 (new)** |
| ADT | Abstract Data Type — the operations and their contract, stated independently of any implementation | **Week 1 (new)** |
| `\texttt{malloc}` / `\texttt{calloc}` / `\texttt{realloc}` / `\texttt{free}` | C heap-allocation interface; `\texttt{calloc}` zero-initializes, `\texttt{realloc}` may move the block, every `\texttt{malloc}` needs a matching `\texttt{free}` | **Week 1 (new)** |
| `\texttt{NULL}` | The null pointer — no valid object; dereferencing it is undefined behaviour | **Week 1 (new)** |
| `\texttt{sizeof}` | Compile-time size in bytes of a type or object; the unit of every allocation request | **Week 1 (new)** |
| Stack vs. heap | Automatic storage (function frames, freed on return) vs. dynamic storage (explicit lifetime, freed by `\texttt{free}`) | **Week 1 (new)** |
| Dangling pointer / leak | Pointer to freed memory (use-after-free) vs. allocated memory with no live pointer to it | **Week 1 (new)** |
| $T(n)$ | Exact running-time cost function in the chosen basic operation | **Week 2 (projected)** |
| $O$, $\Omega$, $\Theta$, $o$, $\omega$ | Asymptotic upper / lower / tight bounds, and their strict forms | **Week 2 (projected)** |
| $S(n)$ | Space complexity — auxiliary space, stated separately from input space | **Week 2 (projected)** |
| Best / worst / average case | Cost over the most favourable / least favourable / expected input of size $n$ — a *case*, orthogonal to the *bound* ($O$/$\Theta$) | **Week 2 (projected)** |
| `\texttt{top}` | Stack index of the most recently pushed element; $-1$ denotes empty in the array implementation | **Week 3 (projected)** |
| Row-major address | $\text{addr}(A[i][j]) = \text{base} + ((i \times c) + j) \times w$ for a $r \times c$ array of $w$-byte elements | **Week 3 (projected)** |
| Infix / postfix / prefix | Operator between / after / before its operands; postfix and prefix need no parentheses or precedence rules | **Week 4 (projected)** |
| `\texttt{front}` / `\texttt{rear}` | Queue indices of the next element to dequeue and the last enqueued | **Week 5 (projected)** |
| Circular queue wraparound | Index advance is $(\texttt{rear} + 1) \bmod \text{capacity}$; full and empty are distinguished by a count or a sacrificed slot | **Week 5 (projected)** |
| `\texttt{head}` | Pointer to the first node of a linked list; `\texttt{NULL}` when the list is empty | **Week 6 (projected)** |
| `\texttt{p->next}` / `\texttt{p->prev}` | Successor / predecessor links in singly and doubly linked lists | **Week 6–7 (projected)** |
| Stable sort | A sort preserving the relative order of equal keys — the property that makes radix sort work | **Week 8–9 (projected)** |
| In-place / auxiliary space | Sorting with $O(1)$ extra space vs. requiring $\Theta(n)$ (merge sort's merge buffer) | **Week 9 (projected)** |
| Load factor $\alpha$ | $\alpha = n/m$ — entries over table slots; drives expected probe count in hashing | **Week 10 (projected)** |
| Open / closed hashing | Open (separate chaining): collisions in per-slot lists. Closed (open addressing): collisions probed into other slots. **The names are historically confusing — define both explicitly every time.** | **Week 10 (projected)** |
| `\texttt{root}` | Handle to a tree's root node; `\texttt{NULL}` for the empty tree | **Week 11 (projected)** |
| Height $h$ | Longest root-to-leaf edge count; a single node has $h = 0$, the empty tree $h = -1$ (state the convention, it varies by book) | **Week 11 (projected)** |
| Balance factor | $\text{height(left)} - \text{height(right)}$; an AVL node is balanced when it lies in $\{-1, 0, +1\}$ | **Week 11 (projected)** |
| $G = (V, E)$ | Graph with vertex set $V$ and edge set $E$; $\lvert V \rvert = n$, $\lvert E \rvert = m$ | **Week 12 (projected)** |
| Adjacency matrix / list | $\Theta(n^2)$ space, $O(1)$ edge query vs. $\Theta(n + m)$ space, $O(\deg v)$ scan — the density trade-off | **Week 12 (projected)** |

## Lecture Progression

| # | Title | Core Question | Key Notation | Key Method |
|---|-------|--------------|-------------|------------|
| 1 | Foundations, Pointers & ADTs | Where does a program's data actually live, and who owns its lifetime? | `\texttt{malloc}`/`\texttt{free}`, `\texttt{NULL}`, ADT | Memory-layout tracing; allocate/free discipline |
| 2 | Algorithm Analysis | What does an operation cost, and how do we compare two solutions without running them? | $T(n)$, $O/\Omega/\Theta$, best/worst/average | Counting basic operations → asymptotic class |
| 3 | Arrays & Stacks | What is the simplest useful ADT, and what does an array buy and cost us? | `\texttt{top}`, row-major address | Array address arithmetic; push/pop tracing |
| 4 | Expression Evaluation & Recursion | Why do compilers rewrite arithmetic before evaluating it? | infix/postfix/prefix | Stack-driven conversion and evaluation traces |
| 5 | Queues | What changes when the first element out is the first one in? | `\texttt{front}`/`\texttt{rear}`, mod wraparound | Circular-index arithmetic; priority ordering |
| 6 | Singly Linked Lists | When is a pointer chain worth the loss of random access? | `\texttt{head}`, `\texttt{p->next}` | Pointer surgery: insert, delete, reverse |
| 7 | Doubly Linked Lists & Applications | What does a backward link buy, and what does it cost? | `\texttt{p->prev}` | Two-link invariant maintenance; polynomial merge |
| 8 | Searching & Elementary Sorting | How much does sorted order accelerate search, and what is the cheapest way to get it? | $O(\log n)$, stability | Loop-invariant argument; comparison counting |
| 9 | Efficient Sorting | Why can't a comparison sort beat $n \log n$, and what escapes that bound? | in-place, auxiliary space | Divide-and-conquer recurrences; partition traces |
| 10 | File Organization & Hashing | How do we find a record in one probe instead of $n$? | load factor $\alpha$, open/closed hashing | Hash-function design; collision-resolution tracing |
| 11 | Trees, BSTs & AVL | How do we keep search logarithmic when the data keeps changing? | `\texttt{root}`, height $h$, balance factor | Traversal recursion; rotation case analysis |
| 12 | Graphs: Traversal, MST, Shortest Paths | How do we reason about arbitrary connections rather than a fixed shape? | $G = (V,E)$, adjacency matrix/list | BFS/DFS frontier tracing; greedy-choice arguments |

## Empirical Applications

| Application | Paper | Dataset | Lecture(s) | Purpose |
|------------|-------|---------|------------|---------|
| **The expression-processor thread** — build a small calculator end to end: tokenize `\texttt{(a+b)*c}`, check its parentheses, convert it to postfix, evaluate it, then index and look up the identifiers it uses | Horowitz & Sahni Ch. 3 (stacks/queues); Aho–Hopcroft–Ullman Ch. 2 | n/a (worked structure traces) | Weeks 3–5 (stacks, expression conversion, queues), 6–7 (symbol table as a list), 10 (symbol table as a hash table), 11 (expression tree) | The course's single running artifact. Each new structure is introduced as *the fix for a concrete deficiency the calculator just hit*, so the syllabus's structure list becomes one evolving program rather than twelve disconnected topics. Also delivers the Week 10 vs. Week 6 payoff: the same symbol table, $O(n)$ as a list vs. $O(1)$ expected as a hash table. |
| **The allocation-lifetime trace** — one `\texttt{struct node}` followed from `\texttt{malloc}` through insertion, traversal, and `\texttt{free}` | Horowitz & Sahni Ch. 1, 4 | n/a (worked memory trace) | Week 1 (introduced), Weeks 6–7 (linked lists), 11 (trees) | Makes ownership and lifetime concrete before pointers get hard. The Week 1 diagram is redrawn at each structure so leaks and dangling pointers are diagnosed visually, not just warned about. |

## Design Principles

| Principle | Evidence | Lectures Applied |
|-----------|----------|-----------------|
| Introduce every structure as the answer to a deficiency the previous structure just exhibited — never as the next item in a list | The syllabus is a catalogue; a catalogue taught in order produces memorization without selection skill. The whole point of the course is *choosing* a structure | All weeks; the expression-processor thread is the mechanism |
| State the ADT contract before any implementation, and implement the same ADT at least twice | Stack over array (Wk 3) then over a list (Wk 7); queue over circular array (Wk 5) then over a list (Wk 7). Two implementations of one contract is what makes the abstraction visible | Weeks 3, 5, 7 |
| Pair every complexity claim with the case *and* a trace that exhibits it | "Quick sort is $O(n \log n)$" is the single most common misconception this course must dismantle — students must see the sorted-input worst case traced | Weeks 2, 8, 9, 10, 11 |
| Draw memory, don't describe it | Pointer bugs are spatial. A consistent memory diagram (stack down, heap up, arrows to nodes) reused across Weeks 1, 6, 7, 11 does more than any prose warning | Weeks 1, 6, 7, 11 |

## Anti-Patterns (Don't Do This)

| Anti-Pattern | What Happened | Correction |
|-------------|---------------|-----------|
| Presenting "open hashing" and "closed hashing" without immediately defining both | The names are historically inverted relative to intuition (open hashing = chaining, closed hashing = open addressing), and the syllabus uses the confusing pair | Define both on the slide that names them, and give each its alternative name (separate chaining / open addressing) |
| Teaching binary search before establishing the sorted precondition as an invariant | Students apply it to unsorted arrays and get plausible-looking wrong answers | State the precondition in the ADT contract, then show a failure trace on unsorted input |

## R Code Pitfalls

| Bug | Impact | Fix |
|-----|--------|-----|
| | | |

<!-- This course has no R/statistical component in Weeks 1-12 per syllabi/CS301.md;
     the R Code Pitfalls table is left empty by design, not an oversight. The
     course's code is C throughout — C-specific hazards (leaks, use-after-free,
     off-by-one on array bounds, unchecked malloc) are tracked in the Notation
     Registry and Anti-Patterns tables above instead. -->
