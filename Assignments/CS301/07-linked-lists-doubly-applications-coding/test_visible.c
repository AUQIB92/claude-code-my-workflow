/*
 * test_visible.c — the visible tests, one per worked example in the P7
 * problem statement. Run locally to sanity-check your dlist.c before
 * submitting; the autograder runs a LARGER hidden suite on top of these.
 *
 * Build + run (from the assignment directory):
 *   gcc -std=c11 -Wall -Wextra -Werror -o test_visible test_visible.c dlist.c
 *   ./test_visible
 */

#include <stdio.h>
#include "dlist.h"

static int failures = 0;

static void check(const char *name, long long got, long long want)
{
    if (got == want) {
        printf("  PASS  %s\n", name);
    } else {
        printf("  FAIL  %s (got %lld, want %lld)\n", name, got, want);
        failures++;
    }
}

int main(void)
{
    /* Example 1: build, insert, and read the chain both ways. */
    {
        DNode *head = NULL, *f;
        int fwd[8], bwd[8], n;
        printf("Example 1: insert_back 14,28,42; insert_front 7; insert_after 14 -> 21\n");
        check("insert_back(14) non-NULL", dlist_insert_back(&head, 14) != NULL, 1);
        check("insert_back(28) non-NULL", dlist_insert_back(&head, 28) != NULL, 1);
        check("insert_back(42) non-NULL", dlist_insert_back(&head, 42) != NULL, 1);
        check("insert_front(7) non-NULL", dlist_insert_front(&head, 7) != NULL, 1);
        f = dlist_search(head, 14);
        check("search(14) found", f != NULL, 1);
        check("insert_after(14,21) non-NULL", dlist_insert_after(f, 21) != NULL, 1);
        n = dlist_print_forward(head, fwd, 8);
        check("forward writes 5", n, 5);
        check("forward [0] is 7", fwd[0], 7);
        check("forward [1] is 14", fwd[1], 14);
        check("forward [2] is 21", fwd[2], 21);
        check("forward [3] is 28", fwd[3], 28);
        check("forward [4] is 42", fwd[4], 42);
        n = dlist_print_backward(head, bwd, 8);
        check("backward writes 5", n, 5);
        check("backward [0] is 42", bwd[0], 42);
        check("backward [1] is 28", bwd[1], 28);
        check("backward [2] is 21", bwd[2], 21);
        check("backward [3] is 14", bwd[3], 14);
        check("backward [4] is 7", bwd[4], 7);
        dlist_free(&head);
        check("free sets head NULL", head == NULL, 1);
    }

    /* Example 2: delete from both ends and by pointer, plus search. */
    {
        DNode *head = NULL, *f;
        int v = -999, buf[8], n;
        printf("Example 2: delete_front, delete_back, delete_node, search\n");
        dlist_insert_back(&head, 14);
        dlist_insert_back(&head, 28);
        dlist_insert_back(&head, 42);
        check("delete_front gives 14",
              (dlist_delete_front(&head, &v) == 0) ? v : -999, 14);
        check("delete_back gives 42",
              (dlist_delete_back(&head, &v) == 0) ? v : -999, 42);
        n = dlist_print_forward(head, buf, 8);
        check("survivor is just 28", (n == 1 && buf[0] == 28) ? 1 : 0, 1);
        f = dlist_search(head, 28);
        check("search(28) is the head", f == head, 1);
        check("search(99) absent", dlist_search(head, 99) == NULL, 1);
        check("delete_node(28) ok", dlist_delete_node(&head, f), 0);
        check("empty after delete_node", head == NULL, 1);
        check("delete_front on empty is -1", dlist_delete_front(&head, &v), -1);
        check("delete_back on empty is -1", dlist_delete_back(&head, &v), -1);
        dlist_free(&head);
    }

    /* Example 3: reverse, and a polynomial addition with cancellation. */
    {
        DNode *head = NULL;
        int fwd[4], bwd[4], n;
        static const int ac[] = { 5, 3 };
        static const int ae[] = { 2, 0 };
        static const int bc[] = { -5, 4 };
        static const int be[] = { 2, 1 };
        static const int rc[] = { 4, 3 };
        static const int re[] = { 1, 0 };
        struct poly A, B, C;
        const PNode *q;
        int i, ok;
        printf("Example 3: reverse, then poly_add (5x^2+3) + (-5x^2+4x) = 4x+3\n");
        dlist_insert_back(&head, 28);
        dlist_insert_back(&head, 35);
        dlist_reverse(&head);
        n = dlist_print_forward(head, fwd, 4);
        check("reverse forward writes 2", n, 2);
        check("reverse forward [0] is 35", fwd[0], 35);
        check("reverse forward [1] is 28", fwd[1], 28);
        n = dlist_print_backward(head, bwd, 4);
        check("reverse backward [0] is 28", bwd[0], 28);
        check("reverse backward [1] is 35", bwd[1], 35);
        dlist_reverse(&head);
        n = dlist_print_forward(head, fwd, 4);
        check("double-reverse restores 28,35", (n == 2 && fwd[0] == 28 && fwd[1] == 35) ? 1 : 0, 1);
        dlist_free(&head);

        poly_init(&A);
        poly_init(&B);
        poly_init(&C);
        check("append A (5,2) ok", poly_append_term(&A, ac[0], ae[0]), 0);
        check("append A (3,0) ok", poly_append_term(&A, ac[1], ae[1]), 0);
        check("append B (-5,2) ok", poly_append_term(&B, bc[0], be[0]), 0);
        check("append B (4,1) ok", poly_append_term(&B, bc[1], be[1]), 0);
        check("poly_add ok", poly_add(&A, &B, &C), 0);
        q = C.head;
        ok = 1;
        i = 0;
        while (q != NULL && i < 6) {
            if (i >= 2 || q->coeff != rc[i] || q->exp != re[i]) {
                ok = 0;
            }
            q = q->next;
            i++;
        }
        check("poly sum is 4x + 3 (2 terms)", (ok && i == 2) ? 1 : 0, 1);
        check("poly sum tail is last term", (C.tail != NULL && C.tail->next == NULL) ? 1 : 0, 1);
        poly_free(&A);
        poly_free(&B);
        poly_free(&C);
    }

    if (failures == 0) {
        printf("\nAll visible tests passed.\n");
        return 0;
    }
    printf("\n%d visible test(s) FAILED.\n", failures);
    return 1;
}
