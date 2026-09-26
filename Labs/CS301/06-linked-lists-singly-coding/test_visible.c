/*
 * test_visible.c — the visible tests, one per worked example in the lab
 * problem statement. Run locally to sanity-check your slist.c before
 * submitting; the autograder runs a LARGER hidden suite on top of these.
 *
 * Build + run (from the lab directory):
 *   gcc -std=c11 -Wall -Wextra -o test_visible test_visible.c slist.c
 *   ./test_visible
 */

#include <stdio.h>
#include "slist.h"

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
    /* Example 1: build the chain 17 -> 42 -> 88. */
    {
        SNode *head = NULL;
        int buf[8], n;
        printf("Example 1: front-insert 42, front-insert 17, end-insert 88\n");
        check("insert_front(42) non-NULL",
              slist_insert_front(&head, 42) != NULL, 1);
        check("insert_front(17) non-NULL",
              slist_insert_front(&head, 17) != NULL, 1);
        check("insert_end(88) non-NULL",
              slist_insert_end(&head, 88) != NULL, 1);
        check("length is 3", (long long)slist_length(head), 3);
        n = slist_display(head, buf, 8);
        check("display writes 3", n, 3);
        check("order [0] is 17", buf[0], 17);
        check("order [1] is 42", buf[1], 42);
        check("order [2] is 88", buf[2], 88);
        slist_free(&head);
        check("free sets head NULL", head == NULL, 1);
    }

    /* Example 2: position insert, delete, search on the 17-42-88 chain. */
    {
        SNode *head = NULL;
        SNode *f;
        int buf[8], n;
        printf("Example 2: insert_at(1, 63), delete 42, search\n");
        slist_insert_end(&head, 17);
        slist_insert_end(&head, 42);
        slist_insert_end(&head, 88);
        check("insert_at(1, 63) ok", slist_insert_at(&head, 1, 63), 0);
        n = slist_display(head, buf, 8);
        check("display writes 4", n, 4);
        check("order [0] is 17", buf[0], 17);
        check("order [1] is 63", buf[1], 63);
        check("order [2] is 42", buf[2], 42);
        check("order [3] is 88", buf[3], 88);
        check("delete 42 ok", slist_delete_value(&head, 42), 0);
        check("length now 3", (long long)slist_length(head), 3);
        f = slist_search(head, 63);
        check("search(63) found", f != NULL, 1);
        check("search(63) value", f != NULL ? f->data : -1, 63);
        check("search(77) absent", slist_search(head, 77) == NULL, 1);
        n = slist_display(head, buf, 8);
        check("survivors display 3", n, 3);
        check("survivor [0] is 17", buf[0], 17);
        check("survivor [1] is 63", buf[1], 63);
        check("survivor [2] is 88", buf[2], 88);
        slist_free(&head);
    }

    /* Example 3: reverse 17 -> 63 -> 88, then edge reverses. */
    {
        SNode *head = NULL;
        int buf[8], n;
        printf("Example 3: reverse, delete head, single/empty reverse\n");
        slist_insert_end(&head, 17);
        slist_insert_end(&head, 63);
        slist_insert_end(&head, 88);
        slist_reverse(&head);
        n = slist_display(head, buf, 8);
        check("reversed writes 3", n, 3);
        check("reversed [0] is 88", buf[0], 88);
        check("reversed [1] is 63", buf[1], 63);
        check("reversed [2] is 17", buf[2], 17);
        check("delete head 88 ok", slist_delete_value(&head, 88), 0);
        check("length now 2", (long long)slist_length(head), 2);
        slist_reverse(&head);
        n = slist_display(head, buf, 8);
        check("re-reversed writes 2", n, 2);
        check("re-reversed [0] is 17", buf[0], 17);
        check("re-reversed [1] is 63", buf[1], 63);
        slist_free(&head);
        slist_reverse(&head); /* reverse of freed (NULL) list: safe no-op */
        check("reverse after free safe", head == NULL, 1);
        check("length of empty is 0", (long long)slist_length(head), 0);
    }

    if (failures == 0) {
        printf("\nAll visible tests passed.\n");
        return 0;
    }
    printf("\n%d visible test(s) FAILED.\n", failures);
    return 1;
}
