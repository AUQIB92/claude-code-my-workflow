/*
 * p2_reference_solution.c -- instructor-only reference implementation of
 * p2_postfix.h. DO NOT ship to students.
 *
 * Straight translation of the lecture's own postfix-evaluation
 * pseudocode (Slides/CS301/03-arrays-stacks.tex, "Postfix Evaluation
 * Algorithm") -- operands push; each operator pops the RIGHT operand
 * first, then the LEFT, applies left OP right, and pushes the result --
 * extended from single-digit tokens to whitespace-separated multi-digit
 * ones via a small hand-written tokenizer (isdigit/isspace only, no
 * strtok, so the parsing decisions are fully explicit here rather than
 * hidden behind a standard-library state machine).
 */

#include <ctype.h>
#include "p2_postfix.h"

void stack_init(IntStack *s)
{
    s->top = -1;
}

int stack_push(IntStack *s, int v)
{
    if (s->top == MAX_STACK - 1) {
        return 0;   /* overflow: no slot left */
    }
    s->top = s->top + 1;
    s->data[s->top] = v;
    return 1;
}

int stack_pop(IntStack *s, int *out)
{
    if (s->top == -1) {
        return 0;   /* underflow: nothing to remove */
    }
    *out = s->data[s->top];
    s->top = s->top - 1;
    return 1;
}

int stack_is_empty(const IntStack *s)
{
    return s->top == -1;
}

static int apply_op(int left, char op, int right)
{
    switch (op) {
        case '+': return left + right;
        case '-': return left - right;
        case '*': return left * right;
        case '/': return left / right;   /* precondition: divides exactly */
        default:  return 0;              /* unreachable per the contract */
    }
}

int eval_postfix(const char *expr)
{
    IntStack s;
    int i = 0;

    stack_init(&s);

    while (expr[i] != '\0') {
        /* Skip the single space between tokens (and any leading run,
           though the contract promises none). */
        while (expr[i] == ' ') {
            i++;
        }
        if (expr[i] == '\0') {
            break;   /* trailing whitespace consumed; nothing left */
        }

        if (isdigit((unsigned char)expr[i])) {
            /* Operand token: one or more digits. */
            int value = 0;
            while (isdigit((unsigned char)expr[i])) {
                value = value * 10 + (expr[i] - '0');
                i++;
            }
            stack_push(&s, value);
        } else {
            /* Operator token: exactly one of + - * /. */
            char op = expr[i];
            int right = 0, left = 0;   /* defensive init: silences a
                                           spurious -O2 maybe-uninitialized
                                           warning; stack_pop always sets
                                           these under the guaranteed
                                           well-formed-expression precondition */
            i++;
            stack_pop(&s, &right);   /* popped FIRST: the right operand */
            stack_pop(&s, &left);    /* popped SECOND: the left operand */
            stack_push(&s, apply_op(left, op, right));
        }
    }

    {
        int result = 0;
        stack_pop(&s, &result);   /* the single, only, value left */
        return result;
    }
}
