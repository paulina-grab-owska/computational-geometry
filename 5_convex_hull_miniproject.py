import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon as ShapelyPolygon
import time


# dane z plików
def read_space_craft_file(filename):
    with open(filename, 'r') as file:
        position = list(map(float, file.readline().strip().split()))
        velocity = list(map(float, file.readline().strip().split()))
    return position, velocity

def read_craft_file(filename):
    with open(filename, 'r') as file:
        file.readline()
        craft_points = []
        for line in file:
            x, y = map(float, line.strip().split())
            craft_points.append([x, y])
    return craft_points

def read_missiles_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        missiles = []
        for line in lines:
            data = line.strip().split()
            time = float(data[0])
            position = list(map(float, data[1:3]))
            velocity = list(map(float, data[3:]))
            missiles.append({'time': time, 'position': position, 'velocity': velocity})
    return missiles









# rysowanie pola walki
def draw_battlefield(ax, craft_points, space_craft_position, missiles):
    # statek kosmiczny
    moved_craft_points = craft_points + np.array(space_craft_position)
    ax.scatter(moved_craft_points[:, 0], moved_craft_points[:, 1], color='blue', s=5)

    # pociski
    for missile in missiles:
        ax.plot(missile['position'][0], missile['position'][1], marker='o', color='red', markersize=5)

    ax.set_xlim([-500, 500])
    ax.set_ylim([-500, 500])
    ax.set_aspect('equal')


    craft_polygon = ShapelyPolygon(moved_craft_points)
    space_craft_point = Point(space_craft_position)
    for missile in missiles:
        missile_point = Point(missile['position'])
        if craft_polygon.contains(missile_point) or space_craft_point.distance(missile_point) < 10:
            return True
    return False

craft_points = np.array(read_craft_file('/content/craft1_ksztalt.txt'))
space_craft_position, space_craft_velocity = read_space_craft_file('/content/space_craft1.txt')
missiles = read_missiles_file('/content/missiles3.txt')


# aktualizacja pozycji obiektów
def update_position(object_position, object_velocity, time_delta):
    return object_position + np.array(object_velocity) * time_delta


# sprawdzanie kolizji
def check_collision(craft_points, space_craft_position, missiles):
    for missile in missiles:
        missile_point = missile['position']
        for craft_point in craft_points:
            moved_craft_point = craft_point + np.array(space_craft_position)
            if np.linalg.norm(missile_point - moved_craft_point) < 10:
                return True
    return False

# pole walki
time_delta = 0.1
total_time = 5.0
current_time = 0.0
collision_detected = False

while current_time <= total_time:
    fig, ax = plt.subplots(figsize=(10, 10))
    draw_battlefield(ax, craft_points, space_craft_position, missiles)
    ax.set_title(f'Time: {current_time} s')
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.grid(True)

    if check_collision(craft_points, space_craft_position, missiles):
        collision_detected = True
        break

    space_craft_position = update_position(space_craft_position, space_craft_velocity, time_delta)
    for missile in missiles:
        missile['position'] = update_position(missile['position'], missile['velocity'], time_delta)

    current_time += time_delta
    plt.pause(0.1)







