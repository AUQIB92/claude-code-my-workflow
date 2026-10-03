/*
 * dlist.h — the Doubly-Linked-List and Sparse-Polynomial ADT contracts for
 * Week 7 (CS301): P7 "doubly-linked-list operations", plus the week's
 * polynomial application (Part B).
 *
 * The contract says WHAT each function must do, not HOW the chain is laid
 * out. This header is given to you; do NOT change it. Your job is to provide
 * every function below in dlist.c (start from starter_dlist.c).
 *
 * -----------------------------------------------------------------------------
 * Part A — representation (deck: Week 7, Sections 1-2; notes Figures 7.1-7.3)
 * -----------------------------------------------------------------------------
 *
 *   struct dnode { int data; struct dnode *prev; struct dnode *next; };
 *
 * `head` is the ONLY entry point (NULL when empty). The first node's `prev`
 * is NULL and the last node's `next` is NULL. Nodes live anywhere in the
 * heap — order lives in the LINKS, never in the layout. Every node is
 * separately malloc'd; every malloc needs a matching free (dlist_free, or one
 * delete per node).
 *
 * THE TWO-LINK INVARIANT (the single correctness condition for a DLL): after
 * every operation, for each interior node p, p->next->prev == p AND
 * p->prev->next == p. An insert or delete must repair BOTH links, not one.
 * The hidden suite re-checks this invariant after every operation.
 *
 * The back (tail) end: this ADT caches NO tail handle. Delete-by-pointer
 * (dlist_delete_node) is still O(1) because prev reaches the neighbours
 * directly; but operations that must first FIND the last node (insert_back,
 * delete_back, print_backward) walk the chain in O(n) worst case. A cached
 * tail (Week 7's list-backed queue) would make the back end O(1) — this
 * assignment leaves that trade-off visible rather than hiding it.
 *
 * Memory discipline (graded):
 *   - check every malloc for NULL before dereferencing;
 *   - free exactly once per node; never touch a node after freeing it;
 *   - dlist_free sets *head to NULL so a second free is a safe no-op.
 *
 * Complexity (deck Section 1 price list — these bounds are the CONSTRAINT
 * your implementation must meet; every bound names its operation AND case):
 *   insert_front      O(1) worst case   (two links, fixed number of writes)
 *   insert_after(p)   O(1) worst case   (given pointer skips the walk)
 *   insert_back       O(n) worst case   (no tail handle: the walk dominates)
 *   delete_front      O(1) worst case
 *   delete_node(p)    O(1) worst case   (THE backward link's payoff)
 *   delete_back       O(n) worst case   (no tail handle: the walk dominates)
 *   search            O(n) worst / O(1) best case (unordered; prev does not help)
 *   print_forward     Theta(n)          (must visit all n)
 *   print_backward    Theta(n)          (walk to the tail, then walk back)
 *   reverse           O(n) worst case, O(1) auxiliary space
 *   free              O(n) worst case
 */

#ifndef DLIST_H
#define DLIST_H

/* ------------------------------------------------------------------ */
/* Part A: doubly linked list                                          */
/* ------------------------------------------------------------------ */

typedef struct dnode {
    int data;
    struct dnode *prev;   /* predecessor; NULL at the head */
    struct dnode *next;   /* successor;   NULL at the tail */
} DNode;

/*
 * dlist_insert_front: malloc a node holding x and splice it at the front,
 * wiring BOTH links (newNode->next = *head FIRST, then fix the old head's
 * prev, then swing *head). Return the new node.
 *   - return NULL and change nothing when head == NULL or malloc fails.
 *   - O(1) worst case.
 */
DNode *dlist_insert_front(DNode **head, int x);

/*
 * dlist_insert_back: malloc a node holding x and append it at the back (walk
 * to the last node; an empty list sets *head directly). Return the new node.
 *   - return NULL and change nothing when head == NULL or malloc fails.
 *   - O(n) worst case: no tail handle, so the walk to the last node dominates.
 */
DNode *dlist_insert_back(DNode **head, int x);

/*
 * dlist_insert_after: malloc a node holding x and splice it immediately after
 * the node p (p->next becomes newNode->next; repair the old successor's prev
 * before overwriting p->next). Return the new node.
 *   - return NULL and change nothing when p == NULL or malloc fails.
 *   - the caller guarantees p is a node of the list (or NULL).
 *   - O(1) worst case: p is already in hand, so there is no walk.
 */
DNode *dlist_insert_after(DNode *p, int x);

/*
 * dlist_delete_front: unlink and free the front node; store its data in *out
 * (out may be NULL to discard).
 *   - return 0 when a node was deleted.
 *   - return -1 and change nothing (neither the list nor *out) when head ==
 *     NULL or the list is empty.
 *   - O(1) worst case.
 */
int dlist_delete_front(DNode **head, int *out);

/*
 * dlist_delete_back: unlink and free the last node; store its data in *out
 * (out may be NULL to discard).
 *   - return 0 when a node was deleted.
 *   - return -1 and change nothing (neither the list nor *out) when head ==
 *     NULL or the list is empty.
 *   - O(n) worst case: no tail handle, so the walk to the last node dominates.
 */
int dlist_delete_back(DNode **head, int *out);

/*
 * dlist_delete_node: unlink and free exactly the node target, given only a
 * pointer to it — the O(1) delete the backward link exists for. Bypass:
 * target->prev->next = target->next (or move *head when target is first);
 * target->next->prev = target->prev; then free(target) exactly once.
 *   - return 0 when the node was deleted.
 *   - return -1 and change nothing when head == NULL, target == NULL, the
 *     list is empty, or target is not the current front while target->prev is
 *     NULL (a target the caller has already unlinked).
 *   - the caller guarantees target is a live node of the list.
 *   - O(1) worst case.
 */
int dlist_delete_node(DNode **head, DNode *target);

/*
 * dlist_search: walk p = head while (p != NULL && p->data != x); return the
 * first node holding x, or NULL when absent (a miss walks the whole chain).
 *   - O(n) worst case, O(1) best case. Never modifies the list.
 */
DNode *dlist_search(DNode *head, int x);

/*
 * dlist_print_forward: copy the items head-to-tail into out[0..n-1] and
 * return the number written. (The "print/display" operation made testable:
 * instead of writing to stdout, the caller supplies the buffer — the same
 * convention as Week 5's cqueue_display and Week 6's slist_display.)
 *   - an empty list writes nothing and returns 0 (out may be NULL then).
 *   - a non-empty list with out == NULL, out_cap < 0, or out_cap < length
 *     writes nothing and returns -1 (retry with room for the full list).
 *   - never disturbs the list. Theta(n).
 */
int dlist_print_forward(const DNode *head, int *out, int out_cap);

/*
 * dlist_print_backward: copy the items tail-to-head into out[0..n-1] and
 * return the number written (the reverse of print_forward). This is where the
 * second link pays: after walking forward to the tail, the copy walks back
 * through prev.
 *   - an empty list writes nothing and returns 0 (out may be NULL then).
 *   - a non-empty list with out == NULL, out_cap < 0, or out_cap < length
 *     writes nothing and returns -1.
 *   - never disturbs the list. Theta(n).
 */
int dlist_print_backward(const DNode *head, int *out, int out_cap);

/*
 * dlist_reverse: reverse the chain in place, flipping BOTH links of every node
 * (save old prev, swap prev/next, advance through the new prev) so the
 * two-link invariant holds again on the reversed chain.
 *   - no-op when head == NULL or the list is empty or a single node.
 *   - O(n) worst case, O(1) auxiliary space.
 */
void dlist_reverse(DNode **head);

/*
 * dlist_free: free every node and set *head to NULL (a second call is a safe
 * no-op). No-op when head == NULL or the list is already empty.
 *   - O(n) worst case.
 */
void dlist_free(DNode **head);

/* ------------------------------------------------------------------ */
/* Part B: sparse polynomials (the week's application)                 */
/* ------------------------------------------------------------------ */

/*
 * A polynomial sum_i c_i x^{e_i} is stored as a chain of pnode terms kept in
 * STRICTLY DESCENDING exponent order (the course convention, Week 7 Section
 * 4). Terms whose coefficient is 0 are NEVER stored — that is the sparsity
 * payoff. The zero polynomial is head == NULL.
 *
 * Representation choice (documented for the grader): the polynomial chain is
 * SINGLY linked (next only) with a cached tail, not a doubly linked chain.
 * The merge only ever moves forward, so a prev link would add one pointer per
 * term for no operation this assignment performs; the cached tail is the
 * "tail where appropriate" from Week 7 — it makes every append in the merge
 * O(1), so poly_add is linear. (Compare the list-backed queue in lecture,
 * where tail made enqueue O(1).)
 */

typedef struct pnode {
    int coeff;                 /* nonzero coefficient (zero terms are not stored) */
    int exp;                   /* exponent; terms are in strictly descending order */
    struct pnode *next;
} PNode;

struct poly {
    struct pnode *head;        /* NULL when this is the zero polynomial */
    struct pnode *tail;        /* last term (O(1) append); NULL when empty */
};

/*
 * poly_init: set p to the zero polynomial (head = tail = NULL). Call once
 * before building a polynomial. No-op when p == NULL.
 */
void poly_init(struct poly *p);

/*
 * poly_append_term: append the term (coeff, exp) at the tail. The caller
 * guarantees terms are appended in strictly DESCENDING exponent order.
 *   - return 0 when the term was stored, or when coeff == 0 (a zero term is
 *     skipped by design — sparsity discipline).
 *   - return -1 and change nothing when p == NULL, malloc fails, or exp is
 *     not strictly less than the current tail's exponent (order violation).
 *   - O(1) worst case (the cached tail skips the walk).
 */
int poly_append_term(struct poly *p, int coeff, int exp);

/*
 * poly_free: free every term and reset p to the zero polynomial (a second
 * call is a safe no-op). No-op when p == NULL.
 */
void poly_free(struct poly *p);

/*
 * poly_add: add the polynomials a and b, writing the sum into out. A single
 * linear merge of the two descending-exponent chains: at each step copy the
 * larger exponent through, add the coefficients on an equal exponent, and
 * suppress a term whose coefficient sums to 0. The output is built in
 * descending exponent order with O(1) tail appends.
 *   - a and b are unchanged (inputs are read-only).
 *   - out must be the zero polynomial on entry (head == NULL), and out must
 *     not alias a or b.
 *   - *out receives a freshly allocated sum the caller owns (free it with
 *     poly_free). An all-cancelling sum leaves out as the zero polynomial
 *     (head == NULL), not an error.
 *   - return 0 on success.
 *   - return -1 and leave *out as the zero polynomial when any argument is
 *     NULL, out is not empty, out aliases an input, or malloc fails (partial
 *     work is freed, so no leak).
 *   - O(n + m) worst case for n and m terms in a and b.
 */
int poly_add(const struct poly *a, const struct poly *b, struct poly *out);

#endif /* DLIST_H */
