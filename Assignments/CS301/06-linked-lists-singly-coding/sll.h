/*
 * sll.h -- the contract for Coding Assignment 6 (Singly Linked Lists),
 * Week 6's institute practical: singly-linked-list operations.
 *
 * This header is given to you; do not change it. Your job is to provide
 * the two functions below (start from p1_starter.c / p2_starter.c).
 *
 * Node type and discipline are exactly the lecture's
 * (Slides/CS301/06-linked-lists-singly.tex): `head` is the list handle,
 * `p->next` is the successor link, NULL terminates the chain.
 */

#ifndef SLL_H
#define SLL_H

#include <stddef.h> /* NULL */

struct node {
    int data;
    struct node *next;
};

/*
 * deleteAtPosition: remove the node at 0-based index pos.
 *   - pos == 0 removes the head (same three steps as lecture deleteHead:
 *     save, advance, free).
 *   - pos > 0 walks to the predecessor (lecture's deleteValue walk
 *     discipline), unlinks, then frees.
 *   - return 0 on success.
 *   - return -1 and change NOTHING (no unlink, no free) when the list is
 *     empty, pos is negative, or pos >= length of the list.
 *   - the freed node's memory must be released with free().
 */
int deleteAtPosition(struct node **head, int pos);

/*
 * mergeSorted: merge two ASCENDING lists a and b into one ascending list.
 *   - either (or both) input may be NULL (empty list).
 *   - REUSE the existing nodes: rewire `next` links only, allocate
 *     nothing, free nothing. After the call, every input node appears
 *     exactly once in the returned list.
 *   - return the head of the merged list (NULL only if both inputs
 *     are NULL/empty).
 *   - ties (a->data == b->data): take the node from `a` first (stable).
 *   - callers pass ownership of both input lists to mergeSorted; they
 *     must not use the old a/b heads afterwards.
 */
struct node *mergeSorted(struct node *a, struct node *b);

/* ---- helpers (implemented in sll_common.c, given to you) ---- */

/* Allocate one node holding x with next == NULL; NULL on malloc failure. */
struct node *newNode(int x);

/* Build a list from the first n entries of arr (order preserved);
   returns NULL when n == 0. */
struct node *buildList(const int *arr, int n);

/* Free every node of the list. */
void freeList(struct node *head);

/* Write up to cap list elements into out[]; return the number written. */
int listToArray(struct node *head, int *out, int cap);

/* Return the number of nodes in the list. */
int listLength(struct node *head);

#endif /* SLL_H */
