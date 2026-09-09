/*
 * test_visible.c — the visible tests, one per worked example in the
 * assignment statement. Run locally to sanity-check your stack.c before
 * submitting; the autograder runs a LARGER hidden suite on top of these.
 *
 * Build + run (from the assignment directory):
 *   gcc -Wall -Wextra -o test_visible test_visible.c stack.c
 *   ./test_visible
 */

#include <stdio.h>
#include "stack.h"

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
    /* Example 1: the stack itself (push/peek/pop + status codes). */
    {
        IntStack st;
        int v = -999;
        printf("Example 1: push/peek/pop discipline\n");
        stack_init(&st);
        check("empty after init", stack_is_empty(&st), 1);
        check("push(10) ok", stack_push(&st, 10), STACK_OK);
        check("push(20) ok", stack_push(&st, 20), STACK_OK);
        check("peek is 20", (stack_peek(&st, &v) == STACK_OK) ? v : -999, 20);
        check("size still 2 after peek", stack_size(&st), 2);
        check("pop is 20", (stack_pop(&st, &v) == STACK_OK) ? v : -999, 20);
        check("pop is 10", (stack_pop(&st, &v) == STACK_OK) ? v : -999, 10);
        check("pop on empty is UNDERFLOW", stack_pop(&st, &v), STACK_UNDERFLOW);
    }

    /* Example 2: P1 — balanced brackets. */
    printf("Example 2: is_balanced\n");
    check("empty string is balanced", is_balanced(""), 1);
    check("\"({[]})\" is balanced", is_balanced("({[]})"), 1);
    check("\"({[})\" mismatches", is_balanced("({[})"), 0);
    check("\"((())\" never closes", is_balanced("((())"), 0);

    /* Example 3: P2 — postfix evaluation. */
    {
        int ans = -999;
        printf("Example 3: eval_postfix\n");
        check("\"6 2 3 + * 4 -\" ok",
              eval_postfix("6 2 3 + * 4 -", &ans), EVAL_OK);
        check("\"6 2 3 + * 4 -\" is 26", ans, 26);
        check("\"20 4 / 3 -\" ok",
              eval_postfix("20 4 / 3 -", &ans), EVAL_OK);
        check("\"20 4 / 3 -\" is 2", ans, 2);
        check("\"5 0 /\" is DIV_BY_ZERO",
              eval_postfix("5 0 /", &ans), EVAL_DIV_BY_ZERO);
        check("\"2 +\" is TOO_FEW_OPERANDS",
              eval_postfix("2 +", &ans), EVAL_TOO_FEW_OPERANDS);
    }

    if (failures == 0) {
        printf("\nAll visible tests passed.\n");
        return 0;
    }
    printf("\n%d visible test(s) FAILED.\n", failures);
    return 1;
}
