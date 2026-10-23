from helpers.Node import Node


# Represents the frontier list. This is using a binary min heap data structure.
class Frontier:
    """
        A class representing a Frontier.

        Attributes:
            arr (list): The frontier list which behaves as a binary min tree.
    """

    def __init__(self, initial_node):
        """
        Initialises a Frontier object.

        Parameters:
            initial_node (Node): The first node in the frontier.
        """

        self.arr = [initial_node]

    def insert(self, node):
        """
        Appends a single node into the frontier, and reorders accordingly.

        Parameters:
            node (Node): The node to be inserted into the frontier.
        """

        try:
            if not isinstance(node, Node):
                raise ValueError()
        except ValueError:
            print("'node' is not of the class 'Node'.")

        # add node to the end of the list
        self.arr.append(node)

        i = len(self.arr) - 1

        # work from the bottom of nodes up and rearrange given the new value
        while i > 0:
            parent_index = getParent(i)

            new_cost = self.arr[i].getF()
            parent_cost = self.arr[parent_index].getF()

            if new_cost < parent_cost:
                self.arr[i], self.arr[parent_index] = self.arr[parent_index], self.arr[i]

                # swap the indexes so we are still checking our new value
                i = parent_index
            else:
                break

    # Inserts a list of nodes into the frontier. These nodes will be ordered by their priority
    def insertPriority(self, nodes):
        """
        Inserts a list of nodes into the frontier.

        Parameters:
            nodes (list): The nodes to be appended to the frontier.
        """

        try:
            nodes = list(nodes)

            for node in nodes:
                self.insert(node)

        except ValueError:
            print("'nodes' is not of the type list.")

    # *************** Helper functions ***************#

    def isEmpty(self):
        """
        States if the frontier is empty.

        Returns:
            bool
        """

        return len(self.arr) == 0

    def remove(self):
        """
        Returns:
            Node: The top element of the frontier
        """

        return self.arr.pop(0)

    def getNodes(self):
        """
        Returns:
            list: The frontier nodes
        """

        return self.arr

def getParent(i):
    """
    Parameters:
        i (int): The index of the current frontier node.

    Returns:
        int: The index of the current frontier node's parent node.
    """

    return (i - 1) // 2


def getLeftChild(i):
    """
    Parameters:
        i (int): The index of the current frontier node.

    Returns:
        int: The index of the current frontier node's left child.
    """

    return (2 * i) + 1


def getRightChild(i):
    """
    Parameters:
        i (int): The index of the current frontier node.

    Returns:
        int: The index of the current frontier node's right child.
    """

    return (2 * i) + 2
