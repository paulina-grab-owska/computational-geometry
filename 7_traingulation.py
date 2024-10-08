import numpy as np
import matplotlib.pyplot as plt
from random import random
from math import sqrt

class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = (p1[0], p1[1])
        self.p2 = (p2[0], p2[1])
        self.p3 = (p3[0], p3[1])

    def calculate_circumcenter(self, display=True):
        ax, ay = self.p1[0], self.p1[1]
        bx, by = self.p2[0], self.p2[1]
        cx, cy = self.p3[0], self.p3[1]
        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        c_x = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
        c_y = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
        radius = sqrt((c_x - ax) ** 2 + (c_y - ay) ** 2)

        return (round(c_x, 5), round(c_y, 5)), round(radius, 5)

class Delaunay:
    def __init__(self, R=10):
        self.triangles = {}
        self.points = []
        self.triangle_id = 0
        self.eps = 0.0001
        self.R = R
        self.super_triangle = Triangle((0, R), (R * sqrt(3) / 2, -R / 2), (-R * sqrt(3) / 2, -R / 2))
        self.triangles[self.triangle_id] = Triangle((-R, R), (R, R), (R, -R))
        self.triangle_id += 1
        self.triangles[self.triangle_id] = Triangle((-R, R), (-R, -R), (R, -R))
        self.triangle_id += 1
        self.points.append((R, R))
        self.points.append((-R, R))
        self.points.append((R, -R))
        self.points.append((-R, -R))

    def point_exists(self, pt):
        for point in self.points:
            dist = sqrt((pt[0] - point[0]) ** 2 + (pt[1] - point[1]) ** 2)
            if dist < self.eps:
                return True
        return False

    def add_point(self, pt):
        if not self.point_exists(pt):
            self.points.append(pt)
            self.bad_triangles = {}
            list_keys = []
            for key in self.triangles:
                tri = self.triangles[key]
                if tri.calculate_circumcenter(display=False):
                    list_keys.append(key)
                    self.bad_triangles[key] = Triangle(tri.p1, tri.p2, tri.p3)

            polygone = self.find_enclosing_edges()

            for key in list_keys:
                del self.triangles[key]

            for edge in polygone:
                self.triangles[self.triangle_id] = Triangle(edge.p1, pt, edge.p2)
                self.triangle_id += 1

    def find_enclosing_edges(self):
        if not self.bad_triangles:
            return []
        polygone = []
        for key1, T1 in self.bad_triangles.items():
            global_flag = True
            for key2, T2 in self.bad_triangles.items():
                if key1 != key2:
                    dists = [
                        sqrt((T1.p1[0] - T2.p1[0]) ** 2 + (T1.p1[1] - T2.p1[1]) ** 2) +
                        sqrt((T1.p2[0] - T2.p2[0]) ** 2 + (T1.p2[1] - T2.p2[1]) ** 2),
                        sqrt((T1.p1[0] - T2.p2[0]) ** 2 + (T1.p1[1] - T2.p2[1]) ** 2) +
                        sqrt((T1.p2[0] - T2.p1[0]) ** 2 + (T1.p2[1] - T2.p1[1]) ** 2),
                        sqrt((T1.p2[0] - T2.p1[0]) ** 2 + (T1.p2[1] - T2.p1[1]) ** 2) +
                        sqrt((T1.p3[0] - T2.p2[0]) ** 2 + (T1.p3[1] - T2.p2[1]) ** 2),
                        sqrt((T1.p2[0] - T2.p2[0]) ** 2 + (T1.p2[1] - T2.p2[1]) ** 2) +
                        sqrt((T1.p3[0] - T2.p1[0]) ** 2 + (T1.p3[1] - T2.p1[1]) ** 2),
                        sqrt((T1.p3[0] - T2.p1[0]) ** 2 + (T1.p3[1] - T2.p1[1]) ** 2) +
                        sqrt((T1.p1[0] - T2.p2[0]) ** 2 + (T1.p1[1] - T2.p2[1]) ** 2),
                        sqrt((T1.p1[0] - T2.p1[0]) ** 2 + (T1.p1[1] - T2.p1[1]) ** 2) +
                        sqrt((T1.p3[0] - T2.p2[0]) ** 2 + (T1.p3[1] - T2.p2[1]) ** 2),
                        sqrt((T1.p3[0] - T2.p2[0]) ** 2 + (T1.p3[1] - T2.p2[1]) ** 2) +
                        sqrt((T1.p1[0] - T2.p1[0]) ** 2 + (T1.p1[1] - T2.p1[1]) ** 2),
                    ]
                    if min(dists) < self.eps:
                        global_flag = False
                        break
            if global_flag:
                polygone.append(T1)
        return polygone

    def visualization(self):
      plt.figure(figsize=(8, 4))
      plt.subplot(1, 2, 1)
      X, Y = zip(*self.points)
      plt.scatter(X, Y, c='black', s=25)

      plt.subplot(1, 2, 2)
      for key in self.triangles:
        T = self.triangles[key]
        plt.plot([T.p1[0], T.p2[0]], [T.p1[1], T.p2[1]], 'g-', linewidth=1)
        plt.plot([T.p2[0], T.p3[0]], [T.p2[1], T.p3[1]], 'g-', linewidth=1)
        plt.plot([T.p3[0], T.p1[0]], [T.p3[1], T.p1[1]], 'g-', linewidth=1)
      plt.scatter(X, Y, c='black', s=25)
      plt.triplot(X, Y, color='pink')
      plt.show()





de = Delaunay(R=15)

points = []
N = 50
for _ in range(N):
    x = 2 * 10 * (random() - 0.5)
    y = 2 * 10 * (random() - 0.5)
    points.append((x, y))

for pt in points:
    de.add_point(pt)

de.visualization()
