from Node import Node

# Represents the frontier list. This is using a binary min heap data structure.
class Frontier:
    # Initialises the frontier with a single item array of the initial node
    def __init__(self, initial_node):
        self.arr = [initial_node]

    # Single node into the frontier
    def insert(self, node):
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
        try:
            nodes = list(nodes)

            for node in nodes:
                self.insert(node)

        except ValueError:
            print("'nodes' is not of the type list.")

    def isEmpty(self):
        return len(self.arr) == 0

    # removes the top element, arr[0], from the frontier list and returns it
    def remove(self):
        return self.arr.pop(0)

    def getNodes(self):
        return self.arr

# Helper functions
def getParent(i):
    return (i - 1) // 2

def getLeftChild(i):
    return (2 * i) + 1

def getRightChild(i):
    return (2 * i) + 2