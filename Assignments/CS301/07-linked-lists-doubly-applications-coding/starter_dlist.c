/*
 * starter_dlist.c — starter stub for Week 7's P7 doubly-linked-list
 * assignment (doubly linked list + sparse polynomial addition).
 *
 * Copy this file to dlist.c and fill in every function body. Do not modify
 * dlist.h. Each function below is a TODO: replace the placeholder body with
 * the deck's algorithm (Week 7, Sections 1-4), keeping the contract stated in
 * dlist.h — including the TWO-LINK INVARIANT after every insert/delete.
 *
 * Build + sanity-check (from this directory):
 *   gcc -std=c11 -Wall -Wextra -Werror -o test_visible test_visible.c dlist.c
 *   ./test_visible
 */

#include <stddef.h>
#include <stdlib.h>
#include "dlist.h"

/* ---------------- Part A: doubly linked list ---------------- */

DNode *dlist_insert_front(DNode **head, int x)
{
    (void)head;
    (void)x;
    return NULL; /* TODO: malloc, fill, wire next AND prev, swing *head */
}

DNode *dlist_insert_back(DNode **head, int x)
{
    (void)head;
    (void)x;
    return NULL; /* TODO: empty sets *head; else walk to the last node, append */
}

DNode *dlist_insert_after(DNode *p, int x)
{
    (void)p;
    (void)x;
    return NULL; /* TODO: wire newNode between p and p->next; fix old next->prev */
}

int dlist_delete_front(DNode **head, int *out)
{
    (void)head;
    (void)out;
    return -1; /* TODO: unlink the front, repair the new head's prev, free once */
}

int dlist_delete_back(DNode **head, int *out)
{
    (void)head;
    (void)out;
    return -1; /* TODO: walk to the last node, bypass via prev, free once */
}

int dlist_delete_node(DNode **head, DNode *target)
{
    (void)head;
    (void)target;
    return -1; /* TODO: O(1) bypass with target->prev/target->next, then free */
}

DNode *dlist_search(DNode *head, int x)
{
    (void)head;
    (void)x;
    return NULL; /* TODO: one loop over p = p->next */
}

int dlist_print_forward(const DNode *head, int *out, int out_cap)
{
    (void)head;
    (void)out;
    (void)out_cap;
    return -1; /* TODO: count; empty -> 0; validate buffer; copy; return count */
}

int dlist_print_backward(const DNode *head, int *out, int out_cap)
{
    (void)head;
    (void)out;
    (void)out_cap;
    return -1; /* TODO: count; walk to the tail; copy back through prev */
}

void dlist_reverse(DNode **head)
{
    (void)head;
    /* TODO: prev/curr walker swapping curr->prev and curr->next each step */
}

void dlist_free(DNode **head)
{
    (void)head;
    /* TODO: walk with a saved next, free each node, set *head = NULL */
}

/* ---------------- Part B: sparse polynomials ---------------- */

void poly_init(struct poly *p)
{
    (void)p;
    /* TODO: set p->head = NULL and p->tail = NULL */
}

int poly_append_term(struct poly *p, int coeff, int exp)
{
    (void)p;
    (void)coeff;
    (void)exp;
    return -1; /* TODO: skip coeff==0; enforce descending order; append at tail */
}

void poly_free(struct poly *p)
{
    (void)p;
    /* TODO: free the term chain, reset head and tail to NULL */
}

int poly_add(const struct poly *a, const struct poly *b, struct poly *out)
{
    (void)a;
    (void)b;
    (void)out;
    return -1; /* TODO: linear descending-exponent merge; suppress zero terms;
                  keep an output tail so each append is O(1) */
}
