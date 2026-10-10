/*
 * p1_test_visible.c -- the worked examples from the problem statement.
 * Shown to students; run this locally before submitting.
 */

#include <stdio.h>
#include "p1_bracket.h"

static int failures = 0;
static int checks = 0;

static void check(const char *name, int got, int want)
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
    printf("P1 visible tests: is_balanced\n");

    check("worked ex. 1: {[(a+b)*c]-d}", is_balanced("{[(a+b)*c]-d}"), 1);
    check("worked ex. 2: ([a+b)]",       is_balanced("([a+b)]"), 0);
    check("worked ex. 3: ((a+b]",        is_balanced("((a+b]"), 0);
    check("worked ex. 4: empty string",  is_balanced(""), 1);
    check("worked ex. 5: no brackets",   is_balanced("a+b*c"), 1);

    printf("\n%d checks, %d failures.\n", checks, failures);
    return failures == 0 ? 0 : 1;
}
