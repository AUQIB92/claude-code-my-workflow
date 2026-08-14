/*
 * reference_solution.c — INSTRUCTOR-ONLY reference implementation of the
 * IntBuffer ADT declared in intbuf.h.
 *
 * NEVER ship this file to students, and NEVER sync it to docs/ (see
 * single-source-of-truth.md / the coding-assignment skill's file-split
 * discipline). Used only to build the hidden test suite's oracle and to
 * verify the autograder harness end-to-end before release.
 */

#include <stdlib.h>
#include "intbuf.h"

IntBuffer *buf_create(size_t initial_capacity)
{
    if (initial_capacity == 0) {
        initial_capacity = 1;
    }

    IntBuffer *buf = malloc(sizeof(IntBuffer));
    if (buf == NULL) {
        return NULL;
    }

    buf->data = calloc(initial_capacity, sizeof(int));
    if (buf->data == NULL) {
        free(buf);
        return NULL;
    }

    buf->size = 0;
    buf->capacity = initial_capacity;
    return buf;
}

int buf_push(IntBuffer *buf, int value)
{
    if (buf->size == buf->capacity) {
        size_t new_capacity = buf->capacity * 2;
        int *bigger = realloc(buf->data, new_capacity * sizeof(int));
        if (bigger == NULL) {
            /* buf->data, buf->size, buf->capacity are all untouched. */
            return -1;
        }
        buf->data = bigger;
        buf->capacity = new_capacity;
    }

    buf->data[buf->size] = value;
    buf->size = buf->size + 1;
    return 0;
}

int buf_get(const IntBuffer *buf, size_t index, int *out)
{
    if (index >= buf->size) {
        return -1;
    }
    *out = buf->data[index];
    return 0;
}

void buf_free(IntBuffer *buf)
{
    if (buf == NULL) {
        return;
    }
    free(buf->data);
    free(buf);
}
