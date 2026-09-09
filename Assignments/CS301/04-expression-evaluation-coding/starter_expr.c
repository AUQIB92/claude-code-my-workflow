/*
 * expr.c — your implementation of Week 4's expression conversions (P3/P4)
 *
 * Fill in every function declared in expr.h. Do not change expr.h. Do not
 * add any global/static mutable state — each function must work through the
 * input string and the output buffer it is given.
 *
 * Compile check with MSVC (this machine, from the assignment directory):
 *   cmd /c "vcvars64.bat >NUL && cl /nologo /W4 /Fe:test_visible.exe test_visible.c expr.c"
 *   .\test_visible.exe
 * Or with gcc (lab machines):
 *   gcc -std=c11 -Wall -Wextra -o test_visible test_visible.c expr.c
 *   ./test_visible
 *
 * Reminders from lecture:
 *   - infix->postfix: operands append to output; '(' pushes; ')' pops to
 *     output until '(' (both parens discarded); operator op pops waiting
 *     operators of >= precedence (strictly > if op is right-associative),
 *     then pushes. Each token is pushed/popped at most once: O(n).
 *   - infix->prefix: reverse the TOKEN stream (not the characters — "12"
 *     must stay "12"), swap parens, run the postfix pass under the mirror
 *     rule (pop only on strictly greater precedence), reverse the result.
 *   - prefix->postfix: scan RIGHT to left; operands push as strings;
 *     operator op pops a first, b second, pushes "a b op".
 *   - '^' is right-associative: "x^y^z" is "x y z ^ ^", NOT "x y ^ z ^".
 */

#include "expr.h"

ExprStatus infix_to_postfix(const char *infix, char *postfix, size_t out_size)
{
    /* TODO: tokenise (letters single, digits run, ops/parens single, spaces
       skipped), validate the infix grammar with an expect-operand flag,
       run the shunting-yard pass, join output tokens with single spaces. */
    (void)infix; (void)postfix; (void)out_size;
    return EXPR_BAD_INPUT;
}

ExprStatus infix_to_prefix(const char *infix, char *prefix, size_t out_size)
{
    /* TODO: tokenise, reverse + swap parens, postfix pass with the mirror
       rule (strictly-greater pops), reverse the token list, join. */
    (void)infix; (void)prefix; (void)out_size;
    return EXPR_BAD_INPUT;
}

ExprStatus prefix_to_postfix(const char *prefix, char *postfix, size_t out_size)
{
    /* TODO: tokenise (whitespace-split if any space/tab present, else one
       token per character), scan right-to-left with a stack of strings,
       join the single remaining entry. */
    (void)prefix; (void)postfix; (void)out_size;
    return EXPR_BAD_INPUT;
}
