import sys
import math

B = 4  # Branching factor

def main(points_list):
    # Initialize an R-tree and insert each point from points_list
    rtree = RTree()
    for point in points_list:
        rtree.insert(rtree.root, point)
    return rtree


class Node:
    def __init__(self):
        # Initialize node properties, including MBR and empty lists for children/data points
        self.id = 0
        self.child_nodes = []
        self.data_points = []
        self.parent = None
        self.MBR = {'x1': -1, 'y1': -1, 'x2': -1, 'y2': -1}

    def perimeter(self):
        # Calculate half-perimeter based on MBR dimensions
        return (self.MBR['x2'] - self.MBR['x1']) + (self.MBR['y2'] - self.MBR['y1'])

    def is_overflow(self):
        # Check if node exceeds allowed count of points/child nodes
        return len(self.data_points if self.is_leaf() else self.child_nodes) > B

    def is_root(self):
        # Node is root if it has no parent
        return self.parent is None

    def is_leaf(self):
        # Node is a leaf if it has no child nodes
        return len(self.child_nodes) == 0


class RTree:
    def __init__(self):
        # Create the R-tree with a root node
        self.root = Node()

    def insert(self, node, point):
        # Insert point into the appropriate node, handling overflow if needed
        if node.is_leaf():
            self.add_data_point(node, point)
            if node.is_overflow():
                self.handle_overflow(node)
        else:
            target_child = self.select_subtree(node, point)
            self.insert(target_child, point)
            self.update_mbr(target_child)

    def select_subtree(self, node, point):
        # Find child node that minimizes MBR expansion for point insertion
        min_increase = sys.maxsize
        best_child = None
        for child in node.child_nodes:
            increase = self.perimeter_increase(child, point)
            if increase < min_increase:
                min_increase, best_child = increase, child
        return best_child

    def perimeter_increase(self, node, point):
        # Calculate perimeter increase if point is added to node's MBR
        x1, x2, y1, y2 = node.MBR['x1'], node.MBR['x2'], node.MBR['y1'], node.MBR['y2']
        new_x1, new_x2 = min(x1, point['x']), max(x2, point['x'])
        new_y1, new_y2 = min(y1, point['y']), max(y2, point['y'])
        return (new_x2 - new_x1 + new_y2 - new_y1) - node.perimeter()

    def handle_overflow(self, node):
        # Split node if it exceeds capacity and adjust tree structure if needed
        split1, split2 = self.split(node)
        if node.is_root():
            new_root = Node()
            self.add_child(new_root, split1)
            self.add_child(new_root, split2)
            self.root = new_root
            self.update_mbr(new_root)
        else:
            parent = node.parent
            parent.child_nodes.remove(node)
            self.add_child(parent, split1)
            self.add_child(parent, split2)
            if parent.is_overflow():
                self.handle_overflow(parent)

    def split(self, node):
        # Divide a node into two nodes to handle overflow, aiming to minimize perimeter
        best_split1 = Node()
        best_split2 = Node()
        best_perimeter = sys.maxsize

        if node.is_leaf():
            m = len(node.data_points)
            splits = [
                sorted(node.data_points, key=lambda p: p['x']),
                sorted(node.data_points, key=lambda p: p['y'])
            ]
            for split in splits:
                for i in range(math.ceil(0.4 * B), m - math.ceil(0.4 * B) + 1):
                    s1, s2 = Node(), Node()
                    s1.data_points = split[:i]
                    s2.data_points = split[i:]
                    self.update_mbr(s1)
                    self.update_mbr(s2)
                    perimeter = s1.perimeter() + s2.perimeter()
                    if perimeter < best_perimeter:
                        best_perimeter = perimeter
                        best_split1, best_split2 = s1, s2
        else:
            m = len(node.child_nodes)
            splits = [
                sorted(node.child_nodes, key=lambda n: n.MBR['x1']),
                sorted(node.child_nodes, key=lambda n: n.MBR['y1']),
            ]
            for split in splits:
                for i in range(math.ceil(0.4 * B), m - math.ceil(0.4 * B) + 1):
                    s1, s2 = Node(), Node()
                    s1.child_nodes = split[:i]
                    s2.child_nodes = split[i:]
                    self.update_mbr(s1)
                    self.update_mbr(s2)
                    perimeter = s1.perimeter() + s2.perimeter()
                    if perimeter < best_perimeter:
                        best_perimeter = perimeter
                        best_split1, best_split2 = s1, s2

        for child in best_split1.child_nodes:
            child.parent = best_split1
        for child in best_split2.child_nodes:
            child.parent = best_split2

        return best_split1, best_split2

    def add_child(self, node, child):
        node.child_nodes.append(child)  # Add child nodes to the current parent (node) and update the MBRs. Used in handling overflows
        child.parent = node
        if child.MBR['x1'] < node.MBR['x1']:
            node.MBR['x1'] = child.MBR['x1']
        if child.MBR['x2'] > node.MBR['x2']:
            node.MBR['x2'] = child.MBR['x2']
        if child.MBR['y1'] < node.MBR['y1']:
            node.MBR['y1'] = child.MBR['y1']
        if child.MBR['y2'] > node.MBR['y2']:
            node.MBR['y2'] = child.MBR['y2']
    
    def add_data_point(self, node, data_point):  # Add data points and update the MBRs
        node.data_points.append(data_point)
        if data_point['x'] < node.MBR['x1']:
            node.MBR['x1'] = data_point['x']
        if data_point['x'] > node.MBR['x2']:
            node.MBR['x2'] = data_point['x']
        if data_point['y'] < node.MBR['y1']:
            node.MBR['y1'] = data_point['y']
        if data_point['y'] > node.MBR['y2']:
            node.MBR['y2'] = data_point['y']

    def update_mbr(self, node):  # Update MBRs when forming a new MBR. Used for checking combinations and updating the root
        x_list = []
        y_list = []
        if node.is_leaf():  # For leaf nodes, collect x and y values from data points
            x_list = [point['x'] for point in node.data_points]
            y_list = [point['y'] for point in node.data_points]
        else:  # For internal nodes, gather x and y values from children MBRs
            x_list = [child.MBR['x1'] for child in node.child_nodes] + [child.MBR['x2'] for child in node.child_nodes]
            y_list = [child.MBR['y1'] for child in node.child_nodes] + [child.MBR['y2'] for child in node.child_nodes]
        
        # Form the new MBR using the minimum and maximum x and y values
        new_mbr = {
            'x1': min(x_list),
            'x2': max(x_list),
            'y1': min(y_list),
            'y2': max(y_list)
        }
        node.MBR = new_mbr