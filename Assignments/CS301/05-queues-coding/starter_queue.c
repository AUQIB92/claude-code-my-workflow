/*
 * queue.c — your implementation of Week 5's Queue ADTs (P5 circular queue +
 * P6 unordered priority queue).
 *
 * Fill in every function declared in queue.h. Do not change queue.h. Do not
 * add any global/static mutable state — each function must work through the
 * CQueue/PQueue pointer it is given.
 *
 * Compile check (from the assignment directory):
 *   gcc -Wall -Wextra -c queue.c -o queue.o
 *
 * Reminders from lecture:
 *   - P5 is the COUNT version: empty iff count == 0, full iff
 *     count == QUEUE_MAX. Never test full as front == rear — that test also
 *     fires on an empty ring, and the hidden suite checks a wrapped state
 *     where the two coincide on purpose.
 *   - Advance indices modulo the capacity: rear = (rear + 1) % QUEUE_MAX on
 *     enqueue, front = (front + 1) % QUEUE_MAX on dequeue. Init sets
 *     front = 0, rear = -1, count = 0, so the first enqueue lands at 0.
 *   - P6 is UNORDERED: enqueue appends at data[size] in O(1); peek_min and
 *     delete_min scan every live item in O(n) and pick the smallest priority
 *     number, earliest-inserted wins ties. delete_min must close the gap —
 *     the survivors stay packed in data[0..size-1].
 *   - Errors use the explicit status codes, never a -1 sentinel: pushing the
 *     VALUE -1 (or priority -1) and getting it back must succeed with *_OK.
 */

#include "queue.h"

/* ---------------- P5: circular queue ---------------- */

void cqueue_init(CQueue *q)
{
    /* TODO: set q->front = 0, q->rear = -1, q->count = 0. */
    (void)q;
}

int cqueue_is_empty(const CQueue *q)
{
    /* TODO: return 1 when q->count == 0, else 0. */
    (void)q;
    return 1;
}

int cqueue_is_full(const CQueue *q)
{
    /* TODO: return 1 when q->count == QUEUE_MAX, else 0. */
    (void)q;
    return 0;
}

int cqueue_size(const CQueue *q)
{
    /* TODO: return q->count. */
    (void)q;
    return 0;
}

CQStatus cqueue_enqueue(CQueue *q, int x)
{
    /* TODO: if full (q->count == QUEUE_MAX) return CQ_FULL and change
       nothing; else advance q->rear modulo QUEUE_MAX, store x, count++. */
    (void)q; (void)x;
    return CQ_FULL;
}

CQStatus cqueue_dequeue(CQueue *q, int *out)
{
    /* TODO: if empty return CQ_EMPTY and change nothing; else read
       data[q->front] into *out (unless out is NULL), advance q->front
       modulo QUEUE_MAX, count--, return CQ_OK. */
    (void)q; (void)out;
    return CQ_EMPTY;
}

CQStatus cqueue_front(const CQueue *q, int *out)
{
    /* TODO: if empty return CQ_EMPTY and leave *out unchanged; else copy
       data[q->front] into *out (unless out is NULL) WITHOUT moving front. */
    (void)q; (void)out;
    return CQ_EMPTY;
}

int cqueue_display(const CQueue *q, int *out, int out_cap)
{
    /* TODO: validate (q/out NULL, or out_cap < q->count -> return -1 and
       write nothing); else copy the live items front-to-rear into
       out[0..count-1] WITHOUT touching front/rear/count, and return count. */
    (void)q; (void)out; (void)out_cap;
    return -1;
}

/* ---------------- P6: unordered priority queue ---------------- */

void pqueue_init(PQueue *q)
{
    /* TODO: set q->size = 0. */
    (void)q;
}

int pqueue_is_empty(const PQueue *q)
{
    /* TODO: return 1 when q->size == 0, else 0. */
    (void)q;
    return 1;
}

int pqueue_is_full(const PQueue *q)
{
    /* TODO: return 1 when q->size == PQUEUE_MAX, else 0. */
    (void)q;
    return 0;
}

int pqueue_size(const PQueue *q)
{
    /* TODO: return q->size. */
    (void)q;
    return 0;
}

PQStatus pqueue_enqueue(PQueue *q, int value, int priority)
{
    /* TODO: if full (q->size == PQUEUE_MAX) return PQ_FULL and change
       nothing; else append {value, priority} at data[q->size], size++. */
    (void)q; (void)value; (void)priority;
    return PQ_FULL;
}

PQStatus pqueue_peek_min(const PQueue *q, int *value_out, int *priority_out)
{
    /* TODO: if empty return PQ_EMPTY and leave the outs unchanged; else scan
       data[0..size-1] for the smallest priority (ties -> smallest index),
       report through the non-NULL outs, WITHOUT removing anything. */
    (void)q; (void)value_out; (void)priority_out;
    return PQ_EMPTY;
}

PQStatus pqueue_delete_min(PQueue *q, int *value_out, int *priority_out)
{
    /* TODO: if empty return PQ_EMPTY and change nothing; else find the min
       exactly as in peek_min, report through the non-NULL outs, close the
       gap (shift the tail left one slot), size--, return PQ_OK. */
    (void)q; (void)value_out; (void)priority_out;
    return PQ_EMPTY;
}
