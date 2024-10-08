import matplotlib.pyplot as plt                                                 #do wizualizaji danych
import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

    # 1. Wyznaczenie równania prostej, do której należy dana linia.
    def calculate_slope_intercept(self):
        x1, y1 = self.start_point.x, self.start_point.y
        x2, y2 = self.end_point.x, self.end_point.y

        if x1 == x2:                                                            #jeśli x1 równa się x2, linia jest pionowa, a nachylenie (slope) jest nieskończone.
            slope = None
            intercept = x1
        else:
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - slope * x1

        return slope, intercept

    # 2. Sprawdzenie przynależności punktu do prostej / linii
    def is_point_on_line(self, point):
        slope, intercept = self.calculate_slope_intercept()

        if slope is None:                                                       #czy punkt leży na tej pionowej linii
            return point.x == self.start_point.x and \
                   min(self.start_point.y, self.end_point.y) <= point.y <= max(self.start_point.y, self.end_point.y)
        else:
            return point.y == (slope * point.x + intercept)                     #wartość y na linii dla x i porównujemy z y punktu.

    # 3. Określenie położenia punktu względem prostej (prawo/lewo)
    def point_position_relative_to_line(self, point):
        x1, y1 = self.start_point.x, self.start_point.y
        x2, y2 = self.end_point.x, self.end_point.y
        x, y = point.x, point.y

        if x1 == x2:                                                            #przypadek linii pionowej
            if x == x1:
                return "on the line"
            elif x < x1:
                return "left"
            else:
                return "right"
        else:
            position = (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)              #pozycja punktu względem linii - iloczynu wektorowego.

            if position < 0:
                return "left"
            elif position > 0:
                return "right"
            else:
                return "on the line"


    # 4. Dokonanie translacji linii o podany wektor
    def translate(self, vector):                                                #przesuwamy obie współrzędne
        self.start_point.x += vector[0]
        self.end_point.x += vector[0]
        self.start_point.y += vector[1]
        self.end_point.y += vector[1]

    # 5. Dokonanie odbicia danego punktu względem linii
    def reflect_point(self, point):
        slope, intercept = self.calculate_slope_intercept()

        if slope is None:                                                       #dla linii pionowej odbija się względem osi y
            return Point(point.x, 2 * intercept - point.y)
        else:                                                                   #odbicie prostopadłe
            reflected_slope = -1 / slope
            reflected_intercept = point.y - reflected_slope * point.x

            intersection_x = (reflected_intercept - intercept) / (slope - reflected_slope)
            intersection_y = slope * intersection_x + intercept

            reflected_x = 2 * intersection_x - point.x
            reflected_y = 2 * intersection_y - point.y

            return Point(reflected_x, reflected_y)


# 6. Zaimplementuj mechanizm umożliwiający wizualizację graficzną punktów, linii, prostych
def visualize_line_and_point(line, point):                                      #biblioteka matplotlib
    x_vals = [line.start_point.x, line.end_point.x]
    y_vals = [line.start_point.y, line.end_point.y]

    plt.plot(x_vals, y_vals, color='pink', label='Line')
    plt.scatter([point.x], [point.y], color='black', label='Point')
    plt.title('Line and Point Visualization')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.grid(True)
    plt.show()




# TESTY JEDNOSTKOWE

#wersja 1 - punkt poza prostą
point_a = Point(1, 2)
point_b = Point(4, 6)
line_ab = Line(point_a, point_b)
test_point = Point(3, 4)

print(f"is point on the line? {line_ab.is_point_on_line(test_point)}")
print(f"point position relative to the line: {line_ab.point_position_relative_to_line(test_point)}")

visualize_line_and_point(line_ab, test_point)


#wersja 2 - punkt na prostej
point_a2 = Point(1, 7)
point_b2 = Point(7, 13)
line_ab2 = Line(point_a2, point_b2)
test_point2 = Point(4, 10)

print(f"is point on the line? {line_ab2.is_point_on_line(test_point2)}")
print(f"point position relative to the line: {line_ab2.point_position_relative_to_line(test_point2)}")

visualize_line_and_point(line_ab2, test_point2)


#wersja 3 - prosta pionowa
point_a3 = Point(2, 3)
point_b3 = Point(2, 6)
line_ab3 = Line(point_a3, point_b3)
test_point3 = Point(1, 4)

print(f"is point on the line? {line_ab3.is_point_on_line(test_point3)}")
print(f"point position realtive to the line: {line_ab3.point_position_relative_to_line(test_point3)}")

visualize_line_and_point(line_ab3, test_point3)


#translacja (dla wykresu z wersji 2)
translation_vector = (2, 3)
line_ab2.translate(translation_vector)
print(f"translated line: start point ({line_ab2.start_point.x}, {line_ab2.start_point.y}), "
      f"end point ({line_ab2.end_point.x}, {line_ab2.end_point.y})")

visualize_line_and_point(line_ab2, test_point2)


#odbicie punktu (dla wykresu 1)
reflected_point = line_ab.reflect_point(test_point)
print(f"reflected point: ({reflected_point.x}, {reflected_point.y})")

visualize_line_and_point(line_ab, reflected_point)
