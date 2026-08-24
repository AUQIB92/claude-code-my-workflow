/*
 * test_visible.c — the visible tests, one group per worked example in the
 * assignment statement. Run locally to sanity-check your analysis.c before
 * submitting; the autograder runs a LARGER hidden suite on top of these.
 *
 * Build + run (from the assignment directory):
 *   gcc -Wall -Wextra -o test_visible test_visible.c analysis.c
 *   ./test_visible
 */

#include <stdio.h>
#include "analysis.h"

static int failures = 0;

static void check(const char *name, int got, int want)
{
    if (got == want) {
        printf("  PASS  %s\n", name);
    } else {
        printf("  FAIL  %s (got %d, want %d)\n", name, got, want);
        failures++;
    }
}

int main(void)
{
    /* Example 1: linear_search on an unsorted inventory-code array. */
    {
        int A[] = {42, 17, 99, 3, 56};
        int n = 5;
        printf("Example 1: linear_search (unsorted)\n");
        check("linear_search(A,5,3) == 3",  linear_search(A, n, 3),  3);
        check("linear_search(A,5,42) == 0", linear_search(A, n, 42), 0);
        check("linear_search(A,5,7) == -1", linear_search(A, n, 7), -1);
    }

    /* Example 2: binary_search on a sorted array. */
    {
        int A[] = {2, 9, 14, 23, 31, 40, 58};
        int n = 7;
        printf("Example 2: binary_search (sorted)\n");
        check("binary_search(A,7,23) == 3", binary_search(A, n, 23), 3);
        check("binary_search(A,7,2) == 0",  binary_search(A, n, 2),  0);
        check("binary_search(A,7,58) == 6", binary_search(A, n, 58), 6);
        check("binary_search(A,7,15) == -1", binary_search(A, n, 15), -1);
    }

    /* Example 3: has_duplicate. */
    {
        int A1[] = {5, 8, 1, 8, 3};
        int A2[] = {5, 8, 1, 3};
        printf("Example 3: has_duplicate\n");
        check("has_duplicate([5,8,1,8,3]) == 1", has_duplicate(A1, 5), 1);
        check("has_duplicate([5,8,1,3]) == 0",   has_duplicate(A2, 4), 0);
    }

    if (failures == 0) {
        printf("\nAll visible tests passed.\n");
        return 0;
    }
    printf("\n%d visible test(s) FAILED.\n", failures);
    return 1;
}
