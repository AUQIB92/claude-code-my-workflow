/*
 * stack.h — the Stack ADT + P1/P2 contract (Week 3: Arrays and Stacks)
 *
 * The contract says WHAT each function must do, not HOW the array is laid
 * out. This header is given to you; do not change it. Your job is to provide
 * every function below in stack.c (start from starter_stack.c).
 *
 * Representation (fixed by this header): one int array of STACK_MAX cells
 * plus one index, top, exactly as in lecture (deck: MAX 100, top == -1 means
 * empty). P1 stores bracket characters in the int cells as their char codes.
 *
 * Unlike the lecture slides — which return -1 on pop/peek errors to keep the
 * slide readable — every fallible function here reports an explicit status
 * code. A -1 sentinel cannot distinguish "the stack held -1" from "the stack
 * was empty"; the status codes below can. Using them correctly is part of
 * the grade.
 */

#ifndef STACK_H
#define STACK_H

#define STACK_MAX 100  /* fixed capacity, as in lecture */

/* Status codes for the three stack operations. */
typedef enum {
    STACK_OK = 0,       /* the operation succeeded */
    STACK_OVERFLOW = 1, /* push onto a full stack (top + 1 == STACK_MAX) */
    STACK_UNDERFLOW = 2 /* pop/peek on an empty stack (top == -1) */
} StackStatus;

typedef struct {
    int data[STACK_MAX];
    int top;  /* index of the top element; -1 means empty */
} IntStack;

/*
 * stack_init: set s->top to -1 (empty). Call once before any other
 * operation on s.
 */
void stack_init(IntStack *s);

/*
 * stack_is_empty: return 1 if s holds no elements, 0 otherwise.
 * stack_size: return the number of elements in s (0 when empty).
 */
int stack_is_empty(const IntStack *s);
int stack_size(const IntStack *s);

/*
 * stack_push: place x on the top.
 *   - return STACK_OK and store x when the stack is not full.
 *   - return STACK_OVERFLOW and change nothing when top + 1 == STACK_MAX.
 */
StackStatus stack_push(IntStack *s, int x);

/*
 * stack_pop: remove the top item and store it in *out.
 *   - return STACK_OK when the stack is not empty.
 *   - return STACK_UNDERFLOW and change nothing (neither the stack nor
 *     *out) when the stack is empty.
 *   - out may be NULL, meaning "discard the popped value".
 */
StackStatus stack_pop(IntStack *s, int *out);

/*
 * stack_peek: copy the top item into *out WITHOUT removing it.
 *   - return STACK_OK when the stack is not empty.
 *   - return STACK_UNDERFLOW and leave *out unchanged when empty.
 *   - out may be NULL, meaning "check emptiness only".
 */
StackStatus stack_peek(const IntStack *s, int *out);

/*
 * P1 — is_balanced: return 1 if every opener in s is closed in the right
 * order, 0 otherwise. The lecture's one-stack algorithm: push openers
 * ( [ { ; on a closer ) ] } report 0 if the stack is empty or the top is
 * not its match, else pop; at the end, balanced iff the stack is empty.
 *   - Only the six bracket characters matter; every other character
 *     (letters, digits, spaces, operators) is ignored, so "(a+b)*[c]" is
 *     checked as "()[]".
 *   - The empty string is balanced (returns 1); NULL returns 0.
 *   - Fixed-capacity limit: a string needing more than STACK_MAX
 *     simultaneously-open brackets returns 0 (the array is full, so the
 *     nesting cannot be verified — the price of a fixed array, as in
 *     lecture). A 150-deep balanced string therefore reports 0 here.
 */
int is_balanced(const char *s);

/*
 * P2 — eval_postfix: evaluate a postfix expression with one stack and store
 * the answer in *out. The lecture's algorithm: numbers are pushed; on an
 * operator op, b = pop(), a = pop(), then push apply(op, a, b); at the end
 * the answer is the single remaining value.
 *
 * Token rules (tokens are separated by one or more spaces/tabs):
 *   - An integer literal is an optional leading '-' followed by one or more
 *     digits (e.g. 42, -7, 1000). It must fit in an int. A leading '+' is
 *     NOT accepted ("+5" is a bad token). A lone "-" is the minus operator,
 *     not a number.
 *   - An operator is exactly one of the single characters + - * / %.
 *     Division and remainder follow C semantics (truncation toward zero;
 *     the sign of % follows the dividend). Order matters: "8 3 -" is 5.
 *   - Anything else (letters, multi-character operators, "++") is a bad
 *     token.
 *
 * Status codes (on ANY non-OK status, *out is left unchanged):
 *   - EVAL_OK: success; *out holds the answer.
 *   - EVAL_BAD_TOKEN: a token is neither an integer literal nor an operator.
 *   - EVAL_TOO_FEW_OPERANDS: an operator found fewer than two operands
 *     on the stack (e.g. "2 +" or "+").
 *   - EVAL_DIV_BY_ZERO: '/' or '%' with a zero divisor.
 *   - EVAL_MALFORMED: empty/whitespace-only input, NULL input, NULL out,
 *     or a token stream that does not leave exactly one value (e.g. "2 3").
 *   - EVAL_OVERFLOW: more than STACK_MAX pending operands at once.
 */
typedef enum {
    EVAL_OK = 0,
    EVAL_BAD_TOKEN = 1,
    EVAL_TOO_FEW_OPERANDS = 2,
    EVAL_DIV_BY_ZERO = 3,
    EVAL_MALFORMED = 4,
    EVAL_OVERFLOW = 5
} EvalStatus;

EvalStatus eval_postfix(const char *expr, int *out);

#endif /* STACK_H */
