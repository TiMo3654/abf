import random
import math
from matplotlib import pyplot as plt, patches
import matplotlib.colors as mcolors
from IPython import display
import pylab as pl
import time
import copy

def calculate_overlap(A : dict, B : dict) -> tuple:

    x_A_min             = A['xmin']
    y_A_min             = A['ymin']
    x_A_max             = A['xmin'] + A['width']
    y_A_max             = A['ymin'] + A['height']

    x_B_min             = B['xmin']
    y_B_min             = B['ymin']
    x_B_max             = B['xmin'] + B['width']
    y_B_max             = B['ymin'] + B['height']

    # Determine overlap direction (multiple can be true)

    if  (x_A_min >= x_B_max or x_A_max <= x_B_min) or (y_A_min >= y_B_max or y_A_max <= y_B_min):    # No horizontal or vertical overlap

        overlapped          = False
        locations           = [False, False, False, False, False, False]

    else:

        overlapped        = True

        A_fully_encloses_B      = (x_A_min <= x_B_min <= x_A_max) and (x_A_min <= x_B_max <= x_A_max) and  (y_A_min <= y_B_min <= y_A_max) and (y_A_min <= y_B_max <= y_A_max)

        B_fully_encloses_A      = (x_B_min <= x_A_min <= x_B_max) and (x_B_min <= x_A_max <= x_B_max) and (y_B_min <= y_A_min <= y_B_max) and (y_B_min <= y_A_max <= y_B_max)

        west_edge_overlap       = (x_A_min > x_B_min) and (x_A_min < x_B_max)

        east_edge_overlap       = (x_A_max > x_B_min) and (x_A_max < x_B_max)

        north_edge_overlap      = (y_A_max > y_B_min) and (y_A_max < y_B_max)

        south_edge_overlap      = (y_A_min > y_B_min) and (y_A_min < y_B_max)
        
        locations   = [A_fully_encloses_B, B_fully_encloses_A, west_edge_overlap, east_edge_overlap, north_edge_overlap, south_edge_overlap]

# Determine overlap coordinates

    if not overlapped:
        overlap = {}
    else:
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

        overlap_width = x_Overlap_max - x_Overlap_min
        overlap_height = y_Overlap_max - y_Overlap_min

        overlap = {
            "xmin": x_Overlap_min,
            "ymin": y_Overlap_min,
            "width": overlap_width,
            "height": overlap_height
        }
        
    return overlap, locations
    

def calculate_participant_area(A : dict) -> float:

    return A['width'] * A['height']


def calculate_layout_area(layout_zone : dict) -> float:

    total_layout_area = layout_zone['width'] * layout_zone['height']      

    return total_layout_area


def calculate_euclidean_distance(A : dict, B : dict) -> float:

    center_A_x  = A['xmin'] + 0.5 * A['width']

    center_A_y  = A['ymin'] + 0.5 * A['height']

    center_B_x  = B['xmin'] + 0.5 * B['width']

    center_B_y  = B['ymin'] + 0.5 * B['height']

    distance    = math.sqrt((center_A_x - center_B_x)**2 + (center_A_y - center_B_y)**2)

    return distance


def calculate_all_participants_area(participants : dict) -> float:

    widths                        = [sub_dict.get('width') for sub_dict in participants.values()]

    heights                       = [sub_dict.get('height') for sub_dict in participants.values()]

    summed_participants_area      = sum([a * b for a, b in zip(widths, heights)])

    return summed_participants_area






        










