/*
 * p1_starter.c -- fill in every function declared in p1_bracket.h.
 *
 * Rename this file to p1_bracket.c (or copy it) before submitting; it
 * must compile standalone against the unmodified p1_bracket.h.
 */

#include "p1_bracket.h"

void stack_init(CharStack *s)
{
    /* TODO: reset s to the empty state. */
}

int stack_push(CharStack *s, char c)
{
    /* TODO: boundary-check, then push. Return 1/0 per the contract. */
    return 0;
}

int stack_pop(CharStack *s, char *out)
{
    /* TODO: boundary-check, then pop into *out. Return 1/0 per the contract. */
    return 0;
}

int stack_is_empty(const CharStack *s)
{
    /* TODO */
    return 1;
}

int is_balanced(const char *expr)
{
    /* TODO: scan expr, using stack_push/stack_pop/stack_is_empty above --
       do not touch the CharStack's fields directly from this function. */
    return 0;
}
