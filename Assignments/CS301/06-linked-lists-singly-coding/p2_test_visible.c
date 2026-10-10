/*
 * p2_test_visible.c -- visible P2 tests (the assignment's worked examples).
 * Shown to students.
 */
#include <stdio.h>
#include "sll.h"

static int failures = 0;
static int checks = 0;

static void checkList(const char *name, struct node *head,
                      const int *want, int wantN)
{
    int got[64];
    int gotN = listToArray(head, got, 64);
    int ok = (gotN == wantN);
    int i;
    for (i = 0; ok && i < wantN; i++) {
        if (got[i] != want[i]) {
            ok = 0;
        }
    }
    checks++;
    if (ok) {
        printf("  PASS  %s\n", name);
    } else {
        int j;
        printf("  FAIL  %s (got [", name);
        for (j = 0; j < gotN; j++) {
            printf("%d%s", got[j], j + 1 < gotN ? " " : "");
        }
        printf("], want [");
        for (j = 0; j < wantN; j++) {
            printf("%d%s", want[j], j + 1 < wantN ? " " : "");
        }
        printf("])\n");
        failures++;
    }
}

int main(void)
{
    /* W1: interleave [2, 8, 21] + [5, 15, 33] */
    {
        const int a[] = { 2, 8, 21 };
        const int b[] = { 5, 15, 33 };
        const int want[] = { 2, 5, 8, 15, 21, 33 };
        struct node *ha = buildList(a, 3);
        struct node *hb = buildList(b, 3);
        struct node *m = mergeSorted(ha, hb);
        checkList("W1 merge", m, want, 6);
        freeList(m);
    }
    /* W2: one side empty: [3, 11, 29] + [] */
    {
        const int a[] = { 3, 11, 29 };
        const int want[] = { 3, 11, 29 };
        struct node *ha = buildList(a, 3);
        struct node *m = mergeSorted(ha, NULL);
        checkList("W2 merge", m, want, 3);
        freeList(m);
    }
    /* W3: both empty */
    {
        struct node *m = mergeSorted(NULL, NULL);
        checks++;
        if (m == NULL) {
            printf("  PASS  W3 merge\n");
        } else {
            printf("  FAIL  W3 merge (want NULL)\n");
            failures++;
            freeList(m);
        }
    }
    /* W4: duplicates across lists [4, 9, 18] + [9, 18, 26] */
    {
        const int a[] = { 4, 9, 18 };
        const int b[] = { 9, 18, 26 };
        const int want[] = { 4, 9, 9, 18, 18, 26 };
        struct node *ha = buildList(a, 3);
        struct node *hb = buildList(b, 3);
        struct node *m = mergeSorted(ha, hb);
        checkList("W4 merge", m, want, 6);
        freeList(m);
    }

    printf("%d checks, %d failures\n", checks, failures);
    return failures ? 1 : 0;
}
