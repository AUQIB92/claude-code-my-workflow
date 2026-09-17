/*
 * queue.h — the Queue ADT contracts for Week 5 (Queues): P5 + P6.
 *
 * The contract says WHAT each function must do, not HOW the array is laid
 * out. This header is given to you; do not change it. Your job is to provide
 * every function below in queue.c (start from starter_queue.c).
 *
 * Two structures, matching the lecture (deck: Week 5, Sections 2 and 4):
 *
 *   P5 — CQueue: a circular buffer of ints using the COURSE CONVENTION
 *   (deck Section 2): a live-item `count` distinguishes full from empty, so
 *   the ring holds all QUEUE_MAX items. Indices advance with modular
 *   arithmetic: rear = (rear + 1) % QUEUE_MAX on enqueue, front =
 *   (front + 1) % QUEUE_MAX on dequeue. QUEUE_MAX is 8, the capacity of the
 *   ring figure drawn in lecture — small enough that wraparound is two
 *   operations away, never a hundred.
 *
 *   P6 — PQueue: an UNORDERED array priority queue (deck Section 4, first
 *   row of the cost table): enqueue appends at the end in O(1) worst case;
 *   peek_min/delete_min scan all live priorities in O(n) worst case and
 *   return the SMALLEST priority number first (priority 0 runs before
 *   priority 9, as in lecture). Ties — equal priorities — leave in arrival
 *   order: the earliest-inserted of the tied items leaves first (FIFO among
 *   equals). delete_min closes the gap so the live items always sit in
 *   data[0..size-1] with no holes.
 *
 * Unlike the lecture slides — which return -1 on dequeue errors to keep the
 * slide readable — every fallible function here reports an explicit status
 * code. A -1 sentinel cannot distinguish "the queue held -1" from "the
 * queue was empty"; the status codes below can. Using them correctly is part
 * of the grade (same discipline as Week 3's stack).
 */

#ifndef QUEUE_H
#define QUEUE_H

#define QUEUE_MAX 8    /* circular-buffer capacity (P5); holds all 8 items */
#define PQUEUE_MAX 32  /* unordered priority-queue capacity (P6) */

/* ------------------------------------------------------------------ */
/* P5: circular queue (count version)                                  */
/* ------------------------------------------------------------------ */

/* Status codes for the circular queue operations. */
typedef enum {
    CQ_OK = 0,    /* the operation succeeded */
    CQ_FULL = 1,  /* enqueue (or display-write) refused: count == QUEUE_MAX */
    CQ_EMPTY = 2  /* dequeue/front on an empty queue (count == 0) */
} CQStatus;

typedef struct {
    int data[QUEUE_MAX];
    int front;  /* index of the next item to dequeue (0-based) */
    int rear;   /* index of the most recently enqueued item; -1 when empty */
    int count;  /* number of live items; 0 means empty, QUEUE_MAX full */
} CQueue;

/*
 * cqueue_init: reset q to empty (count 0, front 0, rear -1). Call once
 * before any other operation on q.
 */
void cqueue_init(CQueue *q);

/*
 * cqueue_is_empty: return 1 if q holds no items (count == 0), else 0.
 * cqueue_is_full: return 1 if q holds QUEUE_MAX items, else 0.
 * cqueue_size: return the number of live items in q (0 when empty).
 * The honest full test is count == QUEUE_MAX — never front == rear, which
 * also fires on an empty ring (deck Section 2).
 */
int cqueue_is_empty(const CQueue *q);
int cqueue_is_full(const CQueue *q);
int cqueue_size(const CQueue *q);

/*
 * cqueue_enqueue: append x at the rear (rear = (rear + 1) % QUEUE_MAX,
 * count++).
 *   - return CQ_OK when the queue is not full.
 *   - return CQ_FULL and change nothing when count == QUEUE_MAX.
 */
CQStatus cqueue_enqueue(CQueue *q, int x);

/*
 * cqueue_dequeue: remove the front item and store it in *out
 * (front = (front + 1) % QUEUE_MAX, count--).
 *   - return CQ_OK when the queue is not empty.
 *   - return CQ_EMPTY and change nothing (neither the queue nor *out)
 *     when the queue is empty.
 *   - out may be NULL, meaning "discard the dequeued value".
 */
CQStatus cqueue_dequeue(CQueue *q, int *out);

/*
 * cqueue_front: copy the front item into *out WITHOUT removing it.
 *   - return CQ_OK when the queue is not empty.
 *   - return CQ_EMPTY and leave *out unchanged when empty.
 *   - out may be NULL, meaning "check emptiness only".
 */
CQStatus cqueue_front(const CQueue *q, int *out);

/*
 * cqueue_display: copy the live items, front-to-rear, into out[0..count-1]
 * (the Lab P5 "display", made testable: instead of printing, the caller
 * supplies the buffer). Returns the number of items written.
 *   - return the live count (0 for an empty queue) on success.
 *   - return -1 and write nothing when q is NULL, out is NULL, or out_cap
 *     < count (the buffer cannot hold the queue — the caller must retry
 *     with room for at least cqueue_size(q) ints).
 * A display must never disturb the queue: front, rear, and count are
 * unchanged afterwards.
 */
int cqueue_display(const CQueue *q, int *out, int out_cap);

/* ------------------------------------------------------------------ */
/* P6: unordered priority queue (array)                                */
/* ------------------------------------------------------------------ */

/*
 * One queued job: value is the payload (a job id), priority is its urgency.
 * SMALLER priority numbers leave FIRST (0 beats 9). Priorities may be any
 * int, including negatives (an interrupt at -2 outranks everything >= 0).
 */
typedef struct {
    int value;
    int priority;
} PQItem;

/* Status codes for the priority queue operations. */
typedef enum {
    PQ_OK = 0,    /* the operation succeeded */
    PQ_FULL = 1,  /* enqueue refused: size == PQUEUE_MAX */
    PQ_EMPTY = 2  /* peek_min/delete_min on an empty queue (size == 0) */
} PQStatus;

typedef struct {
    PQItem data[PQUEUE_MAX];
    int size;  /* number of live items in data[0..size-1] */
} PQueue;

/*
 * pqueue_init: reset q to empty (size 0). Call once before any other
 * operation on q.
 */
void pqueue_init(PQueue *q);

/*
 * pqueue_is_empty: return 1 if q holds no items, else 0.
 * pqueue_is_full: return 1 if q holds PQUEUE_MAX items, else 0.
 * pqueue_size: return the number of live items in q (0 when empty).
 */
int pqueue_is_empty(const PQueue *q);
int pqueue_is_full(const PQueue *q);
int pqueue_size(const PQueue *q);

/*
 * pqueue_enqueue: append (value, priority) at the end of the live region.
 *   - return PQ_OK when the queue is not full.
 *   - return PQ_FULL and change nothing when size == PQUEUE_MAX.
 */
PQStatus pqueue_enqueue(PQueue *q, int value, int priority);

/*
 * pqueue_peek_min: copy the most urgent item into *value_out / *priority_out
 * WITHOUT removing it. "Most urgent" = smallest priority number; ties go to
 * the earliest-inserted of the tied items.
 *   - return PQ_OK when the queue is not empty.
 *   - return PQ_EMPTY and leave both outs unchanged when empty.
 *   - either out pointer may be NULL, meaning "do not report that half".
 */
PQStatus pqueue_peek_min(const PQueue *q, int *value_out, int *priority_out);

/*
 * pqueue_delete_min: remove the most urgent item (same choice rule as
 * peek_min), store it in *value_out / *priority_out, and close the gap so
 * the survivors sit packed in data[0..size-1].
 *   - return PQ_OK when the queue is not empty.
 *   - return PQ_EMPTY and change nothing (neither the queue nor the outs)
 *     when empty.
 *   - either out pointer may be NULL, meaning "discard that half".
 */
PQStatus pqueue_delete_min(PQueue *q, int *value_out, int *priority_out);

#endif /* QUEUE_H */
