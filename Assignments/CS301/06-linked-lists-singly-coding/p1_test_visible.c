/*
 * p1_test_visible.c -- visible P1 tests (the assignment's worked examples).
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

static void checkInt(const char *name, int got, int want)
{
    checks++;
    if (got == want) {
        printf("  PASS  %s\n", name);
    } else {
        printf("  FAIL  %s (got %d, want %d)\n", name, got, want);
        failures++;
    }
}

int main(void)
{
    /* V1: delete middle (pos 1) of 7 -> 13 -> 19 -> 27 */
    {
        const int in[] = { 7, 13, 19, 27 };
        const int want[] = { 7, 19, 27 };
        struct node *h = buildList(in, 4);
        checkInt("V1 rc", deleteAtPosition(&h, 1), 0);
        checkList("V1 list", h, want, 3);
        freeList(h);
    }
    /* V2: delete head (pos 0) of 7 -> 13 -> 19 -> 27 */
    {
        const int in[] = { 7, 13, 19, 27 };
        const int want[] = { 13, 19, 27 };
        struct node *h = buildList(in, 4);
        checkInt("V2 rc", deleteAtPosition(&h, 0), 0);
        checkList("V2 list", h, want, 3);
        freeList(h);
    }
    /* V3: delete tail (pos 3) of 7 -> 13 -> 19 -> 27 */
    {
        const int in[] = { 7, 13, 19, 27 };
        const int want[] = { 7, 13, 19 };
        struct node *h = buildList(in, 4);
        checkInt("V3 rc", deleteAtPosition(&h, 3), 0);
        checkList("V3 list", h, want, 3);
        freeList(h);
    }
    /* V4: out of range (pos 4) leaves 7 -> 13 -> 19 -> 27 unchanged */
    {
        const int in[] = { 7, 13, 19, 27 };
        struct node *h = buildList(in, 4);
        checkInt("V4 rc", deleteAtPosition(&h, 4), -1);
        checkList("V4 list", h, in, 4);
        freeList(h);
    }
    /* V5: singleton delete (pos 0) empties the list */
    {
        const int in[] = { 42 };
        struct node *h = buildList(in, 1);
        checkInt("V5 rc", deleteAtPosition(&h, 0), 0);
        checkInt("V5 empty", h == NULL, 1);
        freeList(h);
    }

    printf("%d checks, %d failures\n", checks, failures);
    return failures ? 1 : 0;
}
