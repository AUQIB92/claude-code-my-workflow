/*
 * p2_reference_solution.c -- INSTRUCTOR-ONLY reference for P2.
 * NEVER ship to students; NEVER sync to docs/.
 */
#include <stdlib.h>
#include "sll.h"

struct node *mergeSorted(struct node *a, struct node *b)
{
    struct node dummy;
    struct node *tail = &dummy;

    dummy.next = NULL;
    while (a != NULL && b != NULL) {
        if (a->data <= b->data) {
            tail->next = a;
            a = a->next;
        } else {
            tail->next = b;
            b = b->next;
        }
        tail = tail->next;
    }
    tail->next = (a != NULL) ? a : b;
    return dummy.next;
}
