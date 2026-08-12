/*
 * bag.h — the Bag ADT contract (Week 1: Foundations, Pointers & ADTs)
 *
 * The contract says WHAT you can do, not HOW it is stored. This header is
 * given to you; do not change it. Your job is to provide the four operations
 * below using a singly-linked chain of nodes on the heap.
 *
 * A node is a small struct with an int and a pointer to the next node.
 * The bag is represented by a pointer to the first node ("head"); the empty
 * bag is the value NULL.
 */

#ifndef BAG_H
#define BAG_H

typedef struct node {
    int   data;
    struct node *next;
} Node;

/*
 * insert: add x to the bag.
 *   - allocate a new node on the heap with malloc
 *   - wire it at the FRONT of the chain (new node becomes head)
 *   - returns the new head
 *   - if malloc fails, returns the original head unchanged (bag unchanged)
 */
Node *bag_insert(Node *head, int x);

/*
 * member: return 1 if x is present in the bag, 0 otherwise.
 *   - walk the chain from head, comparing data fields
 */
int bag_member(const Node *head, int x);

/*
 * size: return how many items are in the bag.
 *   - count the nodes reachable from head
 *   - the empty bag has size 0
 */
int bag_size(const Node *head);

/*
 * free_bag: free every node in the chain.
 *   - must free ALL nodes reachable from head (no leaks)
 *   - must not crash when called on the empty bag (head == NULL)
 *   - does not return a value
 */
void free_bag(Node *head);

#endif /* BAG_H */
