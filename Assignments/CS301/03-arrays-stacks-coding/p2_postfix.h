/*
 * p2_postfix.h -- the contract for P2 (Postfix Expression Evaluation),
 * Week 3's second institute practical.
 *
 * This header is given to you; do not change it. Your job is to provide
 * every function below in p2_postfix.c (start from p2_starter.c).
 *
 * Same discipline as P1: implement the stack ADT yourself over a
 * fixed-size array (top index, -1 when empty, explicit boundary
 * checks). Do NOT use any built-in stack container.
 */

#ifndef P2_POSTFIX_H
#define P2_POSTFIX_H

/* MAX_TOKENS bounds the number of operands + operators in one postfix
   string. The operand stack never holds more entries than operands seen
   so far, so MAX_STACK = MAX_TOKENS is always enough. */
#define MAX_TOKENS 100
#define MAX_STACK  MAX_TOKENS

typedef struct {
    int data[MAX_STACK];
    int top;   /* -1 when empty, matching the lecture's convention */
} IntStack;

/*
 * stack_init: reset s to the empty state (top = -1).
 */
void stack_init(IntStack *s);

/*
 * stack_push: push v onto s.
 *   - return 1 on success.
 *   - return 0 on overflow (top == MAX_STACK - 1 already) and leave the
 *     stack UNCHANGED.
 */
int stack_push(IntStack *s, int v);

/*
 * stack_pop: pop the top element of s into *out.
 *   - return 1 on success (top decremented, *out set to the popped value).
 *   - return 0 on underflow (s is empty) and leave *out UNCHANGED.
 */
int stack_pop(IntStack *s, int *out);

/*
 * stack_is_empty: return 1 if s has no elements (top == -1), else 0.
 */
int stack_is_empty(const IntStack *s);

/*
 * eval_postfix: evaluate a postfix (Reverse Polish) expression using the
 * lecture's algorithm (operands push; each operator pops the RIGHT
 * operand first, then the LEFT operand, applies the operator LEFT-OP-
 * RIGHT, and pushes the result). The final, only, value left on the
 * stack is the answer.
 *
 * Input format:
 *   - expr is a NUL-terminated C string: whitespace-separated tokens.
 *   - Every operand is a non-negative integer literal, one or more
 *     digits (e.g. "7", "42", "128") -- single-digit AND multi-digit
 *     operands both occur; there is no minus sign on an operand token
 *     (a '-' token is always the subtraction operator, never a sign).
 *   - Every operator is exactly one of + - * /, appearing as its own
 *     token, surrounded by whitespace on each side like any other token.
 *   - There is at most one space between consecutive tokens, and no
 *     leading or trailing whitespace.
 *
 * PRECONDITION (guaranteed by every test the autograder runs): expr is
 * a well-formed postfix expression for the given tokens (evaluating it
 * never pops from an empty stack, and exactly one value remains at the
 * end), and every division that occurs divides its dividend by its
 * divisor with ZERO remainder, divisor != 0 -- so the correct integer
 * result is unambiguous regardless of C's truncation-toward-zero
 * convention for "/". You do not need to detect or handle a malformed
 * expression.
 *
 *   - return the single int value left on the stack after evaluating
 *     every token.
 */
int eval_postfix(const char *expr);

#endif /* P2_POSTFIX_H */
