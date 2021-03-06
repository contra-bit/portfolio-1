/**
 * @brief An implementation of an AVL tree.
 */

#pragma once

#include "binary_tree.h"

// One node of the AVL tree.
typedef struct {
	void *data; // The data contained inside this node.
	int balanceFactor; // The balance factor of this node.
} AVLTree_Node_t;

// An AVL tree.
typedef BinaryTree_Tree_t AVLTree_Tree_t;

/*
 * @brief Create an AVL tree.
 * @param compareData A function used to compare any two of the tree's nodes'
 *      data items. Should return a number less than 0 if `data1` is less than
 *      `data2`, 0 if they're equal, and a number greater than 0 otherwise.
 * @param create A function to deallocate the data stored in this tree's
 * @return A pointer to the newly allocated tree.
*/
AVLTree_Tree_t *AVLTree_create(
	void (*freeData)(void *data),
	int (*compareData)(const void *data1, const void *data2)
);

/*
 * @brief Deallocate an AVL tree.
 * @param tree If the tree has any nodes, they will be deallocated, and their
 *      `data` members freed with `tree->freeData()`. It will be `free()`d
 *      afterwards.
*/
void AVLTree_free(AVLTree_Tree_t *tree);

/*
 * @brief Insert a data item into a tree.
 * @param tree The tree to insert the item into; need not have any items.
 * @param data The data item to insert; must be usable by
 *      `tree->compareData()`. If `tree` has a `size` of 0, then `data` will be
 *      inserted in its `root`.
*/
void AVLTree_insert(AVLTree_Tree_t *tree, void *data);
