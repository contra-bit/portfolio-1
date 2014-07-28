/*
	An implementation of a circular, singly-linked list.
*/

// A singly-linked node that composes an ::CSLList_t.
struct CSLNode {
	void *data; // The contained data.
	struct CSLNode *next; // The next node in the sequence.
};
typedef struct CSLNode CSLNode_t;

// A singly-linked-list.
typedef struct {
	int len; // The number of ::CSLNode_t inside the list.
	CSLNode_t *head; // The beginning of the list.
	// Function to deallocate the data stored inside this list's ::CSLNode_t.
	void (*freeData)(void *data);
} CSLList_t;

/*
	@brief Allocate a ::CSLList_t.

	@param freeData Function that will be used to deallocate the data contained
		inside the new list's nodes.

	@return The new list.
*/
CSLList_t *createCSLList(void (*freeData)(void *data));

/*
	@brief Deallocate a ::CSLList_t.

	@param list The list to be freed. All member nodes will also be
		deallocated.
*/
void freeCSLList(CSLList_t *list);

/*
	@brief Insert a new head ::CSLNode_t into a ::CSLList_t.

	@param list The list to insert a new head into.
	@param data The ::data of the new head.
*/
void insertCSLListHead(CSLList_t *list, void *data);

/*
	@brief Remove the head of a ::CSLList_t.

	@param list The list to remove the head from. The node following the
		current ::head becomes the list's new head. `list` may be of length 0.

	@return If `list` had a length greater than 0, return the ::data of the
		list's removed and deallocated head. Otherwise, `NULL`.
*/
void *removeCSLListHead(CSLList_t *list);

/*
	@brief Insert a ::CSLNode_t after another ::CSLNode_t in a ::CSLList_t.

	@param list The list to insert the new node into.
	@param node The node to insert a new node after.
	@param data The ::data of the new node.
*/
void insertAfterCSLNode(CSLList_t *list, CSLNode_t *node, void *data);

/*
	@brief Remove the ::CSLNode_t after another ::CSLNode_t in a ::CSLList_t.

	@param list The list to remove a node from.
	@param node The node preceding the node to be removed.

	@return The ::data of the removed node, which is itself deallocated.
*/
void *removeAfterCSLNode(CSLList_t *list, CSLNode_t *node);
void insertAtIndex(CSLList_t *list, int index, void *data);
void *removeAtIndex(CSLList_t *list, int index);
void *removeCSLNode(CSLList_t *list, CSLNode_t *node);

/*
	@brief Prints the contents of an ::CSLList_t.

	@param list The list whose ::CSLNode_t will be printed.
	@param nodeDataFmt Since ::CSLList_t is implemented to support arbitrary
		data-types by storing `void *` data inside its ::CSLNode_t, a
		format-string is needed to print its contents. The string should be a
		standard C format string (see `printf(3)`).
*/
void printCSLList(const CSLList_t *list, const char *nodeDataFmt);
