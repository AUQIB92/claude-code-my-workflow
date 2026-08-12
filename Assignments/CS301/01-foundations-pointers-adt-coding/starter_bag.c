/*
 * bag.c — your implementation of the Bag ADT (Week 1)
 *
 * Fill in the four functions declared in bag.h. Use ONLY the linked-chain
 * representation: the bag is a chain of Node structs on the heap, reached
 * through a head pointer; the empty bag is NULL.
 *
 * Compile check (from the assignment directory):
 *   gcc -Wall -Wextra -c bag.c -o bag.o
 *
 * Requirements (from the lecture's pointer discipline):
 *   - malloc BEFORE you use a node; check the result against NULL
 *   - every malloc has a matching free; free every node on free_bag
 *   - never dereference a NULL pointer
 */

#include <stdlib.h>
#include "bag.h"

Node *bag_insert(Node *head, int x)
{
    /* TODO: allocate a new node, wire it at the front, return the new head. */
    return head;
}

int bag_member(const Node *head, int x)
{
    /* TODO: walk the chain; return 1 if any node's data equals x, else 0. */
    return 0;
}

int bag_size(const Node *head)
{
    /* TODO: count the nodes reachable from head; empty bag counts 0. */
    return 0;
}

void free_bag(Node *head)
{
    /* TODO: free every node in the chain; no-op when head is NULL. */
    (void)head;
}
