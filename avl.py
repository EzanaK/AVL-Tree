import json
from typing import List

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key       : int,
                  word      : str,
                  leftchild,
                  rightchild):
        self.key        = key
        self.word      = word
        self.leftchild  = leftchild
        self.rightchild = rightchild

# DO NOT MODIFY!
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "key": node.key,
            "word": node.word,
            "l": (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr,indent = 2)

# insert
# For the tree rooted at root, insert the given key,word pair and then balance as per AVL trees.
# The key is guaranteed to not be in the tree.
# Return the root.
def insert(root: Node, key: int, word: str) -> Node:
    new_node = Node(key=key, word=word, leftchild=None, rightchild=None)
    if root == None:
        return new_node
    cur = root
    ancestors = []
    while cur:
        if key < cur.key:
            if cur.leftchild:
                ancestors.append(cur)
                cur = cur.leftchild
            else:
                cur.leftchild = new_node
                break
        else:
            if cur.rightchild:
                ancestors.append(cur)
                cur = cur.rightchild
            else:
                cur.rightchild = new_node
                break
    while len(ancestors) > 0:
        ancestor: Node = ancestors.pop()
        if not is_balanced(ancestor):
            if len(ancestors) > 0:
                parent: Node = ancestors.pop()
                if ancestor.key < parent.key:
                    parent.leftchild = balance(ancestor)
                else:
                    parent.rightchild = balance(ancestor)
                break
            return balance(ancestor)
    return root

# Returns True if node is balanced, False otherwise
def is_balanced(node:Node) -> bool:
    if abs(height(node.rightchild) - height(node.leftchild)) > 1:
        return False
    else:
        return True

# Returns the height of a node
def height(node:Node) -> int:
    if node == None:
        return -1
    return 1 + max(height(node.leftchild), height(node.rightchild))

# Balances node to satisfy AVL conidtion
def balance(node:Node) -> Node:
    if is_left_left_heavy(node):
        return right_rotate(node)
    elif is_left_right_heavy(node):
        return left_right_rotate(node)
    elif is_right_right_heavy(node):
        return left_rotate(node)
    elif is_right_left_heavy(node):
        return right_left_rotate(node)

# Returns True if node is left-left heavy
def is_left_left_heavy(node:Node) -> bool:
    if height(node.leftchild) > height(node.rightchild):
        left_child: Node = node.leftchild
        if height(left_child.leftchild) > height(left_child.rightchild):
            return True
    return False

# Returns True if node is left-right heavy
def is_left_right_heavy(node:Node) -> bool:
    if height(node.leftchild) > height(node.rightchild):
        left_child: Node = node.leftchild
        if height(left_child.rightchild) > height(left_child.leftchild):
            return True
    return False

# Returns True if node is right-right heavy
def is_right_right_heavy(node:Node) -> bool:
    if height(node.rightchild) > height(node.leftchild):
        right_child: Node = node.rightchild
        if height(right_child.rightchild) > height(right_child.leftchild):
            return True
    return False

# Returns True if node is right-left heavy
def is_right_left_heavy(node:Node) -> bool:
    if height(node.rightchild) > height(node.leftchild):
        right_child: Node = node.rightchild
        if height(right_child.leftchild) > height(right_child.rightchild):
            return True
    return False

# Performs a right rotation on node
def right_rotate(node:Node) -> Node:
    left_child: Node = node.leftchild
    left_right_subtree = left_child.rightchild
    left_child.rightchild = node
    node.leftchild = left_right_subtree
    return left_child

# Performs a left-right rotation on node
def left_right_rotate(node:Node) -> Node:
    node.leftchild = left_rotate(node.leftchild)
    return right_rotate(node)

# Performs a left rotation on node
def left_rotate(node:Node) -> Node:
    right_child: Node = node.rightchild
    right_left_subtree = right_child.leftchild
    right_child.leftchild = node
    node.rightchild = right_left_subtree
    return right_child

# Performs a right-left rotation on node
def right_left_rotate(node:Node) -> Node:
    node.rightchild = right_rotate(node.rightchild)
    return left_rotate(node)

# bulkInsert
# The parameter items should be a list of pairs of the form [key,word] where key is an integer and word is a string.
# For the tree rooted at root, first insert all of the [key,word] pairs as if the tree were a standard BST, with no balancing.
# Then do a preorder traversal of the [key,word] pairs and use this traversal to build a new tree using AVL insertion.
# Return the root
def bulkInsert(root: Node, items: List) -> Node:
    # Standard BST insertion
    i = 0
    if root == None:
        root = Node(key=int(items[i][0]), word=items[i][1], leftchild=None, rightchild=None)
        i += 1
    while i < len(items):
        cur = root
        node: Node = Node(key=int(items[i][0]), word=items[i][1], leftchild=None, rightchild=None)
        while cur:
            if node.key < cur.key:
                if cur.leftchild:
                    cur = cur.leftchild
                else:
                    cur.leftchild = node
                    break
            else:
                if cur.rightchild:
                    cur = cur.rightchild
                else:
                    cur.rightchild = node
                    break
        i += 1

    # Get preorder traversal
    preorder_traversal_list: List[Node] = get_preorder_traversal(root)

    # Build AVL tree
    new_root = None
    i = 0
    for node in preorder_traversal_list:
        new_root = insert(root=new_root, key=node.key, word=node.word)
    return new_root

def get_preorder_traversal(root:Node) -> List[Node]:
    lst = []
    if root:
        lst.append(root)
        lst.extend(get_preorder_traversal(root.leftchild))
        lst.extend(get_preorder_traversal(root.rightchild))
    return lst

# bulkDelete
# The parameter keys should be a list of keys.
# For the tree rooted at root, first tag all the corresponding nodes (however you like),
# Then do a preorder traversal of the [key,word] pairs, ignoring the tagged nodes,
# and use this traversal to build a new tree using AVL insertion.
# Return the root.
def bulkDelete(root: Node, keys: List[int]) -> Node:
    # Get preorder traversal
    preorder_traversal_list = get_preorder_traversal(root)

    # Build AVL tree
    new_root = None
    i = 0
    for node in preorder_traversal_list:
        if node.key not in keys:
            new_root = insert(root=new_root, key=node.key, word=node.word)        
    return new_root

# search
# For the tree rooted at root, calculate the list of keys on the path from the root to the search_key,
# including the search key, and the word associated with the search_key.
# Return the json stringified list [key1,key2,...,keylast,word] with indent=2.
# If the search_key is not in the tree return a word of None.
def search(root: Node, search_key: int) -> str:
    lst = []
    cur = root
    while cur and cur.key != search_key:
        lst.append(cur.key)
        if search_key < cur.key:
            cur = cur.leftchild
        else:
            cur = cur.rightchild 
    if cur.key == search_key:
        lst.append(search_key)
        lst.append(cur.word)
        return json.dumps(lst,indent=2)
    else:
        return json.dumps(None,indent=2)

# replace
# For the tree rooted at root, replace the word corresponding to the key search_key by replacement_word.
# The search_key is guaranteed to be in the tree.
# Return the root
def replace(root: Node, search_key: int, replacement_word:str) -> None:
    cur = root
    while cur.key != search_key:
        if search_key < cur.key:
            cur = cur.leftchild
        else:
            cur = cur.rightchild
    cur.word = replacement_word
    return root