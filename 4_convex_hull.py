import matplotlib.pyplot as plt
import pandas as pd
import numpy as np




# algorytm Jarvisa
def jarvis(points):
    def cross_product(p, q, r):
        return (q[0] - p[0]) * (r[1] - q[1]) - (q[1] - p[1]) * (r[0] - q[0])

    hull = []
    start = min(points)
    hull.append(start)
    current = start
    while True:
        next_point = points[0]
        for point in points[1:]:
            if point == current:
                continue
            direction = cross_product(current, next_point, point)
            if (next_point == current) or (direction > 0) or ((direction == 0) and (np.linalg.norm(np.array(point) - np.array(current)) > np.linalg.norm(np.array(next_point) - np.array(current)))):
                next_point = point
        if next_point == start:
            break
        hull.append(next_point)
        current = next_point

    if hull[-1] != start:
        hull.append(start)

    return hull





# algorytm Grahama
def graham(points):
    def polar_angle(p0, p1):
        return np.arctan2(p1[1] - p0[1], p1[0] - p0[0])

    def dist(p0, p1):
        return np.linalg.norm(np.array(p1) - np.array(p0))

    def sort_points_by_polar_angle(points, anchor):
        return sorted(points, key=lambda x: (polar_angle(anchor, x), dist(anchor, x)))

    def orientation(p0, p1, p2):
        val = (p1[1] - p0[1]) * (p2[0] - p1[0]) - (p1[0] - p0[0]) * (p2[1] - p1[1])
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2

    if len(points) < 3:
        return points

    anchor = min(points)
    sorted_points = sort_points_by_polar_angle(points, anchor)
    stack = [anchor, sorted_points[0], sorted_points[1]]

    for point in sorted_points[2:]:
        while len(stack) > 1 and orientation(stack[-2], stack[-1], point) != 2:
            stack.pop()
        stack.append(point)

    if stack[-1] != anchor:
        stack.append(anchor)

    return stack





# wczytywanie z pliku .txt
def read_points_from_file(filename):
    with open(filename, 'r') as file:
        points = []
        num_points = int(file.readline())
        for _ in range(num_points):
            x, y = map(float, file.readline().split())
            points.append((x, y))
    return points

with open('/content/points1.txt', 'r') as file1:
    data = file1.read()

with open('/content/points2.txt', 'r') as file2:
    data = file2.read()

file1 = "points1.txt"
file2 = "points2.txt"






points1 = read_points_from_file(file1)
points2 = read_points_from_file(file2)

hull_jarvis_1 = jarvis(points1)
hull_graham_1 = graham(points1)

hull_jarvis_2 = jarvis(points2)
hull_graham_2 = graham(points2)
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(*zip(*points1), 'o', label='Points')
#plt.plot(*zip(*hull_jarvis_1), '--', label='Jarvis')
plt.plot(*zip(*hull_graham_1), '--', label='Graham')
plt.title('Points 1')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(*zip(*points2), 'o', label='Points')
plt.plot(*zip(*hull_jarvis_2), '--', label='Jarvis')
#plt.plot(*zip(*hull_graham_2), '--', label='Graham')
plt.title('Points 2')
plt.legend()

plt.tight_layout()
plt.show()

