/*
 * p1_reference_solution.c -- instructor-only reference implementation of
 * p1_bracket.h. DO NOT ship to students.
 *
 * Straight translation of the lecture's own balanced-bracket pseudocode
 * (Slides/CS301/03-arrays-stacks.tex, "Balanced-Parenthesis Algorithm"),
 * extended from a single bracket type to all three -- the same extension
 * Assignment 3's Q5 asks students to reason about in writing, done here
 * in code. Matching is done with matches_opener() rather than a chain of
 * if/else so the extension is a one-line table, not a copy-pasted branch
 * per bracket type.
 */

#include "p1_bracket.h"

void stack_init(CharStack *s)
{
    s->top = -1;
}

int stack_push(CharStack *s, char c)
{
    if (s->top == MAX_STACK - 1) {
        return 0;   /* overflow: no slot left */
    }
    s->top = s->top + 1;
    s->data[s->top] = c;
    return 1;
}

int stack_pop(CharStack *s, char *out)
{
    if (s->top == -1) {
        return 0;   /* underflow: nothing to remove */
    }
    *out = s->data[s->top];
    s->top = s->top - 1;
    return 1;
}

int stack_is_empty(const CharStack *s)
{
    return s->top == -1;
}

static int is_opener(char c)
{
    return c == '(' || c == '[' || c == '{';
}

static int is_closer(char c)
{
    return c == ')' || c == ']' || c == '}';
}

/* Does the popped opener match this closer? One table, not three branches. */
static int matches_opener(char opener, char closer)
{
    return (opener == '(' && closer == ')') ||
           (opener == '[' && closer == ']') ||
           (opener == '{' && closer == '}');
}

int is_balanced(const char *expr)
{
    CharStack s;
    int i;

    stack_init(&s);

    for (i = 0; expr[i] != '\0'; i++) {
        char c = expr[i];

        if (is_opener(c)) {
            /* Overflow cannot happen for a well-formed call: the stack
               holds at most one entry per input character. */
            stack_push(&s, c);
        } else if (is_closer(c)) {
            char opener;
            if (!stack_pop(&s, &opener)) {
                return 0;   /* closer with nothing open: unbalanced */
            }
            if (!matches_opener(opener, c)) {
                return 0;   /* wrong bracket TYPE, e.g. "(]" : unbalanced */
            }
        }
        /* Every other character (letters, digits, operators, spaces, ...)
           is not a bracket and is skipped, exactly as lecture states. */
    }

    return stack_is_empty(&s);   /* balanced iff every opener was closed */
}
