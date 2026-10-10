/*
 * p2_test_hidden.c -- the autograder's hidden test suite for P2
 * (mergeSorted). NEVER ship to students. Covers the adversarial bar:
 * worked examples re-checked, boundary sizes (empty/singleton/tie),
 * structure-specific cases (all-less, unequal lengths, negatives,
 * duplicates within and across, long lists, sortedness + multiset
 * conservation), and >=20 random sorted pairs checked against an
 * independent hand-written oracle (flagged below -- index-based
 * array merge with different control flow from the reference's
 * pointer-rewiring loop).
 */

#include <stdio.h>
#include <stdlib.h>
#include "sll.h"

static int failures = 0;
static int checks = 0;

static void checkList(const char *name, struct node *head,
                      const int *want, int wantN)
{
    int got[1024];
    int gotN = listToArray(head, got, 1024);
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
 * oracle_merge: independent hand-written oracle. Merges two SORTED
 * arrays with index arithmetic (i/j/k) instead of pointer rewiring,
 * and breaks ties by consuming from `a` first per the contract.
 * Flagged as hand-written per the oracle policy.
 */
static int oracle_merge(const int *a, int na, const int *b, int nb,
                        int *out)
{
    int i = 0, j = 0, k = 0;
    while (i < na && j < nb) {
        if (a[i] <= b[j]) {
            out[k++] = a[i++];
        } else {
            out[k++] = b[j++];
        }
    }
    while (i < na) {
        out[k++] = a[i++];
    }
    while (j < nb) {
        out[k++] = b[j++];
    }
    return k;
}

static int isSorted(struct node *head)
{
    while (head != NULL && head->next != NULL) {
        if (head->data > head->next->data) {
            return 0;
        }
        head = head->next;
    }
    return 1;
}

static unsigned rng_state = 0x51EDULL;
static unsigned nextRand(unsigned m)
{
    rng_state = rng_state * 1103515245u + 12345u;
    return (unsigned)(((rng_state >> 16) % m));
}

#define RUN_MERGE(tag, av, an, bv, bn) do { \
        struct node *ha_ = buildList((av), (an)); \
        struct node *hb_ = buildList((bv), (bn)); \
        struct node *m_ = mergeSorted(ha_, hb_); \
        int want_[1024]; \
        int wn_ = oracle_merge((av), (an), (bv), (bn), want_); \
        checkList((tag), m_, ((an) + (bn)) ? want_ : NULL, wn_); \
        checks++; \
        if (isSorted(m_)) { printf("  PASS  %s sorted\n", (tag)); } \
        else { printf("  FAIL  %s sorted\n", (tag)); failures++; } \
        freeList(m_); \
    } while (0)

int main(void)
{
    /* H1: worked examples re-checked on fresh data */
    {
        const int a[] = { 6, 14, 28 };
        const int b[] = { 9, 22, 41 };
        const int want[] = { 6, 9, 14, 22, 28, 41 };
        struct node *ha = buildList(a, 3);
        struct node *hb = buildList(b, 3);
        struct node *m = mergeSorted(ha, hb);
        checkList("H1 interleave", m, want, 6);
        freeList(m);
    }
    /* H2: empties */
    {
        const int a[] = { 7, 19, 35 };
        struct node *ha, *m;
        ha = buildList(a, 3);
        m = mergeSorted(ha, NULL);
        checkList("H2 b-empty", m, a, 3);
        freeList(m);
        ha = buildList(a, 3);
        m = mergeSorted(NULL, ha);
        checkList("H2 a-empty", m, a, 3);
        freeList(m);
        m = mergeSorted(NULL, NULL);
        checks++;
        if (m == NULL) {
            printf("  PASS  H2 both-empty\n");
        } else {
            printf("  FAIL  H2 both-empty\n");
            failures++;
            freeList(m);
        }
    }
    /* H3: singleton pairs incl. tie (a-first) */
    {
        const int lt_a[] = { 3 }, lt_b[] = { 17 };
        const int lt_w[] = { 3, 17 };
        const int gt_a[] = { 44 }, gt_b[] = { 12 };
        const int gt_w[] = { 12, 44 };
        const int eq_a[] = { 25 }, eq_b[] = { 25 };
        const int eq_w[] = { 25, 25 };
        struct node *m;
        m = mergeSorted(buildList(lt_a, 1), buildList(lt_b, 1));
        checkList("H3 lt", m, lt_w, 2);
        freeList(m);
        m = mergeSorted(buildList(gt_a, 1), buildList(gt_b, 1));
        checkList("H3 gt", m, gt_w, 2);
        freeList(m);
        m = mergeSorted(buildList(eq_a, 1), buildList(eq_b, 1));
        checkList("H3 tie", m, eq_w, 2);
        freeList(m);
    }
    /* H4: one side entirely smaller */
    {
        const int lo[] = { 1, 2, 3 };
        const int hi[] = { 50, 60, 70, 80 };
        const int want[] = { 1, 2, 3, 50, 60, 70, 80 };
        const int wantR[] = { 1, 2, 3, 50, 60, 70, 80 };
        struct node *m;
        m = mergeSorted(buildList(lo, 3), buildList(hi, 4));
        checkList("H4 a-all-less", m, want, 7);
        freeList(m);
        m = mergeSorted(buildList(hi, 4), buildList(lo, 3));
        checkList("H4 b-all-less", m, wantR, 7);
        freeList(m);
    }
    /* H5: duplicates within and across lists */
    {
        const int a[] = { 4, 4, 9, 18, 18 };
        const int b[] = { 4, 9, 9, 26 };
        const int want[] = { 4, 4, 4, 9, 9, 9, 18, 18, 26 };
        struct node *m = mergeSorted(buildList(a, 5), buildList(b, 4));
        checkList("H5 dups", m, want, 9);
        freeList(m);
    }
    /* H6: unequal lengths + negatives */
    {
        const int a[] = { -30, -8, 5 };
        const int b[] = { -20, -20, 0, 7, 13, 40 };
        const int want[] = { -30, -20, -20, -8, 0, 5, 7, 13, 40 };
        struct node *m = mergeSorted(buildList(a, 3), buildList(b, 6));
        checkList("H6 neg/unequal", m, want, 9);
        freeList(m);
    }
    /* H7: long lists (300 + 200), exact + sorted + length conservation */
    {
        int a[300], b[200];
        int i;
        struct node *m;
        for (i = 0; i < 300; i++) {
            a[i] = i * 2;       /* even */
        }
        for (i = 0; i < 200; i++) {
            b[i] = i * 3 + 1;   /* 1, 4, 7, ... */
        }
        RUN_MERGE("H7 long", a, 300, b, 200);
        m = NULL;
        (void)m;
    }
    /* H8: random sorted pairs vs oracle (>=20) */
    {
        int t;
        for (t = 0; t < 25; t++) {
            int na = (int)nextRand(9); /* 0..8 */
            int nb = (int)nextRand(9);
            int a[16], b[16];
            int i;
            int v = (int)nextRand(5) - 2;
            char nm[48];
            for (i = 0; i < na; i++) {
                v += (int)nextRand(4); /* non-decreasing */
                a[i] = v;
            }
            v = (int)nextRand(5) - 2;
            for (i = 0; i < nb; i++) {
                v += (int)nextRand(4);
                b[i] = v;
            }
            sprintf(nm, "H8 rand%d", t);
            RUN_MERGE(nm, a, na, b, nb);
        }
    }

    printf("%d checks, %d failures\n", checks, failures);
    return failures ? 1 : 0;
}
