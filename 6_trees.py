import random
import matplotlib.pyplot as plt
import sys
import psutil
import networkx as nx





class RangeTree2D:
    def __init__(self, points):
        self.root = self.construct_tree(points)

    class Node:
        def __init__(self, point):
            self.point = point
            self.left = None
            self.right = None

    def construct_tree(self, points):
        if not points:
            return None
        points.sort(key=lambda x: x[0])
        mid = len(points) // 2
        node = self.Node(points[mid])
        node.left = self.construct_tree(points[:mid])
        node.right = self.construct_tree(points[mid + 1:])
        return node

    def query_range(self, node, x1, x2, y1, y2):
        if not node:
            return 0
        if node.point[0] < x1:
            return self.query_range(node.right, x1, x2, y1, y2)
        elif node.point[0] > x2:
            return self.query_range(node.left, x1, x2, y1, y2)
        else:
            if y1 <= node.point[1] <= y2:
                return 1 + self.query_range(node.left, x1, x2, y1, y2) + self.query_range(node.right, x1, x2, y1, y2)
            else:
                return self.query_range(node.left, x1, x2, y1, y2) + self.query_range(node.right, x1, x2, y1, y2)




def generate_2d_points(num_points):
    return [(random.randint(0, 100), random.randint(0, 100)) for _ in range(num_points)]

def visualize_2d(points, x1, x2, y1, y2):
    plt.figure(figsize=(10, 6))
    plt.plot([point[0] for point in points], [point[1] for point in points], 'bo')
    plt.axvline(x=x1, color='r', linestyle='--')
    plt.axvline(x=x2, color='r', linestyle='--')
    plt.axhline(y=y1, color='r', linestyle='--')
    plt.axhline(y=y2, color='r', linestyle='--')
    plt.title("2D range query")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()





def visualize_range_tree_as_graph(G, node, parent_point=None):
    if not node:
        return

    G.add_node(node.point)

    if parent_point:
        G.add_edge(parent_point, node.point)

    visualize_range_tree_as_graph(G, node.left, node.point)
    visualize_range_tree_as_graph(G, node.right, node.point)

def visualize_2d_range_tree(root):
    G = nx.Graph()
    visualize_range_tree_as_graph(G, root)

    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray', linewidths=1, arrows=False)
    plt.title("2D Range Tree")
    plt.show()




def test1(num_points):
    points_2d = generate_2d_points(num_points)
    rt_2d = RangeTree2D(points_2d)
    visualize_2d_range_tree(rt_2d.root)

test1(20)



def test2(num_points):
    points_2d = generate_2d_points(num_points)
    rt_2d = RangeTree2D(points_2d)
    x1, x2, y1, y2 = 20, 80, 20, 80
    result = rt_2d.query_range(rt_2d.root, x1, x2, y1, y2)
    print("number of points in range [{}-{}, {}-{}]: {}".format(x1, x2, y1, y2, result))

    memory_usage = psutil.Process().memory_info().rss
    memory_usage_mb = memory_usage / 1024 / 1024
    print("memory usage for {} points: {} MB".format(num_points, memory_usage_mb))

    visualize_2d(points_2d, x1, x2, y1, y2)

test2(20)
test2(50)
test2(1000)
test2(10000)
test2(100000)
test2(1000000)




