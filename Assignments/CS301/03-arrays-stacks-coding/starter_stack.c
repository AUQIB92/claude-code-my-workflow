/*
 * stack.c — your implementation of Week 3's Stack ADT + P1/P2 (Arrays/Stacks)
 *
 * Fill in every function declared in stack.h. Do not change stack.h. Do not
 * add any global/static mutable state — each function must work through the
 * IntStack pointer (or the input string) it is given.
 *
 * Compile check (from the assignment directory):
 *   gcc -Wall -Wextra -c stack.c -o stack.o
 *
 * Reminders from lecture:
 *   - top == -1 means empty; push writes data[++top], pop reads data[top--].
 *   - push on a full stack (top + 1 == STACK_MAX) and pop/peek on an empty
 *     stack are ERRORS — report them with the status codes in stack.h, not
 *     with a -1 sentinel (a -1 sentinel cannot tell "empty" from "held -1").
 *   - P1 pushes openers, matches closers against the top, and finishes with
 *     an empty stack iff the string is balanced.
 *   - P2 pushes numbers; on an operator, b = pop() FIRST, a = pop() second,
 *     then push apply(op, a, b). Swapping a and b breaks '-'/'/'/'%'.
 */

#include "stack.h"

void stack_init(IntStack *s)
{
    /* TODO: set s->top to -1. */
    (void)s;
}

int stack_is_empty(const IntStack *s)
{
    /* TODO: return 1 when s->top == -1, else 0. */
    (void)s;
    return 1;
}

int stack_size(const IntStack *s)
{
    /* TODO: return the element count (s->top + 1). */
    (void)s;
    return 0;
}

StackStatus stack_push(IntStack *s, int x)
{
    /* TODO: if full (s->top + 1 == STACK_MAX) return STACK_OVERFLOW and
       change nothing; else store x and return STACK_OK. */
    (void)s; (void)x;
    return STACK_OVERFLOW;
}

StackStatus stack_pop(IntStack *s, int *out)
{
    /* TODO: if empty return STACK_UNDERFLOW and change nothing; else remove
       the top, store it in *out (unless out is NULL), return STACK_OK. */
    (void)s; (void)out;
    return STACK_UNDERFLOW;
}

StackStatus stack_peek(const IntStack *s, int *out)
{
    /* TODO: if empty return STACK_UNDERFLOW and leave *out unchanged; else
       copy the top into *out (unless out is NULL) WITHOUT removing it. */
    (void)s; (void)out;
    return STACK_UNDERFLOW;
}

int is_balanced(const char *s)
{
    /* TODO: the lecture's one-stack scan (see stack.h for the exact rules:
       push openers, match-or-fail on closers, ignore all other characters,
       balanced iff the stack ends empty). */
    (void)s;
    return 0;
}

EvalStatus eval_postfix(const char *expr, int *out)
{
    /* TODO: the lecture's one-stack evaluator (see stack.h for the token
       rules and the six status codes). Remember: b pops first, a second;
       leave *out untouched on every non-OK path. */
    (void)expr; (void)out;
    return EVAL_MALFORMED;
}
