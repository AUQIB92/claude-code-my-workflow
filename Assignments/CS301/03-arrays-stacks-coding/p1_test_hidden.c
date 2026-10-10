/*
 * p1_test_hidden.c -- the autograder's hidden test suite for P1. NEVER
 * ship to students. Covers the adversarial bar from
 * algorithm-verification.md: the problem statement's own worked
 * examples, boundary sizes (empty/single char), structure-specific
 * cases (unmatched opener, closer-only, wrong-type mismatch, deep
 * nesting, adjacent independent groups, all-three-types mixed), a
 * long input near MAX_EXPR_LEN, and >=20 random inputs checked against
 * a hand-written oracle (flagged below -- a bug there would read
 * identically to a bug in the submission, so it is deliberately written
 * with different control flow from the reference solution).
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
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

/*
 * oracle_is_balanced: an independent hand-written oracle. Uses a plain
 * counter array of "still open, in order" brackets via a simple char
 * buffer + manual index instead of the CharStack type under test, and
 * a switch statement instead of the reference's table lookup, so a
 * mistranslation in one is unlikely to be mirrored in the other.
 * Flagged as hand-written per the oracle policy in
 * algorithm-verification.md.
 */
static int oracle_is_balanced(const char *expr)
{
    char stk[MAX_STACK];
    int  top = -1;
    int  i;

    for (i = 0; expr[i] != '\0'; i++) {
        char c = expr[i];
        switch (c) {
            case '(': case '[': case '{':
                top++;
                stk[top] = c;
                break;
            case ')':
                if (top < 0 || stk[top] != '(') return 0;
                top--;
                break;
            case ']':
                if (top < 0 || stk[top] != '[') return 0;
                top--;
                break;
            case '}':
                if (top < 0 || stk[top] != '{') return 0;
                top--;
                break;
            default:
                break;  /* not a bracket */
        }
    }
    return top == -1;
}

int main(void)
{
    int i;

    /* ---- Group 1: the problem statement's own worked examples ---- */
    printf("Group 1: worked examples (re-checked)\n");
    check("worked ex. 1: {[(a+b)*c]-d}", is_balanced("{[(a+b)*c]-d}"), 1);
    check("worked ex. 2: ([a+b)]",       is_balanced("([a+b)]"), 0);
    check("worked ex. 3: ((a+b]",        is_balanced("((a+b]"), 0);
    check("worked ex. 4: empty string",  is_balanced(""), 1);
    check("worked ex. 5: no brackets",   is_balanced("a+b*c"), 1);

    /* ---- Group 2: boundary sizes ---- */
    printf("Group 2: empty and single-character boundaries\n");
    check("empty string (again, boundary framing)", is_balanced(""), 1);
    check("single opener",  is_balanced("("), 0);
    check("single closer",  is_balanced(")"), 0);
    check("single non-bracket char", is_balanced("x"), 1);
    check("one matched pair", is_balanced("()"), 1);
    check("one matched pair, brace", is_balanced("{}"), 1);
    check("one matched pair, square", is_balanced("[]"), 1);

    /* ---- Group 3: structure-specific edge cases ---- */
    printf("Group 3: unmatched / wrong-type / deep-nesting / adjacent groups\n");
    check("unmatched opener buried in text", is_balanced("a(b+c*d"), 0);
    check("unmatched closer buried in text", is_balanced("a)b+c*d"), 0);
    check("wrong-type mismatch (]", is_balanced("(]"), 0);
    check("wrong-type mismatch [)", is_balanced("[)"), 0);
    check("wrong-type mismatch {)", is_balanced("{)"), 0);
    check("deep nesting, all same type", is_balanced("((((((((((x))))))))))"), 1);
    check("deep nesting, one extra opener", is_balanced("(((((((((( x)))))))))"), 0);
    check("deep nesting, mixed types balanced", is_balanced("{[({[()]})]}"), 1);
    check("adjacent independent groups", is_balanced("(a+b)*[c-d]+{e/f}"), 1);
    check("adjacent groups, second unbalanced", is_balanced("(a+b)*[c-d)+{e/f}"), 0);
    check("closer type flips order", is_balanced("([)]"), 0);
    check("brackets only, all three interleaved correctly",
          is_balanced("({[]})"), 1);
    check("brackets only, all three interleaved incorrectly",
          is_balanced("({[}])"), 0);

    /* ---- Group 4: a long input near MAX_EXPR_LEN (capacity check) ---- */
    printf("Group 4: long input near MAX_EXPR_LEN\n");
    {
        char buf[MAX_EXPR_LEN + 1];
        int  n = MAX_EXPR_LEN / 2;   /* n opens + n closes = MAX_EXPR_LEN */
        int  j;
        for (j = 0; j < n; j++) buf[j] = '(';
        for (j = 0; j < n; j++) buf[n + j] = ')';
        buf[2 * n] = '\0';
        check("long fully-nested balanced input", is_balanced(buf), 1);

        buf[2 * n - 1] = '(';   /* corrupt the last closer to an opener */
        check("long input, one corrupted closer", is_balanced(buf), 0);
    }

    /* ---- Group 5: random inputs vs. hand-written oracle (>=20) ---- */
    printf("Group 5: random inputs vs. hand-written oracle\n");
    srand(20260902u);
    for (i = 0; i < 40; i++) {
        char buf[64];
        int  len = 1 + (rand() % 40);
        int  j;
        static const char alphabet[] = "()[]{}ab+-";
        for (j = 0; j < len; j++) {
            buf[j] = alphabet[rand() % (int)(sizeof(alphabet) - 1)];
        }
        buf[len] = '\0';

        char label[96];
        snprintf(label, sizeof(label), "random trial %d: \"%s\"", i, buf);
        check(label, is_balanced(buf), oracle_is_balanced(buf));
    }

    printf("\n%d checks, %d failures.\n", checks, failures);
    return failures == 0 ? 0 : 1;
}
