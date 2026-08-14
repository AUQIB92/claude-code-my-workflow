/*
 * intbuf.h — the IntBuffer ADT contract (Week 1 Lab: Pointer and
 * dynamic-memory warm-up)
 *
 * The contract says WHAT you can do, not HOW it is stored. This header is
 * given to you; do not change it. Your job is to provide the four
 * operations below using a SINGLE growable heap block, and to exercise the
 * complete allocation family the lecture covered: malloc, calloc, realloc,
 * and free.
 *
 * The struct is exposed (not opaque) on purpose, so you can inspect
 * `size` and `capacity` directly with `->`, the same arrow notation the
 * lecture used for `struct node`.
 */

#ifndef INTBUF_H
#define INTBUF_H

#include <stddef.h> /* size_t */

typedef struct {
    int    *data;     /* heap block holding `capacity` ints              */
    size_t  size;      /* ints actually pushed; 0 <= size <= capacity     */
    size_t  capacity;  /* ints the current block can hold                 */
} IntBuffer;

/*
 * buf_create: allocate a new IntBuffer with room for initial_capacity
 * ints, all zero-initialized.
 *   - if initial_capacity == 0, treat it as 1 (minimum working capacity)
 *   - allocate the IntBuffer struct itself with malloc
 *   - allocate the capacity-int data block with calloc, so every slot
 *     starts at 0 even before anything is pushed
 *   - if either allocation fails, free whatever was already allocated
 *     and return NULL --- never leak a partial buffer
 */
IntBuffer *buf_create(size_t initial_capacity);

/*
 * buf_push: append value at index buf->size.
 *   - if buf->size == buf->capacity (the block is full), grow the data
 *     block FIRST by calling realloc to exactly DOUBLE the capacity
 *     (1 -> 2 -> 4 -> 8 -> ...), THEN write the new value
 *   - if realloc fails, buf is left completely unchanged (same block,
 *     same size, same capacity, still valid) and the function returns -1
 *   - on success, buf->size increases by 1 and the function returns 0
 */
int buf_push(IntBuffer *buf, int value);

/*
 * buf_get: read the value at index into *out.
 *   - returns 0 and writes *out when 0 <= index < buf->size
 *   - returns -1 and leaves *out untouched when index >= buf->size
 *     (never reads past what has actually been pushed)
 */
int buf_get(const IntBuffer *buf, size_t index, int *out);

/*
 * buf_free: return every heap block owned by buf to the system.
 *   - frees the data block, then the IntBuffer struct itself
 *   - must not crash when called with buf == NULL (no-op)
 */
void buf_free(IntBuffer *buf);

#endif /* INTBUF_H */
