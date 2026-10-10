/*
 * p2_test_visible.c -- the worked examples from the problem statement.
 * Shown to students; run this locally before submitting.
 */

#include <stdio.h>
#include "p2_postfix.h"

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
    printf("P2 visible tests: eval_postfix\n");

    check("worked ex. 1: 12 2 3 * -",  eval_postfix("12 2 3 * -"), 6);
    check("worked ex. 2: 9 3 / 2 +",   eval_postfix("9 3 / 2 +"), 5);
    check("worked ex. 3: single operand", eval_postfix("42"), 42);
    check("worked ex. 4: 100 25 / 4 *", eval_postfix("100 25 / 4 *"), 16);

    printf("\n%d checks, %d failures.\n", checks, failures);
    return failures == 0 ? 0 : 1;
}
