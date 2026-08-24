/*
 * analysis.h — the contract for Week 2's three functions (Algorithm Analysis)
 *
 * The contract says WHAT each function must do, not HOW fast your machine
 * happens to run it. This header is given to you; do not change it. Your
 * job is to provide the three functions below in analysis.c.
 *
 * All three operate on a plain int array A[0..n-1], matching the lecture's
 * own code (linear_search, binary_search, and the nested-loop duplicate
 * check). n is always the number of elements under discussion.
 */

#ifndef ANALYSIS_H
#define ANALYSIS_H

/*
 * linear_search: scan A[0..n-1] for key, in order, starting at index 0.
 *   - basic operation (the one you should count): the comparison A[i]==key
 *   - return the index of the FIRST match, or -1 if key is not present
 *   - works on an array in ANY order (no precondition)
 *   - worst case: O(n); best case: O(1) (key at A[0])
 */
int linear_search(const int A[], int n, int key);

/*
 * binary_search: find key in A[0..n-1].
 *   - PRECONDITION: A must already be sorted in ascending order. This
 *     function does not check the precondition — calling it on an
 *     unsorted array is undefined behaviour for this assignment (this is
 *     the exact anti-pattern the lecture warned against).
 *   - basic operation: the comparison A[mid]==key
 *   - return an index i with A[i]==key, or -1 if key is absent
 *     (if key appears more than once, any matching index is acceptable)
 *   - worst case: O(log n); best case: O(1) (key at the first A[mid])
 */
int binary_search(const int A[], int n, int key);

/*
 * has_duplicate: return 1 if any value appears more than once in
 * A[0..n-1], 0 otherwise (0 and 1 arrays both count as "no duplicate").
 *   - basic operation: the comparison A[i]==A[j]
 *   - REQUIRED APPROACH: the pairwise nested-loop method from lecture —
 *     for every i, compare against every j > i, and stop the instant a
 *     match is found. Do NOT sort first and do NOT use a hash-based
 *     lookup — the point of this problem is to produce, and then
 *     empirically observe, the Theta(n^2) pattern from lecture, not to
 *     engineer around it.
 *   - worst case AND best-of-no-duplicate case: Theta(n^2) (every pair is
 *     checked whenever no duplicate exists); can return early only when a
 *     duplicate is found, so a favourable case exists only for arrays
 *     that DO contain one.
 */
int has_duplicate(const int A[], int n);

#endif /* ANALYSIS_H */
