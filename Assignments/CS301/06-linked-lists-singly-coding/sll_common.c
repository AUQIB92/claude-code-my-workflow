/*
 * sll_common.c -- helper implementations for Coding Assignment 6.
 * Given to students; do not change it. Compiled alongside every
 * submission (visible tests, hidden tests, autograder).
 */

#include <stdlib.h>
#include "sll.h"

struct node *newNode(int x)
{
    struct node *p = malloc(sizeof(struct node));
    if (p == NULL) {
        return NULL;
    }
    p->data = x;
    p->next = NULL;
    return p;
}

struct node *buildList(const int *arr, int n)
{
    struct node *head = NULL;
    struct node *tail = NULL;
    int i;

    for (i = 0; i < n; i++) {
        struct node *p = newNode(arr[i]);
        if (p == NULL) {
            freeList(head);
            return NULL;
        }
        if (head == NULL) {
            head = p;
            tail = p;
        } else {
            tail->next = p;
            tail = p;
        }
    }
    return head;
}

void freeList(struct node *head)
{
    while (head != NULL) {
        struct node *nxt = head->next;
        free(head);
        head = nxt;
    }
}

int listToArray(struct node *head, int *out, int cap)
{
    int n = 0;
    while (head != NULL && n < cap) {
        out[n] = head->data;
        n++;
        head = head->next;
    }
    return n;
}

int listLength(struct node *head)
{
    int n = 0;
    while (head != NULL) {
        n++;
        head = head->next;
    }
    return n;
}
