/*
 * timing_harness.c — Part 2 of Week 2's assignment: the empirical timing
 * experiment (syllabus Week 2 lab: "Empirical timing vs. predicted
 * growth"). PROVIDED to you — you do not write or submit this file, you
 * only compile and run it against your own analysis.c.
 *
 * What it does: times each of the three functions from analysis.h at
 * geometrically increasing input sizes, in each function's WORST CASE
 * (the case the lecture derived a bound for), and prints one table per
 * function. You then transcribe the printed tables into timing_report.md
 * (see the assignment PDF, Part 2) and answer the three short questions
 * there — that write-up is graded by the instructor, not by this
 * program or the autograder.
 *
 * Worst-case inputs used here, matching the lecture's own derivations:
 *   - linear_search: key ABSENT from the array -> every element checked.
 *   - binary_search:  key ABSENT from a SORTED array -> full log2(n) passes.
 *   - has_duplicate:  a strictly increasing (no-duplicate) array -> every
 *                      pair is compared, since no early return is possible.
 *
 * Build (from the assignment directory, against YOUR analysis.c):
 *   gcc -O2 -Wall -Wextra -o timing_harness timing_harness.c analysis.c
 *   ./timing_harness
 *
 * -O2 matters here: at -O0 constant-factor overhead can swamp the signal
 * you are trying to measure. Do not compare -O0 numbers to the lecture's
 * asymptotic predictions.
 *
 * Each measurement repeats the call some number of times and reports the
 * average — a single call is often faster than the system clock's own
 * tick resolution, especially for binary_search's O(log n) work. The
 * repeat count is tuned per function/size (see LS_REPS, BS_REPS, and the
 * nsq_reps table below) so the total run finishes in a few seconds.
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "analysis.h"

#define LS_REPS 200        /* linear_search: O(n) work per call dominates quickly */
#define BS_REPS 2000000    /* binary_search: O(log n) work per call is tiny --
                               needs far more repetitions to clear clock()'s
                               ~1ms tick resolution on some platforms */

static double time_linear_search(int n)
{
    int *A = (int *)malloc(sizeof(int) * (size_t)n);
    int i;
    clock_t start, end;
    for (i = 0; i < n; i++) A[i] = i;      /* 0..n-1, key below will be absent */
    start = clock();
    for (i = 0; i < LS_REPS; i++) {
        volatile int r = linear_search(A, n, -1);   /* -1 never present */
        (void)r;
    }
    end = clock();
    free(A);
    return (double)(end - start) / CLOCKS_PER_SEC / LS_REPS * 1000.0;  /* ms/call */
}

static double time_binary_search(int n)
{
    int *A = (int *)malloc(sizeof(int) * (size_t)n);
    int i;
    clock_t start, end;
    for (i = 0; i < n; i++) A[i] = i;      /* sorted ascending, key below absent */
    start = clock();
    for (i = 0; i < BS_REPS; i++) {
        volatile int r = binary_search(A, n, -1);
        (void)r;
    }
    end = clock();
    free(A);
    return (double)(end - start) / CLOCKS_PER_SEC / BS_REPS * 1000.0;
}

static double time_has_duplicate(int n, int reps)
{
    int *A = (int *)malloc(sizeof(int) * (size_t)n);
    int i;
    clock_t start, end;
    for (i = 0; i < n; i++) A[i] = i;      /* strictly increasing: no duplicate */
    start = clock();
    for (i = 0; i < reps; i++) {
        volatile int r = has_duplicate(A, n);
        (void)r;
    }
    end = clock();
    free(A);
    return (double)(end - start) / CLOCKS_PER_SEC / reps * 1000.0;
}

int main(void)
{
    int i;
    int on_sizes[]  = {100000, 200000, 400000, 800000, 1600000, 3200000};
    int nsq_sizes[] = {500, 1000, 2000, 4000, 8000, 16000};
    /* more reps at small n, where a single O(n^2) call is too fast to
       register on clock()'s tick resolution; fewer reps as n grows and
       a single call is already slow enough to measure on its own. */
    int nsq_reps[]  = {200, 50, 20, 5, 2, 1};

    printf("=== linear_search — worst case (key absent), predicted O(n) ===\n");
    printf("%12s %14s\n", "n", "ms/call");
    for (i = 0; i < (int)(sizeof(on_sizes) / sizeof(on_sizes[0])); i++) {
        printf("%12d %14.5f\n", on_sizes[i], time_linear_search(on_sizes[i]));
    }

    printf("\n=== binary_search — worst case (key absent), predicted O(log n) ===\n");
    printf("%12s %14s\n", "n", "ms/call");
    for (i = 0; i < (int)(sizeof(on_sizes) / sizeof(on_sizes[0])); i++) {
        printf("%12d %14.5f\n", on_sizes[i], time_binary_search(on_sizes[i]));
    }

    printf("\n=== has_duplicate — worst case (no duplicate present), predicted O(n^2) ===\n");
    printf("%12s %14s\n", "n", "ms/call");
    for (i = 0; i < (int)(sizeof(nsq_sizes) / sizeof(nsq_sizes[0])); i++) {
        printf("%12d %14.5f\n", nsq_sizes[i],
               time_has_duplicate(nsq_sizes[i], nsq_reps[i]));
    }

    printf("\nDone. Copy these three tables into timing_report.md and answer\n");
    printf("the three questions in Part 2 of the assignment.\n");
    return 0;
}
