/*
 * p1_test_hidden.c -- the autograder's hidden test suite for P1
 * (deleteAtPosition). NEVER ship to students. Covers the adversarial
 * bar from algorithm-verification.md: the worked examples re-checked,
 * boundary sizes (empty, singleton, negative pos), structure-specific
 * cases (head/tail/out-of-range/drain-to-empty/duplicates/long list),
 * and >=20 random inputs checked against an independent hand-written
 * oracle (flagged below -- array-index model with different control
 * flow from the reference's pointer walk, so a bug in one is unlikely
 * to be mirrored in the other).
 */

#include <stdio.h>
#include <stdlib.h>
#include "sll.h"

static int failures = 0;
static int checks = 0;

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

static void checkList(const char *name, struct node *head,
                      const int *want, int wantN)
{
    int got[512];
    int gotN = listToArray(head, got, 512);
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
        printf("  FAIL  %s (gotN %d, wantN %d)\n", name, gotN, wantN);
        failures++;
    }
}

/*
 * oracle_delete: independent hand-written oracle on a plain int array.
 * Returns 0 on success (element removed by shifting the TAIL DOWN with
 * a low-to-high loop, opposite traversal direction from the
 * reference's head-to-predecessor pointer walk) or -1 leaving the
 * array untouched.
 * Flagged as hand-written per the oracle policy.
 */
static int oracle_delete(int *arr, int *n, int pos)
{
    int i;
    if (pos < 0 || pos >= *n) {
        return -1;
    }
    for (i = pos + 1; i < *n; i++) {
        arr[i - 1] = arr[i]; /* shift down, low-to-high so no clobber */
    }
    /* NOTE: element at pos is overwritten by arr[pos+1] shifting down. */
    (*n)--;
    return 0;
}

static unsigned rng_state = 0xC501ULL;
static unsigned nextRand(unsigned m)
{
    rng_state = rng_state * 1103515245u + 12345u;
    return (unsigned)(((rng_state >> 16) % m));
}

int main(void)
{
    /* H1: worked examples re-checked on fresh data (not the visible lists) */
    {
        const int in[] = { 11, 23, 31, 47 };
        const int w1[] = { 11, 31, 47 };
        const int w0[] = { 23, 31, 47 };
        const int w3[] = { 11, 23, 31 };
        struct node *h;
        h = buildList(in, 4);
        checkInt("H1 mid rc", deleteAtPosition(&h, 1), 0);
        checkList("H1 mid list", h, w1, 3);
        freeList(h);
        h = buildList(in, 4);
        checkInt("H1 head rc", deleteAtPosition(&h, 0), 0);
        checkList("H1 head list", h, w0, 3);
        freeList(h);
        h = buildList(in, 4);
        checkInt("H1 tail rc", deleteAtPosition(&h, 3), 0);
        checkList("H1 tail list", h, w3, 3);
        freeList(h);
        h = buildList(in, 4);
        checkInt("H1 oor rc", deleteAtPosition(&h, 4), -1);
        checkList("H1 oor list", h, in, 4);
        freeList(h);
    }
    /* H2: empty list */
    {
        struct node *h = NULL;
        checkInt("H2 empty pos0", deleteAtPosition(&h, 0), -1);
        checkInt("H2 empty stays NULL", h == NULL, 1);
        checkInt("H2 empty pos5", deleteAtPosition(&h, 5), -1);
        checkInt("H2 empty neg", deleteAtPosition(&h, -1), -1);
    }
    /* H3: singleton */
    {
        const int one[] = { 99 };
        struct node *h;
        h = buildList(one, 1);
        checkInt("H3 singleton pos0", deleteAtPosition(&h, 0), 0);
        checkInt("H3 now empty", h == NULL, 1);
        freeList(h);
        h = buildList(one, 1);
        checkInt("H3 singleton pos1", deleteAtPosition(&h, 1), -1);
        checkList("H3 unchanged", h, one, 1);
        freeList(h);
        h = buildList(one, 1);
        checkInt("H3 singleton neg", deleteAtPosition(&h, -2), -1);
        checkList("H3 unchanged2", h, one, 1);
        freeList(h);
    }
    /* H4: negative / huge pos on a longer list */
    {
        const int in[] = { 7, 13, 19, 27, 36 };
        struct node *h;
        h = buildList(in, 5);
        checkInt("H4 neg", deleteAtPosition(&h, -1), -1);
        checkList("H4 neg unchanged", h, in, 5);
        freeList(h);
        h = buildList(in, 5);
        checkInt("H4 pos==len", deleteAtPosition(&h, 5), -1);
        checkList("H4 len unchanged", h, in, 5);
        freeList(h);
        h = buildList(in, 5);
        checkInt("H4 huge", deleteAtPosition(&h, 1000000), -1);
        checkList("H4 huge unchanged", h, in, 5);
        freeList(h);
    }
    /* H5: drain a 3-list to empty one head-delete at a time */
    {
        const int in[] = { 8, 16, 24 };
        const int w1[] = { 16, 24 };
        const int w2[] = { 24 };
        struct node *h = buildList(in, 3);
        checkInt("H5 d1", deleteAtPosition(&h, 0), 0);
        checkList("H5 l1", h, w1, 2);
        checkInt("H5 d2", deleteAtPosition(&h, 0), 0);
        checkList("H5 l2", h, w2, 1);
        checkInt("H5 d3", deleteAtPosition(&h, 0), 0);
        checkInt("H5 empty", h == NULL, 1);
        checkInt("H5 d4 fails", deleteAtPosition(&h, 0), -1);
        freeList(h);
    }
    /* H6: duplicates -- exactly one copy removed */
    {
        const int in[] = { 5, 5, 5, 5 };
        const int want[] = { 5, 5, 5 };
        struct node *h = buildList(in, 4);
        checkInt("H6 dup rc", deleteAtPosition(&h, 1), 0);
        checkList("H6 dup list", h, want, 3);
        checkInt("H6 len", listLength(h), 3);
        freeList(h);
    }
    /* H7: two-element head and tail */
    {
        const int in[] = { 61, 73 };
        const int wh[] = { 73 };
        const int wt[] = { 61 };
        struct node *h;
        h = buildList(in, 2);
        checkInt("H7 two head", deleteAtPosition(&h, 0), 0);
        checkList("H7 two head list", h, wh, 1);
        freeList(h);
        h = buildList(in, 2);
        checkInt("H7 two tail", deleteAtPosition(&h, 1), 0);
        checkList("H7 two tail list", h, wt, 1);
        freeList(h);
    }
    /* H8: long list (100 elems): head / middle / tail / out-of-range */
    {
        int in[100];
        int i;
        struct node *h;
        for (i = 0; i < 100; i++) {
            in[i] = i * 3 + 1;
        }
        h = buildList(in, 100);
        checkInt("H8 long mid", deleteAtPosition(&h, 50), 0);
        checkInt("H8 long len", listLength(h), 99);
        freeList(h);
        h = buildList(in, 100);
        checkInt("H8 long head", deleteAtPosition(&h, 0), 0);
        checkInt("H8 long head val", h->data, in[1]);
        freeList(h);
        h = buildList(in, 100);
        checkInt("H8 long tail", deleteAtPosition(&h, 99), 0);
        checkInt("H8 long tail len", listLength(h), 99);
        freeList(h);
        h = buildList(in, 100);
        checkInt("H8 long oor", deleteAtPosition(&h, 100), -1);
        checkInt("H8 long oor len", listLength(h), 100);
        freeList(h);
    }
    /* H9: random lists vs array oracle (>=20 inputs) */
    {
        int t;
        for (t = 0; t < 25; t++) {
            int n = (int)nextRand(13); /* 0..12 */
            int arr[16];
            int expect[16];
            int en = n;
            int pos;
            int wantRc;
            int i;
            struct node *h;
            char nm[48];
            for (i = 0; i < n; i++) {
                arr[i] = (int)nextRand(7); /* small: forces duplicates */
                expect[i] = arr[i];
            }
            /* pos in [-2, n+1] */
            pos = (int)nextRand((unsigned)(n + 4)) - 2;
            wantRc = oracle_delete(expect, &en, pos);
            h = buildList(arr, n);
            sprintf(nm, "H9 rand%d rc (n=%d,pos=%d)", t, n, pos);
            checkInt(nm, deleteAtPosition(&h, pos), wantRc);
            sprintf(nm, "H9 rand%d list", t);
            checkList(nm, h, expect, en);
            freeList(h);
        }
    }

    printf("%d checks, %d failures\n", checks, failures);
    return failures ? 1 : 0;
}
