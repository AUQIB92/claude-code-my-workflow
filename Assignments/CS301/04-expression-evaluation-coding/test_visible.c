/*
 * test_visible.c — the visible tests, one per worked example in the
 * assignment statement. Run locally to sanity-check your expr.c before
 * submitting; the autograder runs a LARGER hidden suite on top of these.
 *
 * Build + run with MSVC (this machine, from the assignment directory):
 *   cmd /c "vcvars64.bat >NUL && cl /nologo /W4 /Fe:test_visible.exe test_visible.c expr.c"
 *   .\test_visible.exe
 * Or with gcc (lab machines):
 *   gcc -std=c11 -Wall -Wextra -o test_visible test_visible.c expr.c
 *   ./test_visible
 */

#include <stdio.h>
#include <string.h>
#include "expr.h"

static int failures = 0;

static void check_status(const char *name, int got, int want)
{
    if (got == want) {
        printf("  PASS  %s\n", name);
    } else {
        printf("  FAIL  %s (got %d, want %d)\n", name, got, want);
        failures++;
    }
}

static void check_string(const char *name, const char *got, const char *want)
{
    if (strcmp(got, want) == 0) {
        printf("  PASS  %s\n", name);
    } else {
        printf("  FAIL  %s (got \"%s\", want \"%s\")\n", name, got, want);
        failures++;
    }
}

int main(void)
{
    char buf[EXPR_MAX];

    /* Example 1: infix -> postfix (Lab P3, first half). */
    printf("Example 1: infix_to_postfix\n");
    check_status("x+y*z-w status", infix_to_postfix("x+y*z-w", buf, sizeof buf), EXPR_OK);
    check_string("x+y*z-w value", buf, "x y z * + w -");
    check_status("x^y^z+w status (right-assoc)", infix_to_postfix("x^y^z+w", buf, sizeof buf), EXPR_OK);
    check_string("x^y^z+w value", buf, "x y z ^ ^ w +");
    check_status("(x+y)*(z-w) status", infix_to_postfix("(x+y)*(z-w)", buf, sizeof buf), EXPR_OK);
    check_string("(x+y)*(z-w) value", buf, "x y + z w - *");

    /* Example 2: infix -> prefix + multi-digit operands (Lab P3). */
    printf("Example 2: infix_to_prefix + multi-digit\n");
    check_status("prefix of x+y*z-w", infix_to_prefix("x+y*z-w", buf, sizeof buf), EXPR_OK);
    check_string("prefix value", buf, "- + x * y z w");
    check_status("postfix of 12+34*5", infix_to_postfix("12+34*5", buf, sizeof buf), EXPR_OK);
    check_string("multi-digit postfix", buf, "12 34 5 * +");
    check_status("prefix of 12+34*5", infix_to_prefix("12+34*5", buf, sizeof buf), EXPR_OK);
    check_string("multi-digit prefix", buf, "+ 12 * 34 5");

    /* Example 3: prefix -> postfix (Lab P4). */
    printf("Example 3: prefix_to_postfix\n");
    check_status("*+ab+cd status", prefix_to_postfix("*+ab+cd", buf, sizeof buf), EXPR_OK);
    check_string("*+ab+cd value", buf, "a b + c d + *");
    check_status("multi-digit prefix status", prefix_to_postfix("+ 12 * 34 5", buf, sizeof buf), EXPR_OK);
    check_string("multi-digit prefix value", buf, "12 34 5 * +");
    check_status("single operand status", prefix_to_postfix("a", buf, sizeof buf), EXPR_OK);
    check_string("single operand value", buf, "a");

    if (failures == 0) {
        printf("\nAll visible tests passed.\n");
        return 0;
    }
    printf("\n%d visible test(s) FAILED.\n", failures);
    return 1;
}
