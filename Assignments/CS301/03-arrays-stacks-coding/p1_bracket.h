/*
 * p1_bracket.h -- the contract for P1 (Balanced Bracket / Parenthesis
 * Check), Week 3's first institute practical.
 *
 * This header is given to you; do not change it. Your job is to provide
 * every function below in p1_bracket.c (start from p1_starter.c).
 *
 * You must implement the stack ADT yourself, over a fixed-size array --
 * exactly the array-backed stack from lecture (top index, -1 when empty,
 * push/pop with an explicit boundary check). Do NOT use any built-in
 * stack container (no C++ <stack>, no third-party library) -- the point
 * of this practical is the array-backed stack itself, not just the
 * bracket-matching logic on top of it.
 */

#ifndef P1_BRACKET_H
#define P1_BRACKET_H

/* MAX_EXPR_LEN bounds the input string; MAX_STACK is sized so a fully
   nested expression of the longest allowed input can never overflow the
   stack for a correct implementation (every stack slot corresponds to
   one still-open bracket, so it can never exceed the input length). */
#define MAX_EXPR_LEN 500
#define MAX_STACK    (MAX_EXPR_LEN + 1)

typedef struct {
    char data[MAX_STACK];
    int  top;   /* -1 when empty, matching the lecture's convention */
} CharStack;

/*
 * stack_init: reset s to the empty state (top = -1).
 */
void stack_init(CharStack *s);

/*
 * stack_push: push c onto s.
 *   - return 1 on success.
 *   - return 0 on overflow (top == MAX_STACK - 1 already) and leave the
 *     stack UNCHANGED -- exactly the boundary check lecture requires
 *     before every push.
 */
int stack_push(CharStack *s, char c);

/*
 * stack_pop: pop the top element of s into *out.
 *   - return 1 on success (top decremented, *out set to the popped char).
 *   - return 0 on underflow (s is empty) and leave *out UNCHANGED.
 */
int stack_pop(CharStack *s, char *out);

/*
 * stack_is_empty: return 1 if s has no elements (top == -1), else 0.
 */
int stack_is_empty(const CharStack *s);

/*
 * is_balanced: scan expr left to right using the lecture's algorithm
 * (push every opening bracket; on a closing bracket, pop and check the
 * popped character is the SAME bracket type's matching opener; a
 * closing bracket seen with an empty stack, or a popped opener of the
 * wrong type, is an immediate failure). Supports all three bracket
 * types: (), [], {}. Every other character (letters, digits, operators,
 * spaces, ...) is not a bracket and must be skipped -- it never touches
 * the stack, exactly as lecture states for the single-bracket-type case.
 *
 *   - expr is a NUL-terminated C string, length <= MAX_EXPR_LEN.
 *   - return 1 if every bracket is matched (including the case where
 *     expr contains no brackets at all, or is the empty string -- both
 *     are trivially balanced).
 *   - return 0 if any bracket is unmatched, of the wrong type, or the
 *     stack is non-empty after the scan finishes (an opener that never
 *     closed).
 */
int is_balanced(const char *expr);

#endif /* P1_BRACKET_H */
