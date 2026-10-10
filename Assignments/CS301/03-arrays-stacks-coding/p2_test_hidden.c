/*
 * p2_test_hidden.c -- the autograder's hidden test suite for P2. NEVER
 * ship to students. Covers the adversarial bar from
 * algorithm-verification.md: the problem statement's own worked
 * examples, boundary sizes (single operand), structure-specific cases
 * (each of the four operators, a negative intermediate/final result,
 * multi-digit operands, an exact-division negative dividend, and a
 * chained multi-operator expression), a wide expression near
 * MAX_TOKENS (stack-capacity check), and >=20 random valid postfix
 * expressions checked against an independently-tokenized oracle
 * (strtok_s-free manual split, flagged below as hand-written -- the
 * evaluation ORDER it applies is dictated by the postfix definition
 * itself, same as any correct implementation, but the tokenizing code
 * path is deliberately different from the reference solution's).
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
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

/*
 * oracle_eval_postfix: independent hand-written oracle. Tokenizes with
 * strtok (a whole different code path from the reference solution's
 * manual isdigit/isspace scan) and keeps its value stack in a plain
 * local array instead of the IntStack type under test.
 */
static int oracle_eval_postfix(const char *expr)
{
    char   buf[4096];
    char  *tok;
    int    stk[MAX_TOKENS];
    int    top = -1;

    strncpy(buf, expr, sizeof(buf) - 1);
    buf[sizeof(buf) - 1] = '\0';

    tok = strtok(buf, " ");
    while (tok != NULL) {
        if (tok[0] >= '0' && tok[0] <= '9') {
            stk[++top] = atoi(tok);
        } else {
            int right = stk[top--];
            int left  = stk[top--];
            int result;
            switch (tok[0]) {
                case '+': result = left + right; break;
                case '-': result = left - right; break;
                case '*': result = left * right; break;
                default:  result = left / right; break;   /* '/' */
            }
            stk[++top] = result;
        }
        tok = strtok(NULL, " ");
    }
    return stk[top];
}

int main(void)
{
    int i;

    /* ---- Group 1: the problem statement's own worked examples ---- */
    printf("Group 1: worked examples (re-checked)\n");
    check("worked ex. 1: 12 2 3 * -",   eval_postfix("12 2 3 * -"), 6);
    check("worked ex. 2: 9 3 / 2 +",    eval_postfix("9 3 / 2 +"), 5);
    check("worked ex. 3: single operand", eval_postfix("42"), 42);
    check("worked ex. 4: 100 25 / 4 *", eval_postfix("100 25 / 4 *"), 16);

    /* ---- Group 2: boundary sizes ---- */
    printf("Group 2: single-operand boundaries\n");
    check("single-digit operand only", eval_postfix("7"), 7);
    check("multi-digit operand only",  eval_postfix("128"), 128);
    check("smallest valid pair: 5 3 -", eval_postfix("5 3 -"), 2);

    /* ---- Group 3: each operator, negative results, multi-digit ---- */
    printf("Group 3: each operator / negative results / multi-digit operands\n");
    check("addition",        eval_postfix("0 5 +"), 5);
    check("subtraction, positive result", eval_postfix("5 3 -"), 2);
    check("subtraction, negative result", eval_postfix("3 5 -"), -2);
    check("multiplication, by zero",      eval_postfix("6 0 *"), 0);
    check("multiplication, two multi-digit", eval_postfix("25 4 *"), 100);
    check("division, exact",              eval_postfix("144 12 /"), 12);
    check("division, three-digit operands", eval_postfix("1000 4 /"), 250);
    check("division, negative dividend, exact",
          eval_postfix("10 15 - 5 /"), -1);

    /* ---- Group 4: chained multi-operator expressions ---- */
    printf("Group 4: chained expressions\n");
    check("chained additions: 2 3 + 4 + 5 +", eval_postfix("2 3 + 4 + 5 +"), 14);
    check("chained, negative intermediate then multiply: 3 5 - 4 *",
          eval_postfix("3 5 - 4 *"), -8);
    check("chained, mixed operators: 20 4 / 3 2 - *",
          eval_postfix("20 4 / 3 2 - *"), 5);
    check("chained, all four operators: 8 4 / 3 + 2 * 1 -",
          eval_postfix("8 4 / 3 + 2 * 1 -"), 9);

    /* ---- Group 5: wide expression near MAX_TOKENS (capacity check) ---- */
    printf("Group 5: wide expression near MAX_TOKENS\n");
    {
        /* Push 1..20, then 19 '+' operators: sum = 210. 39 tokens total,
           well under MAX_TOKENS=100, but exercises a stack depth of 20
           -- the deepest this practical's tests push the array. */
        char buf[512];
        int  pos = 0;
        int  n = 20;
        int  j;
        for (j = 1; j <= n; j++) {
            pos += sprintf(buf + pos, "%s%d", (j > 1 ? " " : ""), j);
        }
        for (j = 1; j < n; j++) {
            pos += sprintf(buf + pos, " +");
        }
        check("sum of 1..20 via chained +", eval_postfix(buf), 210);
    }

    /* ---- Group 6: random valid postfix expressions vs. oracle (>=20) ---- */
    printf("Group 6: random valid postfix expressions vs. oracle\n");
    srand(20260902u);
    for (i = 0; i < 25; i++) {
        int  vals[16];
        int  nstack = 0;
        char buf[256];
        int  pos = 0;
        int  target = 3 + (rand() % 6);   /* 3..8 "build steps" */
        int  steps = 0;

        while (steps < target || nstack > 1) {
            int can_push = nstack < 6;
            int can_op   = nstack >= 2;
            int do_push  = can_op ? (can_push ? (rand() % 2) : 0) : 1;

            if (do_push) {
                int v = 1 + (rand() % 30);
                vals[nstack++] = v;
                pos += sprintf(buf + pos, "%s%d", (pos > 0 ? " " : ""), v);
            } else {
                int right = vals[nstack - 1];
                int left  = vals[nstack - 2];
                static const char ops[] = "+-*/";
                char op;
                int  tries = 0;
                do {
                    op = ops[rand() % 4];
                    tries++;
                } while (op == '/' && (right == 0 || left % right != 0) && tries < 8);
                if (op == '/' && (right == 0 || left % right != 0)) {
                    op = '+';   /* fallback: division would not be exact */
                }
                {
                    int result;
                    switch (op) {
                        case '+': result = left + right; break;
                        case '-': result = left - right; break;
                        case '*': result = left * right; break;
                        default:  result = left / right; break;
                    }
                    nstack -= 2;
                    vals[nstack++] = result;
                    pos += sprintf(buf + pos, " %c", op);
                }
            }
            steps++;
            if (steps > 40) break;   /* safety valve, should not trigger */
        }

        {
            char label[300];
            int  want = oracle_eval_postfix(buf);
            snprintf(label, sizeof(label), "random trial %d: \"%s\"", i, buf);
            check(label, eval_postfix(buf), want);
        }
    }

    printf("\n%d checks, %d failures.\n", checks, failures);
    return failures == 0 ? 0 : 1;
}
