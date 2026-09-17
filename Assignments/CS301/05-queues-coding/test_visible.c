/*
 * test_visible.c — the visible tests, one per worked example in the
 * assignment statement. Run locally to sanity-check your queue.c before
 * submitting; the autograder runs a LARGER hidden suite on top of these.
 *
 * Build + run (from the assignment directory):
 *   gcc -Wall -Wextra -o test_visible test_visible.c queue.c
 *   ./test_visible
 */

#include <stdio.h>
#include "queue.h"

static int failures = 0;

static void check(const char *name, int got, int want)
{
    if (got == want) {
        printf("  PASS  %s\n", name);
    } else {
        printf("  FAIL  %s (got %d, want %d)\n", name, got, want);
        failures++;
    }
}

int main(void)
{
    /* Example 1: the circular queue itself (enqueue/front/dequeue). */
    {
        CQueue q;
        int v = -999;
        printf("Example 1: circular enqueue/front/dequeue discipline\n");
        cqueue_init(&q);
        check("empty after init", cqueue_is_empty(&q), 1);
        check("size 0 after init", cqueue_size(&q), 0);
        check("enqueue(5) ok", cqueue_enqueue(&q, 5), CQ_OK);
        check("enqueue(15) ok", cqueue_enqueue(&q, 15), CQ_OK);
        check("enqueue(25) ok", cqueue_enqueue(&q, 25), CQ_OK);
        check("front is 5", (cqueue_front(&q, &v) == CQ_OK) ? v : -999, 5);
        check("size still 3 after front", cqueue_size(&q), 3);
        check("dequeue is 5", (cqueue_dequeue(&q, &v) == CQ_OK) ? v : -999, 5);
        check("dequeue is 15", (cqueue_dequeue(&q, &v) == CQ_OK) ? v : -999, 15);
        check("size now 1", cqueue_size(&q), 1);
        check("front is now 25", (cqueue_front(&q, &v) == CQ_OK) ? v : -999, 25);
    }

    /* Example 2: wraparound + display + honest full/empty (P5). */
    {
        CQueue q;
        int v = -999, buf[QUEUE_MAX], n, i;
        static const int want_live[] = { 13, 14, 15, 16, 17, 18, 19 };
        static const int want_drain[] = { 13, 14, 15, 16, 17, 18, 19, 20 };
        int ok;
        printf("Example 2: wraparound, display, full/empty\n");
        cqueue_init(&q);
        for (i = 11; i <= 16; i++) {
            cqueue_enqueue(&q, i);
        }
        check("dequeue is 11", (cqueue_dequeue(&q, &v) == CQ_OK) ? v : -999, 11);
        check("dequeue is 12", (cqueue_dequeue(&q, &v) == CQ_OK) ? v : -999, 12);
        check("enqueue(17) ok", cqueue_enqueue(&q, 17), CQ_OK);
        check("enqueue(18) ok", cqueue_enqueue(&q, 18), CQ_OK);
        check("enqueue(19) wraps to index 0", cqueue_enqueue(&q, 19), CQ_OK);
        check("size 7 after wrap", cqueue_size(&q), 7);
        check("not full at 7 of 8", cqueue_is_full(&q), 0);
        n = cqueue_display(&q, buf, QUEUE_MAX);
        check("display writes 7 items", n, 7);
        ok = (n == 7);
        for (i = 0; ok && i < 7; i++) {
            if (buf[i] != want_live[i]) {
                ok = 0;
            }
        }
        check("display order is 13..19 front-to-rear", ok, 1);
        check("enqueue(20) fills the ring", cqueue_enqueue(&q, 20), CQ_OK);
        check("full at 8 of 8", cqueue_is_full(&q), 1);
        check("enqueue(21) is FULL", cqueue_enqueue(&q, 21), CQ_FULL);
        ok = 1;
        for (i = 0; i < 8; i++) {
            if (cqueue_dequeue(&q, &v) != CQ_OK || v != want_drain[i]) {
                ok = 0;
            }
        }
        check("drain order is 13..20", ok, 1);
        check("empty after drain", cqueue_is_empty(&q), 1);
        check("dequeue on empty is EMPTY",
              cqueue_dequeue(&q, &v), CQ_EMPTY);
    }

    /* Example 3: unordered priority queue (P6). */
    {
        PQueue pq;
        int v = -999, p = -999;
        printf("Example 3: priority enqueue/peek_min/delete_min\n");
        pqueue_init(&pq);
        check("empty after init", pqueue_is_empty(&pq), 1);
        check("enqueue(701,4) ok", pqueue_enqueue(&pq, 701, 4), PQ_OK);
        check("enqueue(702,1) ok", pqueue_enqueue(&pq, 702, 1), PQ_OK);
        check("enqueue(703,3) ok", pqueue_enqueue(&pq, 703, 3), PQ_OK);
        check("peek_min value is 702",
              (pqueue_peek_min(&pq, &v, &p) == PQ_OK) ? v : -999, 702);
        check("peek_min priority is 1", p, 1);
        check("size still 3 after peek", pqueue_size(&pq), 3);
        check("delete_min value is 702",
              (pqueue_delete_min(&pq, &v, &p) == PQ_OK) ? v : -999, 702);
        check("delete_min value is 703",
              (pqueue_delete_min(&pq, &v, &p) == PQ_OK) ? v : -999, 703);
        check("enqueue(704,1) ok", pqueue_enqueue(&pq, 704, 1), PQ_OK);
        check("delete_min value is 704",
              (pqueue_delete_min(&pq, &v, &p) == PQ_OK) ? v : -999, 704);
        check("delete_min value is 701",
              (pqueue_delete_min(&pq, &v, &p) == PQ_OK) ? v : -999, 701);
        check("empty after all deletes", pqueue_is_empty(&pq), 1);
        check("delete_min on empty is EMPTY",
              pqueue_delete_min(&pq, &v, &p), PQ_EMPTY);
        /* Ties leave in arrival order. */
        check("enqueue(801,2) ok", pqueue_enqueue(&pq, 801, 2), PQ_OK);
        check("enqueue(802,2) ok", pqueue_enqueue(&pq, 802, 2), PQ_OK);
        check("tied delete is 801 first",
              (pqueue_delete_min(&pq, &v, &p) == PQ_OK) ? v : -999, 801);
        check("tied delete is 802 next",
              (pqueue_delete_min(&pq, &v, &p) == PQ_OK) ? v : -999, 802);
    }

    if (failures == 0) {
        printf("\nAll visible tests passed.\n");
        return 0;
    }
    printf("\n%d visible test(s) FAILED.\n", failures);
    return 1;
}
