import matplotlib.pyplot as plt                                                 #do wizualizaji danych
import numpy as np                                                              #do wykonywania obliczeń
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.calculate_coefficients()

# 1. Obliczanie punktu przecięcia dwóch prostych

# a. na podstawie współczynników równania w postaci ogólnej (metoda wyznaczników)

    def calculate_coefficients(self):                                           #wspołczynniki równania prostych (ax + by = c)
        self.a = self.end.y - self.start.y
        self.b = self.start.x - self.end.x
        self.c = - self.a * self.start.x - self.b * self.start.y

def intersection_point_general_form(line1, line2):
    a1, b1, c1 = line1.a, line1.b, line1.c                                      #wyopdrębnienie współczynników
    a2, b2, c2 = line2.a, line2.b, line2.c

    det = a1 * b2 - a2 * b1
    if det == 0:
        if a1 / a2 == b1 / b2 == c1 / c2:
            return "lines overlap each other"
        else:
            return "lines are parallel, but don't overlap"
    else:
        x = (b1 * c2 - b2 * c1) / det
        y = (a2 * c1 - a1 * c2) / det
        return Point(x, y)


# b. na podstawie dwóch linii o znanym początku i końcu (punkt przecięcia prostych przechodzących przez te linie),

def intersection_point(line1, line2):
    x1, y1 = line1.start.x, line1.start.y
    x2, y2 = line1.end.x, line1.end.y
    x3, y3 = line2.start.x, line2.start.y
    x4, y4 = line2.end.x, line2.end.y

    det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if det == 0:
        if (x1 - x2) * (y1 - y3) == (y1 - y2) * (x1 - x3):
            return "lines overlap each other"
        else:
            return "lines are parallel, but don't overlap"
    else:                                                                                 #wzory z wykładu
        x = (x2 * (x3 * y4 - x4 * y3 + (x4 - x3) * y1) + x1 * (x4 * y3 - x3 * y4 + (x3 - x4) * y2)) / ((x1 - x2) * (y3 - y4) - (x3 - x4) * (y1 - y2))
        y = (y2 * (x3 * y4 - x4 * y3) + y1 * (x4 * y3 - x3 * y4) + x2 * y1 * (y4 - y3) + x1 * y2 * (y3 - y4)) / ((x1 - x2) * (y3 - y4) - (x3 - x4) * (y1 - y2))
        return Point(x, y)


# 1.5. Zmierzenie odległości między punktem a linią (długość najkrótszego odcinka łączącego punkt z prostą przechodzącą przez daną linię).

def distance_point_to_line(point, line_start, line_end):                        #zwraca bezpośrednio odległość punktu od prostej
    x, y = point.x, point.y
    x1, y1 = line_start.x, line_start.y
    x2, y2 = line_end.x, line_end.y

    numerator = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)          #abs eliminuje znak
    denominator = ((y2 - y1)**2 + (x2 - x1)**2) ** 0.5

    distance = numerator / denominator
    return distance

def closest_distance_point_to_line(point, line_start, line_end):                #zwraca punkt u na prostej, który leży najbliżej danego punktu
    x, y = point.x, point.y
    x1, y1 = line_start.x, line_start.y
    x2, y2 = line_end.x, line_end.y

    u = ((x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)) / ((x2 - x1)**2 + (y2 - y1)**2)

    x_closest = x1 + u * (x2 - x1)
    y_closest = y1 + u * (y2 - y1)

    closest_point = Point(x_closest, y_closest)
    return closest_point




# 2. Zaimplementuj klasę reprezentującą trójkąt (3 wierzchołki). Stwórz funkcję, która przyjmuje współczyniki rówań trzech prostych i na tej podstawie tworzy obiekt trójkąt ograniczony tymi trzema prostymi.
class Triangle:
    def __init__(self, line_eq1, line_eq2, line_eq3):
        self.line1 = self.create_line(line_eq1)
        self.line2 = self.create_line(line_eq2)
        self.line3 = self.create_line(line_eq3)

    def create_line(self, line_eq):
        A, B, C = line_eq
        start = self.calculate_point(0, A, B, C)
        end = self.calculate_point(1, A, B, C)
        return Line(start, end)

    def calculate_point(self, t, A, B, C):
        x = t
        y = (-C - A * x) / B
        return Point(x, y)





def visualize_lines_and_points(line1, line2, point1, point2, intersection_point=None):
    plt.plot([line1.start.x, line1.end.x], [line1.start.y, line1.end.y], label='Line 1', color='blue')
    plt.plot([line2.start.x, line2.end.x], [line2.start.y, line2.end.y], label='Line 2', color='green')

    plt.scatter(point1.x, point1.y, marker='o', label='Point 1', color='red')
    plt.text(point1.x, point1.y, '  Point 1', verticalalignment='bottom')

    plt.scatter(point2.x, point2.y, marker='o', label='Point 2', color='purple')
    plt.text(point2.x, point2.y, '  Point 2', verticalalignment='bottom')

    if intersection_point:
        plt.scatter(intersection_point.x, intersection_point.y, color='black', label='Intersection Point')

# rysowanie najkrótszego odcinka łączącego punkt z prostą przechodzącą przez daną linię
    closest_point1 = closest_distance_point_to_line(point1, line1.start, line1.end)
    closest_point2 = closest_distance_point_to_line(point2, line2.start, line2.end)

    plt.plot([point1.x, closest_point1.x], [point1.y, closest_point1.y], linestyle='dashed', color='gray')
    plt.plot([point2.x, closest_point2.x], [point2.y, closest_point2.y], linestyle='dashed', color='gray')

    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.grid(True)
    plt.show()

def visualize_triangle(triangle):
    x1, y1 = triangle.line1.start.x, triangle.line1.start.y
    x2, y2 = triangle.line1.end.x, triangle.line1.end.y
    x3, y3 = triangle.line2.end.x, triangle.line2.end.y

    plt.plot([x1, x2], [y1, y2], label='Line 1', color='black')
    plt.plot([x2, x3], [y2, y3], label='Line 2', color='blue')
    plt.plot([x3, x1], [y3, y1], label='Line 3', color='red')

    plt.fill([x1, x2, x3], [y1, y2, y3], color='lightgray', alpha=0.5, label='Triangle Area')

    plt.scatter([x1, x2, x3], [y1, y2, y3], color='green', label='Vertices')

    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Triangle Visualization')
    plt.legend()
    plt.grid(True)
    plt.show()






# TESTY JEDNOSTKOWE

#1 a.
point1 = Point(2, 1)
point2 = Point(8, 6)
line1 = Line(point1, point2)

point3 = Point(4, 4)
point4 = Point(6, 1)
line2 = Line(point3, point4)

intersection = intersection_point_general_form(line1, line2)
print("intersection point:", intersection.x, intersection.y)

visualize_lines_and_points(line1, line2, point1, point2, intersection)

# 1 b.
point5 = Point(5, 1)
point6 = Point(10, 7)
line3 = Line(point5, point6)

point7 = Point(3, 9)
point8 = Point(5, 1)
line4 = Line(point7, point8)

intersection2 = intersection_point(line3, line4)
print("intersection point:", intersection2.x, intersection2.y)
visualize_lines_and_points(line3, line4, point5, point6, intersection2)

# 1.5
point = Point(1, 4)

distance = distance_point_to_line(point, point5, point6)
closest_point = closest_distance_point_to_line(point, point5, point6)

print("distance from point to line:", distance)
print("closest point on the line:", closest_point.x, closest_point.y)

visualize_lines_and_points(line3, line4, point5, point6, intersection2)


# 2.
line_eq1 = (2, -1, 1)                                                           #2x - y + 1 = 0
line_eq2 = (-1, 1, 3)                                                           #-x + y + 3 = 0
line_eq3 = (1, 1, -2)                                                           #x + y - 2 = 0

triangle = Triangle(line_eq1, line_eq2, line_eq3)

print("the vertises of the traingle:")
print("vertise 1:", triangle.line1.start.x, triangle.line1.start.y)
print("vertise 2:", triangle.line2.start.x, triangle.line2.start.y)
print("vertise 3:", triangle.line3.start.x, triangle.line3.start.y)

visualize_triangle(triangle)
