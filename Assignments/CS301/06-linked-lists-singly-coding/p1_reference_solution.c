/*
 * p1_reference_solution.c -- INSTRUCTOR-ONLY reference for P1.
 * NEVER ship to students; NEVER sync to docs/.
 */
#include <stdlib.h>
#include "sll.h"

int deleteAtPosition(struct node **head, int pos)
{
    struct node *victim;
    struct node *q;
    int i;

    if (head == NULL || *head == NULL) {
        return -1;
    }
    if (pos < 0) {
        return -1;
    }
    if (pos == 0) {
        victim = *head;
        *head = victim->next;
        free(victim);
        return 0;
    }
    q = *head;
    for (i = 0; i < pos - 1; i++) {
        if (q->next == NULL) {
            return -1;
        }
        q = q->next;
    }
    if (q->next == NULL) {
        return -1;
    }
    victim = q->next;
    q->next = victim->next;
    free(victim);
    return 0;
}
