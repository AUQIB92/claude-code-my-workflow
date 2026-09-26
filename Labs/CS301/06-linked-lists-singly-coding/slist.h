/*
 * slist.h — the Singly-Linked-List ADT contract for Week 6 (CS301):
 * singly-linked-list operations (instructor-supplied lab, no P-number).
 *
 * The contract says WHAT each function must do, not HOW the chain is laid
 * out. This header is given to you; do not change it. Your job is to provide
 * every function below in slist.c (start from starter_slist.c).
 *
 * Representation (deck: Week 6, Sections 1 and 3):
 *
 *   struct SNode { int data; struct SNode *next; };
 *
 * `head` is the ONLY entry point (NULL when empty); the last node's `next`
 * is NULL. Nodes live anywhere in the heap — order lives in the links,
 * never in the layout. Every node is separately malloc'd; every malloc
 * needs a matching free (slist_free, or slist_delete_value per node).
 *
 * Memory discipline (graded per the syllabus lab rubric):
 *   - check every malloc for NULL before dereferencing;
 *   - free exactly once per node; never touch a node after freeing it;
 *   - slist_free sets *head to NULL so a second free is a safe no-op.
 *
 * Complexity (deck Section 4 price list — these bounds are the CONSTRAINT
 * your implementation must meet):
 *   insert_front O(1) worst case; insert_end / insert_at / delete_value /
 *   search O(n) worst case in the current length (the walk dominates; the
 *   splice/bypass itself is O(1)); search O(1) best case (head holds x);
 *   display Theta(n); reverse O(n) worst case in O(1) auxiliary space;
 *   length O(n) worst case (it walks); free O(n) worst case.
 */

#ifndef SLIST_H
#define SLIST_H

#include <stddef.h> /* size_t */

typedef struct SNode {
    int data;
    struct SNode *next;
} SNode;

/*
 * slist_insert_front: malloc a node holding x, splice it at the front with
 * the deck's two-write order (newNode->next = *head FIRST, then
 * *head = newNode), and return the new node.
 *   - return NULL and change nothing when head == NULL or malloc fails.
 */
SNode *slist_insert_front(SNode **head, int x);

/*
 * slist_insert_end: append a node holding x at the end (walk to the last
 * node; empty list sets *head directly). Return the new node.
 *   - return NULL and change nothing when head == NULL or malloc fails.
 *   - O(n) worst case without a tail pointer (the walk dominates).
 */
SNode *slist_insert_end(SNode **head, int x);

/*
 * slist_insert_at: insert x at 0-based position pos (pos == 0 is the front,
 * pos == length appends at the end). Walk p from *head to the predecessor,
 * then splice with the deck's two-write order.
 *   - return 0 on success.
 *   - return -1 and change nothing when head == NULL, pos > length
 *     (walking past NULL is a bug, not an edge case), or malloc fails.
 */
int slist_insert_at(SNode **head, size_t pos, int x);

/*
 * slist_delete_value: delete the FIRST node whose data == x (head first,
 * then the predecessor walk). Bypass with one link rewrite
 * (p->next = temp->next, or *head = temp->next at the head), free exactly
 * once, never touch temp afterwards.
 *   - return 0 when a node was deleted.
 *   - return -1 and change nothing when head == NULL, the list is empty,
 *     or x is absent. Only the first occurrence goes; later duplicates stay.
 */
int slist_delete_value(SNode **head, int x);

/*
 * slist_search: walk p = head while (p != NULL && p->data != x); return the
 * first node holding x, or NULL when absent (a miss walks everything).
 * O(n) worst case, O(1) best case. Never modifies the list.
 */
SNode *slist_search(SNode *head, int x);

/*
 * slist_length: count the nodes by walking. O(n) worst case.
 */
size_t slist_length(const SNode *head);

/*
 * slist_display: copy the live items head-to-NULL into out[0..len-1] (the
 * "display" operation, made testable: instead of printing, the caller
 * supplies the buffer). Return the number of items written.
 *   - an empty list writes nothing and returns 0 (out may be NULL then).
 *   - a non-empty list with out == NULL or out_cap < length writes nothing
 *     and returns -1 (the caller must retry with room for at least
 *     slist_length(head) ints).
 * Never disturbs the list: head and every link are unchanged afterwards.
 */
int slist_display(const SNode *head, int *out, int out_cap);

/*
 * slist_reverse: reverse the chain in place with the deck's three-pointer
 * loop (prev = NULL; curr = *head; save next, flip, advance both walkers;
 * *head = prev). O(n) worst case, O(1) auxiliary space.
 *   - no-op when head == NULL, the list is empty, or it holds one node.
 */
void slist_reverse(SNode **head);

/*
 * slist_free: free every node and set *head to NULL (a second call is a
 * safe no-op). No-op when head == NULL or the list is already empty.
 */
void slist_free(SNode **head);

#endif /* SLIST_H */
