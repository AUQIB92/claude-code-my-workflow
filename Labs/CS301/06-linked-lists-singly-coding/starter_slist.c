/*
 * starter_slist.c — starter stub for Week 6's singly-linked-list lab.
 *
 * Copy to slist.c and fill in every function body. Do not modify slist.h.
 * Every function below is a TODO: replace the placeholder body with the
 * deck's algorithm (Week 6, Sections 3-4), keeping the contract in slist.h.
 *
 * Build + sanity-check (from this directory):
 *   gcc -std=c11 -Wall -Wextra -o test_visible test_visible.c slist.c
 *   ./test_visible
 */

#include <stddef.h>
#include <stdlib.h>
#include "slist.h"

SNode *slist_insert_front(SNode **head, int x)
{
    (void)head;
    (void)x;
    return NULL; /* TODO: malloc, fill, two-write splice, swing head */
}

SNode *slist_insert_end(SNode **head, int x)
{
    (void)head;
    (void)x;
    return NULL; /* TODO: empty list sets *head; else walk then append */
}

int slist_insert_at(SNode **head, size_t pos, int x)
{
    (void)head;
    (void)pos;
    (void)x;
    return -1; /* TODO: pos==0 is front; else walk to predecessor, splice */
}

int slist_delete_value(SNode **head, int x)
{
    (void)head;
    (void)x;
    return -1; /* TODO: head case, else predecessor walk, bypass, free once */
}

SNode *slist_search(SNode *head, int x)
{
    (void)head;
    (void)x;
    return NULL; /* TODO: one loop over p = p->next */
}

size_t slist_length(const SNode *head)
{
    (void)head;
    return 0; /* TODO: count the walk */
}

int slist_display(const SNode *head, int *out, int out_cap)
{
    (void)head;
    (void)out;
    (void)out_cap;
    return -1; /* TODO: empty -> 0; else validate buffer, copy, count */
}

void slist_reverse(SNode **head)
{
    (void)head;
    /* TODO: prev=NULL, curr=*head; save next, flip, advance; *head=prev */
}

void slist_free(SNode **head)
{
    (void)head;
    /* TODO: walk with a saved next, free each node, *head = NULL */
}
