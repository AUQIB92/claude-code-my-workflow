/*
 * expr.h — expression-conversion contract (Week 4: Expression Evaluation)
 *
 * The contract says WHAT each function must do, not HOW the stack is laid
 * out. This header is given to you; do not change it. Your job is to provide
 * every function below in expr.c (start from starter_expr.c).
 *
 * Representation: the lecture's one-stack algorithms (deck: infix->postfix
 * left-to-right shunting-yard; infix->prefix by reverse-swap-postfix-reverse;
 * prefix->postfix right-to-left stack of strings). All three conversions make
 * a single pass at O(n) time worst case in the input length, holding at most
 * O(n) auxiliary space. No heap allocation is required — fixed-size local
 * stacks suffice for the bounds below.
 *
 * Unlike the slides — which use single letters and skip error handling to
 * keep the slide readable — every fallible function here reports an explicit
 * status code, and operands may be multi-digit integers as well as letters.
 * Getting the status codes right is part of the grade.
 */

#ifndef EXPR_H
#define EXPR_H

#include <stddef.h> /* size_t */

#define EXPR_MAX 256 /* output buffer size (incl. NUL) used by the tests */

/*
 * Status codes for the three conversions. On ANY non-OK status the output
 * buffer is left in an unspecified state — the caller must not read it.
 */
typedef enum {
    EXPR_OK = 0,              /* success; output holds the result */
    EXPR_BAD_INPUT = 1,       /* NULL pointer, out_size == 0, or
                                 empty/whitespace-only input */
    EXPR_MISMATCHED_PARENS = 2, /* a ')' with nothing open, or '(' never
                                   closed (infix inputs only) */
    EXPR_INVALID_TOKEN = 3,   /* unknown character, malformed infix grammar
                                 (empty parens, operator at an end, two
                                 operators or two operands in a row, ...),
                                 or a malformed prefix stream that leaves
                                 zero or 2+ values (e.g. "a b", "") */
    EXPR_TOO_FEW_OPERANDS = 4, /* prefix operator with fewer than two
                                  operands on the stack (e.g. "+ a") */
    EXPR_OVERFLOW = 5         /* result (incl. NUL) does not fit in out_size */
} ExprStatus;

/*
 * Token rules shared by all three functions.
 *
 * Operands: a single letter [A-Za-z] (e.g. a, x) OR a non-negative
 *   multi-digit integer [0-9]+ (e.g. 12, 305). No unary minus: a leading '-'
 *   is always the binary subtraction operator in infix, never part of a
 *   number. (Week 3's postfix evaluator accepted negative literals; infix
 *   conversion does not — "a+-b" is EXPR_INVALID_TOKEN, not "a + (-b)".)
 * Operators: exactly one of + - * / ^ (single character).
 *   Precedence: ^ (highest) > * / (medium) > + - (low).
 *   Associativity: ^ is RIGHT-associative (x^y^z means x^(y^z));
 *   all others are LEFT-associative (a-b-c means (a-b)-c).
 * Parentheses: ( ) override precedence (infix inputs only).
 * Spaces/tabs may appear anywhere and are ignored, except that they delimit
 *   multi-digit numbers: "12+34*5" and "12 + 34 * 5" are the same expression.
 * Output format: tokens joined by exactly one space, no leading/trailing
 *   space, NUL-terminated. E.g. "x y z * + w -".
 *
 * infix_to_postfix: rewrite infix for the stack (Lab P3, first half).
 *   E.g. "x+y*z-w" -> "x y z * + w -".
 *   Grammar errors (EXPR_INVALID_TOKEN): empty parens "()", an operator
 *   first/last ("+ab", "ab+"), two operators in a row ("a++b"), two operands
 *   in a row ("ab" without an operator — note "12 34" is two operands),
 *   a missing operator between ')' and an operand ("(a)b"), or anything
 *   that is not an operand/operator/paren/space (e.g. '&', '$', '.').
 */
ExprStatus infix_to_postfix(const char *infix, char *postfix, size_t out_size);

/*
 * infix_to_prefix: rewrite infix operator-first (Lab P3, second half) by
 *   the lecture's reversal route: reverse the token stream and swap parens,
 *   run the postfix pass under the mirror rule (pop only on strictly greater
 *   precedence), then reverse the result.
 *   E.g. "x+y*z-w" -> "- + x * y z w".
 *   Same token, grammar, paren, and overflow rules as infix_to_postfix.
 *   The paren swap is load-bearing: "(x+y)*(z-w)" reversed without swapping
 *   binds every bracket backwards.
 */
ExprStatus infix_to_prefix(const char *infix, char *prefix, size_t out_size);

/*
 * prefix_to_postfix: rewrite prefix back to postfix (Lab P4) by scanning
 *   right to left with a stack of strings: operand -> push as a string;
 *   operator op -> a = pop(), b = pop(), push "a b op".
 *   E.g. "*+ab+cd" -> "a b + c d + *".
 *
 * Prefix tokenisation: if the string contains any space/tab, it is split on
 *   whitespace (multi-digit numbers allowed: "+ 12 * 34 5"). Otherwise each
 *   non-space character is one token and every operand is a single
 *   letter/digit ("*+ab+cd") — except a bare all-digit string, which is one
 *   number ("42" -> "42"). Unknown characters (e.g. '&') are
 *   EXPR_INVALID_TOKEN, never silently skipped.
 * A single operand alone is the identity: "a" -> "a", "42" -> "42".
 */
ExprStatus prefix_to_postfix(const char *prefix, char *postfix, size_t out_size);

#endif /* EXPR_H */
