## MOVEMENTS

import copy
from collections import namedtuple
from util import *
from conditions import *
from swarm_types import *

def rotate(A: namedtuple) -> namedtuple:

    new_A = A._replace(width = A.height, height = A.width, last_move = 'rotate')
     
    return new_A


def action_correction(A: namedtuple, layout_zone : namedtuple) -> namedtuple:

    _, extend, _    = calculate_protrusion(layout_zone, A)

    new_A           = A._replace(xmin = A.xmin + extend[0], ymin = A.ymin + extend[1])

    return new_A


# SWARM Movements


def reenter(A : namedtuple, layout_zone : namedtuple) -> list:                      # Only activated and working in case of a totally lost participant

    participant_left_of_layout_zone     = (A.xmin < layout_zone.xmin)

    participant_right_of_layout_zone    = (A.xmin + A.width >= layout_zone.xmin + layout_zone.width) # To detect if an participant is at the north eastern corner of the layout zone

    participant_above_layout_zone       = (A.ymin >= layout_zone.ymin + layout_zone.height)
    
    participant_below_layout_zone       = (A.ymin < layout_zone.ymin)

    x_min_new                           = A.xmin

    y_min_new                           = A.ymin

     
    x_min_new                           = layout_zone.xmin if participant_left_of_layout_zone else x_min_new

    x_min_new                           = (layout_zone.xmin + layout_zone.width - A.width) if participant_right_of_layout_zone else x_min_new

    y_min_new                           = layout_zone.ymin if participant_below_layout_zone else y_min_new

    y_min_new                           = (layout_zone.ymin + layout_zone.height - A.height) if participant_above_layout_zone else y_min_new


    new_A                               = A._replace(xmin = x_min_new, ymin = y_min_new, last_move = 'reenter')
    
    return [new_A]


def evade(A : namedtuple, layout_zone : namedtuple, layout_zone_edge : str, align_position : str) -> list:

    if layout_zone_edge == 'north':

        if align_position == 'left':
         
            x_min_new   = layout_zone.xmin
            y_min_new   = (layout_zone.ymin + layout_zone.height - A.height)

        elif align_position == 'center':

            x_min_new   = int(layout_zone.xmin + 0.5 * layout_zone.width - 0.5 * A.width)
            y_min_new   = (layout_zone.ymin + layout_zone.height - A.height)

        else: #right

            x_min_new   = layout_zone.xmin + layout_zone.width - A.width
            y_min_new   = (layout_zone.ymin + layout_zone.height - A.height)

    elif layout_zone_edge == 'east':    # Rotate layout zone clockwise virtually for edge orientation

        if align_position == 'left':
         
            x_min_new   = layout_zone.xmin + layout_zone.width - A.width
            y_min_new   = (layout_zone.ymin + layout_zone.height - A.height)
        
        elif align_position == 'center':

            x_min_new   = layout_zone.xmin + layout_zone.width - A.width
            y_min_new   = int((layout_zone.ymin + 0.5 * layout_zone.height -  0.5 * A.height))

        else:

            x_min_new   = layout_zone.xmin + layout_zone.width - A.width
            y_min_new   = layout_zone.ymin

    elif layout_zone_edge == 'south':
         
        if align_position == 'left':

            x_min_new    = layout_zone.xmin
            y_min_new    = layout_zone.ymin

        elif align_position == 'center':

            x_min_new    = int(layout_zone.xmin + 0.5 * layout_zone.width - 0.5 * A.width)
            y_min_new    = layout_zone.ymin

        else:

            x_min_new  = layout_zone.xmin + layout_zone.width - A.width
            y_min_new  = layout_zone.ymin

    elif layout_zone_edge == 'west':    # Rotate layout zone counter-clockwise virtually for edge naming orientation

        if align_position == 'left':
         
            x_min_new    = layout_zone.xmin
            y_min_new    = (layout_zone.ymin + layout_zone.height - A.height)

        elif align_position == 'center':

            x_min_new    = layout_zone.xmin
            y_min_new    = int((layout_zone.ymin + 0.5 * layout_zone.height -  0.5 * A.height))

        else:

            x_min_new   = layout_zone.xmin
            y_min_new   = layout_zone.ymin

    else:
        
        print('No correct edge given!')  

    new_A                               = A._replace(xmin = x_min_new, ymin = y_min_new, last_move = 'evade')


    return [new_A]


def center(A: namedtuple) -> list:
     
    x_min_new                       = int(A['freespace'].xmin + 0.5 * A['freespace'].width - 0.5 * A.width)
    y_min_new                       = int(A['freespace'].ymin + 0.5 * A['freespace'].height - 0.5 * A.height)

    new_A                      = A._replace(xmin = x_min_new, ymin = y_min_new, last_move = 'center')

    return [new_A]


def linger(A: namedtuple) -> list:

    new_A   = A._replace(last_move = 'linger')
     
    return [new_A]


def budge(A: namedtuple, direction : str) -> list:   

    secondary_free_space            = getattr(A, direction)

    x_min_new                       = int(secondary_free_space.xmin + 0.5 * secondary_free_space.width - 0.5 * A.width)
    y_min_new                       = int(secondary_free_space.ymin + 0.5 * secondary_free_space.height - 0.5 * A.height)

    new_A                           = A._replace(xmin = x_min_new, ymin = y_min_new, last_move = 'budge')

    return [new_A]


def swap(A: namedtuple, B: namedtuple) -> list:

    new_A   = A._replace(xmin = B.xmin, ymin = B.ymin, last_move = 'swap')
    new_B   = B._replace(xmin = A.xmin, ymin = A.ymin, last_move = 'swap')

    return [new_A, new_B]


def pair(A : namedtuple, B : namedtuple, direction : str, layout_zone : namedtuple) -> list:


    if direction == 'horizontal-push-right' :
    
        x_min_new_A     = int(B.xmin - 0.5 * A.width)
        x_min_new_B     = int(B.xmin + 0.5 * A.width)
        y_min_new_A     = B.ymin
        y_min_new_B     = B.ymin

    elif direction == 'horizontal-push-left' :
        
        x_min_new_A     = int(B.xmin + B.width - 0.5 * A.width)
        x_min_new_B     = int(B.xmin - 0.5 * A.width)
        y_min_new_A     = B.ymin
        y_min_new_B     = B.ymin

    elif direction == 'vertical-push-up' :

        x_min_new_A     = B.xmin
        x_min_new_B     = B.xmin
        y_min_new_A     = int(B.ymin - 0.5 * A.height)
        y_min_new_B     = int(B.ymin + 0.5 * A.height)

    elif direction == 'vertical-push-down':
        x_min_new_A     = B.xmin
        x_min_new_B     = B.xmin
        y_min_new_A     = int(B.ymin + B.height - 0.5 * A.height)
        y_min_new_B     = int(B.ymin - 0.5 * A.height)


    new_A               = A._replace(xmin = x_min_new_A, ymin = y_min_new_A, last_move = 'pair with ' + B.idx)
    new_B               = B._replace(xmin = x_min_new_B, ymin = y_min_new_B, last_move = 'pair with ' + A.idx)

    # Action correction to not push other participants out of the safe zone
    new_B_corrected           = action_correction(new_B, layout_zone)


    return [new_A, new_B_corrected]


def hustle(A : namedtuple, layout_zone : namedtuple, participants : set) -> list:

    moved_participants              = []

    overlapping_participants    = {p for p in participants if p.idx in A.overlap_with_idx}

    for B in overlapping_participants:
        
        overlap, locations              = calculate_overlap(A, B)

        if locations[1]:    # B fully encloses A -> A can not hustle but must flee // Added to prevent stuck state in case of full overlap

            if B.ymin > 0.5 * (layout_zone.ymin + layout_zone.height):     # Enclosure in the upper half of the layout zone -> A flees south

                xmin_new_A              = int(B.xmin + 0.5 * B.width - 0.5 * A.width)
                ymin_new_A              = int(B.ymin - 0.5 * A.height)

            else:   # A flees north

                xmin_new_A              = int(B.xmin + 0.5 * B.width - 0.5 * A.width)
                ymin_new_A              = int(B.ymin + B.height - 0.5 * A.height)

            new_A                       = A._replace(xmin = xmin_new_A, ymin = ymin_new_A, last_move = 'flee')

            break

        else:

            if overlap.width <= overlap.height:

                delta_x                 = overlap.width if B.xmin > A.xmin else overlap.width * -1
                delta_y                 = 0

            else:
                
                delta_x                 = 0
                delta_y                 = overlap.height if B.ymin >= A.ymin else overlap.height * -1


            x_min_new_B                 = B.xmin + delta_x

            y_min_new_B                 = B.ymin + delta_y

            new_B                       = B._replace(xmin = x_min_new_B, ymin = y_min_new_B, last_move = ' got hustled by ' + A.idx)

            # Action correction to not push other participants out of the safe zone
            new_B_corrected             = action_correction(new_B, layout_zone)

            moved_participants          = moved_participants + [new_B_corrected]

            new_A                       = A._replace(last_move = 'hustle')

    return [new_A] + moved_participants


def yielt(A : namedtuple) -> list:      # Intentional typo in "yield" to avoid keyword
     
    x_center_yield_poly = A.yield_polygon.xmin + 0.5 * A.yield_polygon.width

    y_center_yield_poly = A.yield_polygon.ymin + 0.5 * A.yield_polygon.height

    x_min_new_A         = x_center_yield_poly - 0.5 * A.width

    y_min_new_A         = y_center_yield_poly - 0.5 * A.height

    new_A               = A._replace(xmin = x_min_new_A, ymin = y_min_new_A, last_move = 'yield')
    
    return [new_A]