# Bringing a Gun to a Trainer Fight
# =================================

# Uh-oh -- you've been cornered by one of Commander Lambdas elite bunny trainers! Fortunately, you grabbed a beam weapon from an abandoned storeroom while you were running through the station, so you have a chance to fight your way out. But the beam weapon is potentially dangerous to you as well as to the bunny trainers: its beams reflect off walls, meaning you'll have to be very careful where you shoot to avoid bouncing a shot toward yourself!

# Luckily, the beams can only travel a certain maximum distance before becoming too weak to cause damage. You also know that if a beam hits a corner, it will bounce back in exactly the same direction. And of course, if the beam hits either you or the bunny trainer, it will stop immediately (albeit painfully). 

# Write a function solution(dimensions, your_position, trainer_position, distance) that gives an array of 2 integers of the width and height of the room, an array of 2 integers of your x and y coordinates in the room, an array of 2 integers of the trainer's x and y coordinates in the room, and returns an integer of the number of distinct directions that you can fire to hit the elite trainer, given the maximum distance that the beam can travel.

# The room has integer dimensions [1 < x_dim <= 1250, 1 < y_dim <= 1250]. You and the elite trainer are both positioned on the integer lattice at different distinct positions (x, y) inside the room such that [0 < x < x_dim, 0 < y < y_dim]. Finally, the maximum distance that the beam can travel before becoming harmless will be given as an integer 1 < distance <= 10000.

# For example, if you and the elite trainer were positioned in a room with dimensions [3, 2], your_position [1, 1], trainer_position [2, 1], and a maximum shot distance of 4, you could shoot in seven different directions to hit the elite trainer (given as vector bearings from your location): [1, 0], [1, 2], [1, -2], [3, 2], [3, -2], [-3, 2], and [-3, -2]. As specific examples, the shot at bearing [1, 0] is the straight line horizontal shot of distance 1, the shot at bearing [-3, -2] bounces off the left wall and then the bottom wall before hitting the elite trainer with a total shot distance of sqrt(13), and the shot at bearing [1, 2] bounces off just the top wall before hitting the elite trainer with a total shot distance of sqrt(5).

# Languages
# =========

# To provide a Java solution, edit Solution.java
# To provide a Python solution, edit solution.py

# Test cases
# ==========
# Your code should pass the following test cases.
# Note that it may also be run against hidden test cases not shown here.

# -- Java cases --
# Input:
# Solution.solution([3,2], [1,1], [2,1], 4)
# Output:
#     7

# Input:
# Solution.solution([300,275], [150,150], [185,100], 500)
# Output:
#     9

# -- Python cases --
# Input:
# solution.solution([3,2], [1,1], [2,1], 4)
# Output:
#     7

# Input:
# solution.solution([300,275], [150,150], [185,100], 500)
# Output:
#     9

from math import sqrt
from numpy import zeros


def computeDist(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def computeGCD(x, y):
    while(y):
        x, y = y, x % y
    return abs(x)


def get_entity_position_from_room_number(entity, room_number, dimensions):
    r_x, r_y = room_number
    e_x, e_y = entity
    dim_x, dim_y = dimensions

    res_x = dim_x*r_x + e_x if r_x % 2 == 0 else dim_x*r_x + (dim_x - e_x)
    res_y = dim_y*r_y + e_y if r_y % 2 == 0 else dim_y*r_y + (dim_y - e_y)

    return (res_x, res_y)


def solution(dimensions, your_position, trainer_position, distance):

    dim_x, dim_y = dimensions
    m_x, m_y = your_position

    num_rooms_above_x_axis = (distance + m_y)//dim_y + 1
    num_rooms_below_x_axis = (distance - m_y)//dim_y + 1
    num_rooms_left_of_y_axis = (distance - m_x)//dim_x + 1
    num_rooms_right_of_y_axis = (distance + m_x)//dim_x + 1

    w = (num_rooms_right_of_y_axis + num_rooms_left_of_y_axis)*dim_x + 1
    h = (num_rooms_above_x_axis + num_rooms_below_x_axis)*dim_y + 1

    x_offset = num_rooms_left_of_y_axis*dim_x
    y_offset = num_rooms_below_x_axis*dim_y

    matrix = zeros(shape=(w, h))
    for i in range(-1*num_rooms_left_of_y_axis, num_rooms_right_of_y_axis):
        for j in range(-1*num_rooms_below_x_axis, num_rooms_above_x_axis):
            tv_x, tv_y = get_entity_position_from_room_number(
                trainer_position, [i, j], dimensions)

            mv_x, mv_y = get_entity_position_from_room_number(
                your_position, [i, j], dimensions)

            matrix[tv_x+x_offset][tv_y+y_offset] = 1
            matrix[mv_x+x_offset][mv_y+y_offset] = 2

    hits = 0
    shots_taken = set()
    for i in range(-1*num_rooms_left_of_y_axis, num_rooms_right_of_y_axis):
        for j in range(-1*num_rooms_below_x_axis, num_rooms_above_x_axis):
            t_x, t_y = get_entity_position_from_room_number(
                trainer_position, [i, j], dimensions)
            if distance < computeDist([t_x, t_y], your_position):
                continue
            delta_y = t_y - m_y
            delta_x = t_x - m_x
            d = computeGCD(delta_y, delta_x)
            delta_y = int(delta_y/d)
            delta_x = int(delta_x/d)
            if (delta_y, delta_x) in shots_taken:
                continue
            shots_taken.add((delta_y, delta_x))
            ray_x, ray_y = m_x + x_offset, m_y + y_offset
            while True:
                ray_x += delta_x
                ray_y += delta_y
                entity = matrix[ray_x][ray_y]
                if entity == 1:
                    hits += 1
                    break
                elif entity == 2:
                    break
    return hits
