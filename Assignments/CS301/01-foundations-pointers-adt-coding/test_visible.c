/*
 * test_visible.c — the visible tests, one per worked example in the
 * assignment statement. Run locally to sanity-check your bag.c before
 * submitting; the autograder runs a LARGER hidden suite on top of these.
 *
 * Build + run (from the assignment directory):
 *   gcc -Wall -Wextra -o test_visible test_visible.c bag.c
 *   ./test_visible
 */

#include <stdio.h>
#include "bag.h"

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
    Node *bag = NULL;

    printf("Example 1: the empty bag\n");
    check("size() == 0", bag_size(bag), 0);
    check("member(7) == 0", bag_member(bag, 7), 0);

    printf("Example 2: insert three values\n");
    bag = bag_insert(bag, 3);
    bag = bag_insert(bag, 5);
    bag = bag_insert(bag, 7);
    check("size() == 3", bag_size(bag), 3);
    check("member(3) == 1", bag_member(bag, 3), 1);
    check("member(5) == 1", bag_member(bag, 5), 1);
    check("member(7) == 1", bag_member(bag, 7), 1);
    check("member(9) == 0", bag_member(bag, 9), 0);

    printf("Example 3: free and rebuild\n");
    free_bag(bag);
    bag = NULL;
    check("size() == 0 after free", bag_size(bag), 0);
    bag = bag_insert(bag, 42);
    check("member(42) == 1", bag_member(bag, 42), 1);
    check("size() == 1", bag_size(bag), 1);
    free_bag(bag);

    if (failures == 0) {
        printf("\nAll visible tests passed.\n");
        return 0;
    }
    printf("\n%d visible test(s) FAILED.\n", failures);
    return 1;
}
