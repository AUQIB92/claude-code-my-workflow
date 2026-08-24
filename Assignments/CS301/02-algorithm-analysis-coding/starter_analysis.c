/*
 * analysis.c — your implementation of Week 2's three functions
 *
 * Fill in the three function bodies declared in analysis.h. Do not change
 * analysis.h. Do not add any global/static mutable state.
 *
 * Compile check (from the assignment directory):
 *   gcc -Wall -Wextra -c analysis.c -o analysis.o
 *
 * Reminders from lecture:
 *   - linear_search has NO precondition on A's order.
 *   - binary_search REQUIRES A sorted ascending; it does not check this.
 *   - has_duplicate MUST use the pairwise nested-loop method, not a sort
 *     or a hash-based check (see analysis.h for why).
 */

#include "analysis.h"

int linear_search(const int A[], int n, int key)
{
    /* TODO: scan from i = 0 to n-1; return the first index where
       A[i] == key, or -1 if the loop finishes without a match. */
    (void)A; (void)n; (void)key;
    return -1;
}

int binary_search(const int A[], int n, int key)
{
    /* TODO: lo = 0, hi = n-1; while lo <= hi, compute
       mid = lo + (hi - lo) / 2, compare A[mid] to key, and narrow
       [lo, hi] to the half that could still contain key. Return the
       matching index, or -1 if the interval becomes empty. */
    (void)A; (void)n; (void)key;
    return -1;
}

int has_duplicate(const int A[], int n)
{
    /* TODO: for i = 0 to n-2, for j = i+1 to n-1, compare A[i] and A[j];
       return 1 the instant a match is found, 0 if the loops finish
       without one. */
    (void)A; (void)n;
    return 0;
}
