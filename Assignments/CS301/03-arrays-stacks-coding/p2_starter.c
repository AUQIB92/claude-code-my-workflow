/*
 * p2_starter.c -- fill in every function declared in p2_postfix.h.
 *
 * Rename this file to p2_postfix.c (or copy it) before submitting; it
 * must compile standalone against the unmodified p2_postfix.h.
 */

#include "p2_postfix.h"

void stack_init(IntStack *s)
{
    /* TODO: reset s to the empty state. */
}

int stack_push(IntStack *s, int v)
{
    /* TODO: boundary-check, then push. Return 1/0 per the contract. */
    return 0;
}

int stack_pop(IntStack *s, int *out)
{
    /* TODO: boundary-check, then pop into *out. Return 1/0 per the contract. */
    return 0;
}

int stack_is_empty(const IntStack *s)
{
    /* TODO */
    return 1;
}

int eval_postfix(const char *expr)
{
    /* TODO: tokenize expr on whitespace; push operands; on an operator,
       pop the right operand, pop the left operand, push left OP right.
       Use stack_push/stack_pop/stack_is_empty above -- do not touch the
       IntStack's fields directly from this function. */
    return 0;
}
