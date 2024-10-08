import matplotlib.pyplot as plt
import numpy as np
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def length(self):
        return math.sqrt((self.point2.x - self.point1.x)**2 + (self.point2.y - self.point1.y)**2)



class Triangle:
    def __init__(self, point1, point2, point3):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3

# 1. Dodaj metodę obliczającą pole Trójkąta
    def area(self):
        a = Line(self.point1, self.point2).length()
        b = Line(self.point2, self.point3).length()
        c = Line(self.point3, self.point1).length()
        s = (a + b + c) / 2
        return math.sqrt(s * (s - a) * (s - b) * (s - c))

#2. Dodaj metodę obliczającą kąt pomiędzy dwoma liniami
    def angle_between_lines(self, line1, line2):
        vector1_x = line1.point2.x - line1.point1.x
        vector1_y = line1.point2.y - line1.point1.y
        vector2_x = line2.point2.x - line2.point1.x
        vector2_y = line2.point2.y - line2.point1.y

        dot_product = vector1_x * vector2_x + vector1_y * vector2_y
        magnitude1 = math.sqrt(vector1_x**2 + vector1_y**2)
        magnitude2 = math.sqrt(vector2_x**2 + vector2_y**2)

        cos_theta = dot_product / (magnitude1 * magnitude2)
        return math.degrees(math.acos(cos_theta))





def visualize_triangle(triangle):
    plt.plot([triangle.point1.x, triangle.point2.x, triangle.point3.x, triangle.point1.x],
             [triangle.point1.y, triangle.point2.y, triangle.point3.y, triangle.point1.y], 'r-')
    plt.plot(triangle.point1.x, triangle.point1.y, 'bo')
    plt.plot(triangle.point2.x, triangle.point2.y, 'bo')
    plt.plot(triangle.point3.x, triangle.point3.y, 'bo')
    plt.show()





# 3. Dodaj metodę sprawdzającą czy należy do niego podany punkt (2 sposoby)

# a. kąty
def is_inside_angles_sum(triangle, point):
    angle1 = triangle.angle_between_lines(Line(triangle.point1, point), Line(triangle.point3, point))
    angle2 = triangle.angle_between_lines(Line(triangle.point2, point), Line(triangle.point1, point))
    angle3 = triangle.angle_between_lines(Line(triangle.point2, point), Line(triangle.point3, point))
    sum_of_angles = angle1 + angle2 + angle3
    return abs(sum_of_angles - 360) < 1e-6

# b.  pola
def is_inside_area_comparison(triangle, point):
    area_triangle = triangle.area()
    sub_triangle1 = Triangle(point, triangle.point2, triangle.point3)
    sub_triangle2 = Triangle(triangle.point1, point, triangle.point3)
    sub_triangle3 = Triangle(triangle.point1, triangle.point2, point)
    sum_sub_areas = sub_triangle1.area() + sub_triangle2.area() + sub_triangle3.area()
    return abs(area_triangle - sum_sub_areas) < 1e-6





def visualize_triangle_with_points(triangle, point1, point2):
    plt.plot([triangle.point1.x, triangle.point2.x, triangle.point3.x, triangle.point1.x],
             [triangle.point1.y, triangle.point2.y, triangle.point3.y, triangle.point1.y], 'r-')
    plt.plot(triangle.point1.x, triangle.point1.y, 'bo')
    plt.plot(triangle.point2.x, triangle.point2.y, 'bo')
    plt.plot(triangle.point3.x, triangle.point3.y, 'bo')
    plt.plot(point1.x, point1.y, 'go')
    plt.plot(point2.x, point2.y, 'yo')
    plt.show()





# 4-5. Dodaj reprezentację wielokąta; do reprezentacji wielokąta dodaj metodę sprawdzającą czy należy do niego podany punkt
class Polygon:
    def __init__(self, *points):
        self.points = points

    def is_inside(self, point):
        crossings = 0
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]
            if (p1.y > point.y) != (p2.y > point.y) and \
               point.x < (p2.x - p1.x) * (point.y - p1.y) / (p2.y - p1.y) + p1.x:
                crossings += 1
        return crossings % 2 == 1





def visualize_polygon_with_points(polygon, point1, point2):
    plt.plot([p.x for p in polygon.points] + [polygon.points[0].x],
             [p.y for p in polygon.points] + [polygon.points[0].y], 'r-')
    plt.plot([point1.x], [point1.y], 'bo')
    plt.plot([point2.x], [point2.y], 'yo')
    plt.show()





##################### TESTY JEDNOSTKOWE ###################  

#  TRÓJKĄT - POLE
triangle = Triangle(Point(0, 0), Point(4, 0), Point(0, 3))
print(f"traingle area:  {triangle.area()}")
visualize_triangle(triangle)

# TRÓJKĄT - KĄT
triangle2 = Triangle(Point(9, 3), Point(8, 8), Point(4, 1))
line1 = Line(Point(9, 3), Point(8, 8))
line2 = Line(Point(4, 1), Point(8, 8))
print(f"traingle angle:  {triangle2.angle_between_lines(line1, line2)}")
visualize_triangle(triangle2)


# TRÓJĄT I PUNKT
point_inside = Point(0, 0)
point_outside = Point(4, 2)

print("Point inside (angle sum):", is_inside_angles_sum(triangle, point_inside))
print("Point outside  (angle sum):", is_inside_angles_sum(triangle, point_outside))

print("Point inside (area sum):", is_inside_area_comparison(triangle, point_inside))
print("Point outside  (area sum):", is_inside_area_comparison(triangle, point_outside))

visualize_triangle_with_points(triangle, point_inside, point_outside)


#WIELOKĄT
polygon = Polygon(Point(0, 0), Point(4, 1), Point(5, 4), Point(2, 3), Point(0, 2))
point_inside1 = Point(0, 1)
point_outside1 = Point(5, 5)

print("Point inside:", polygon.is_inside(point_inside1))
print("Point outside:", polygon.is_inside(point_outside1))

visualize_polygon_with_points(polygon, point_inside1, point_outside1)

















