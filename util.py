from collections import namedtuple
from swarm_types import *

import math

def point_in_rectangle(x, y, B : namedtuple) -> bool:

    return not ( (B.xmin < x < B.xmin + B.width) and (B.ymin < y < B.ymin + B.heigth) ) # returns False, iff point in rectangle -> easier for the next function


def calculate_free_corners(A: namedtuple, B: namedtuple) -> list:

    corner_north_west = (A.xmin, A.ymin + A.height)
    corner_north_east = (A.xmin + A.width, A.ymin + A.height)
    corner_south_west = (A.xmin, A.ymin)
    corner_south_east = (A.xmin + A.width, A.ymin)

    free_corners_bool = [point_in_rectangle(*corner, B) for corner in [corner_north_west, corner_north_east, corner_south_west, corner_south_east]]

    return free_corners_bool


def calculate_overlap(A : namedtuple, B : namedtuple) -> tuple:

    x_A_min, y_A_min, x_A_max, y_A_max  = A.xmin, A.ymin, A.xmin + A.width, A.ymin + A.height

    x_B_min, y_B_min, x_B_max, y_B_max  = B.xmin, B.ymin, B.xmin + B.width, B.ymin + B.height

    # Determine overlap direction (multiple can be true)

    if  (x_A_min >= x_B_max or x_A_max <= x_B_min) or (y_A_min >= y_B_max or y_A_max <= y_B_min):    # No horizontal or vertical overlap

        overlap                 = ()
        locations               = [False, False, False, False, False, False]

    else:

        A_fully_encloses_B      = (x_A_min <= x_B_min <= x_A_max) and (x_A_min <= x_B_max <= x_A_max) and  (y_A_min <= y_B_min <= y_A_max) and (y_A_min <= y_B_max <= y_A_max)

        B_fully_encloses_A      = (x_B_min <= x_A_min <= x_B_max) and (x_B_min <= x_A_max <= x_B_max) and (y_B_min <= y_A_min <= y_B_max) and (y_B_min <= y_A_max <= y_B_max)

        west_edge_overlap       = (x_A_min > x_B_min) and (x_A_min < x_B_max)

        east_edge_overlap       = (x_A_max > x_B_min) and (x_A_max < x_B_max)

        north_edge_overlap      = (y_A_max > y_B_min) and (y_A_max < y_B_max)

        south_edge_overlap      = (y_A_min > y_B_min) and (y_A_min < y_B_max)
        
        locations               = [A_fully_encloses_B, B_fully_encloses_A, west_edge_overlap, east_edge_overlap, north_edge_overlap, south_edge_overlap]

        # Determine overlap coordinates

        if A_fully_encloses_B:
            x_Overlap_min, x_Overlap_max, y_Overlap_min, y_Overlap_max = x_B_min, x_B_max, y_B_min, y_B_max
        elif B_fully_encloses_A:
            x_Overlap_min, x_Overlap_max, y_Overlap_min, y_Overlap_max = x_A_min, x_A_max, y_A_min, y_A_max
        elif north_edge_overlap and east_edge_overlap and west_edge_overlap:
            x_Overlap_min, x_Overlap_max, y_Overlap_min, y_Overlap_max = x_A_min, x_A_max, y_B_min, y_A_max
        elif north_edge_overlap and east_edge_overlap and south_edge_overlap:
            x_Overlap_min, x_Overlap_max, y_Overlap_min, y_Overlap_max = x_A_min, x_B_max, y_A_min, y_A_max
        elif north_edge_overlap and west_edge_overlap and south_edge_overlap:
            x_Overlap_min, x_Overlap_max, y_Overlap_min, y_Overlap_max = x_B_min, x_A_max, y_A_min, y_B_max
        elif south_edge_overlap and east_edge_overlap and west_edge_overlap:
            x_Overlap_min, x_Overlap_max, y_Overlap_min, y_Overlap_max = x_A_min, x_A_max, y_A_min, y_B_max
        elif north_edge_overlap and east_edge_overlap:
            x_Overlap_min, x_Overlap_max, y_Overlap_min, y_Overlap_max = x_B_min, x_A_max, y_B_min, y_A_max
        elif north_edge_overlap and west_edge_overlap:
            x_Overlap_min, x_Overlap_max, y_Overlap_min, y_Overlap_max = x_A_min, x_B_max, y_B_min, y_A_max
        elif north_edge_overlap and south_edge_overlap:
            x_Overlap_min, x_Overlap_max, y_Overlap_min, y_Overlap_max = x_B_min, x_B_max, y_A_min, y_A_max
        elif south_edge_overlap and east_edge_overlap:
            x_Overlap_min, x_Overlap_max, y_Overlap_min, y_Overlap_max = x_B_min, x_A_max, y_A_min, y_B_max
        elif south_edge_overlap and west_edge_overlap:
            x_Overlap_min, x_Overlap_max, y_Overlap_min, y_Overlap_max = x_A_min, x_B_max, y_A_min, y_B_max
        elif east_edge_overlap and west_edge_overlap:
            x_Overlap_min, x_Overlap_max, y_Overlap_min, y_Overlap_max = x_A_min, x_A_max, y_B_min, y_B_max
        elif north_edge_overlap:
            x_Overlap_min, x_Overlap_max, y_Overlap_min, y_Overlap_max = x_B_min, x_B_max, y_B_min, y_A_max
        elif east_edge_overlap:
            x_Overlap_min, x_Overlap_max, y_Overlap_min, y_Overlap_max = x_B_min, x_A_max, y_B_min, y_B_max
        elif south_edge_overlap:
            x_Overlap_min, x_Overlap_max, y_Overlap_min, y_Overlap_max = x_B_min, x_B_max, y_A_min, y_B_max
        elif west_edge_overlap:
            x_Overlap_min, x_Overlap_max, y_Overlap_min, y_Overlap_max = x_A_min, x_B_max, y_B_min, y_B_max

        overlap_width   = x_Overlap_max - x_Overlap_min
        overlap_height  = y_Overlap_max - y_Overlap_min

        overlap = Rectangle(x_Overlap_min, y_Overlap_min, overlap_width, overlap_height)
        
    return overlap, locations


def calculate_area(A : namedtuple) -> float:

    return A.width * A.height



def calculate_euclidean_distance(A : namedtuple, B : namedtuple) -> float:

    center_A_x  = A.xmin + 0.5 * A.width

    center_A_y  = A.ymin + 0.5 * A.height

    center_B_x  = B.xmin + 0.5 * B.width

    center_B_y  = B.ymin + 0.5 * B.height

    distance    = math.sqrt((center_A_x - center_B_x)**2 + (center_A_y - center_B_y)**2)

    return distance


def calculate_all_participants_area(participants : set) -> float:

    widths                        = [p.width for p in participants]

    heights                       = [p.height for p in participants]

    summed_participants_area      = sum([a * b for a, b in zip(widths, heights)])

    return summed_participants_area






        










