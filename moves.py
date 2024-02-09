## MOVEMENTS

import copy
from util import *
from conditions import *

#TODO: Implement action correction

def rotate(A: dict) -> dict:

    new_A               = copy.deepcopy(A)

    new_A['width']      = A['height']
    new_A['height']     = A['width']

    new_A['last-move']  = 'rotate'
     
    return new_A


def action_correction(A: dict, layout_zone : dict) -> dict:

    new_A                           = copy.deepcopy(A)

    _, extend, _                    = calculate_protrusion(layout_zone, new_A)

    new_A['xmin'], new_A['ymin']    = new_A['xmin'] + extend[0], new_A['ymin'] + extend[1]

    return new_A


# SWARM Movements


def reenter(A : dict, layout_zone : dict) -> list:                      # Only activated and working in case of a totally lost participant

    new_A                               = copy.deepcopy(A)

    participant_left_of_layout_zone     = (A['xmin'] < layout_zone['xmin'])

    participant_right_of_layout_zone    = (A['xmin'] + A['width'] >= layout_zone['xmin'] + layout_zone['width']) # To detect if an participant is at the north eastern corner of the layout zone

    participant_above_layout_zone       = (A['ymin'] >= layout_zone['ymin'] + layout_zone['height'])
    
    participant_below_layout_zone       = (A['ymin'] < layout_zone['ymin'])

    x_min_new                           = A['xmin']

    y_min_new                           = A['ymin']

     
    x_min_new                           = layout_zone['xmin'] if participant_left_of_layout_zone else x_min_new

    x_min_new                           = (layout_zone['xmin'] + layout_zone['width'] - A['width']) if participant_right_of_layout_zone else x_min_new

    y_min_new                           = layout_zone['ymin'] if participant_below_layout_zone else y_min_new

    y_min_new                           = (layout_zone['ymin'] + layout_zone['height'] - A['height']) if participant_above_layout_zone else y_min_new

    new_A['xmin'], new_A['ymin']        = x_min_new, y_min_new

    new_A['last-move']                  = 'reenter'
    
    return [new_A]


def evade(A : dict, layout_zone : dict, layout_zone_edge : str, align_position : str) -> list:

    new_A               = copy.deepcopy(A)

    if layout_zone_edge == 'north':

        if align_position == 'left':
         
            x_min_new   = layout_zone['xmin']
            y_min_new   = (layout_zone['ymin'] + layout_zone['height'] - A['height'])

        elif align_position == 'center':

            x_min_new   = int(layout_zone['xmin'] + 0.5 * layout_zone['width'] - 0.5 * A['width'])
            y_min_new   = (layout_zone['ymin'] + layout_zone['height'] - A['height'])

        else: #right

            x_min_new   = layout_zone['xmin'] + layout_zone['width'] - A['width']
            y_min_new   = (layout_zone['ymin'] + layout_zone['height'] - A['height'])

    elif layout_zone_edge == 'east':    # Rotate layout zone clockwise virtually for edge orientation

        if align_position == 'left':
         
            x_min_new   = layout_zone['xmin'] + layout_zone['width'] - A['width']
            y_min_new   = (layout_zone['ymin'] + layout_zone['height'] - A['height'])
        
        elif align_position == 'center':

            x_min_new   = layout_zone['xmin'] + layout_zone['width'] - A['width']
            y_min_new   = int((layout_zone['ymin'] + 0.5 * layout_zone['height'] -  0.5 * A['height']))

        else:

            x_min_new   = layout_zone['xmin'] + layout_zone['width'] - A['width']
            y_min_new   = layout_zone['ymin']

    elif layout_zone_edge == 'south':
         
        if align_position == 'left':

            x_min_new    = layout_zone['xmin']
            y_min_new    = layout_zone['ymin']

        elif align_position == 'center':

            x_min_new    = int(layout_zone['xmin'] + 0.5 * layout_zone['width'] - 0.5 * A['width'])
            y_min_new    = layout_zone['ymin']

        else:

            x_min_new  = layout_zone['xmin'] + layout_zone['width'] - A['width']
            y_min_new  = layout_zone['ymin']

    elif layout_zone_edge == 'west':    # Rotate layout zone counter-clockwise virtually for edge naming orientation

        if align_position == 'left':
         
            x_min_new    = layout_zone['xmin']
            y_min_new    = (layout_zone['ymin'] + layout_zone['height'] - A['height'])

        elif align_position == 'center':

            x_min_new    = layout_zone['xmin']
            y_min_new    = int((layout_zone['ymin'] + 0.5 * layout_zone['height'] -  0.5 * A['height']))

        else:

            x_min_new   = layout_zone['xmin']
            y_min_new   = layout_zone['ymin']

    else:
        
        print('No correct edge given!')  

    new_A['xmin'], new_A['ymin']    = x_min_new, y_min_new    

    new_A['last-move']              = 'evade'

    return [new_A]


def center(A: dict) -> list:

    new_A                           = copy.deepcopy(A)
     
    x_min_new                       = int(A['freespace']['xmin'] + 0.5 * A['freespace']['width'] - 0.5 * A['width'])
    y_min_new                       = int(A['freespace']['ymin'] + 0.5 * A['freespace']['height'] - 0.5 * A['height'])

    new_A['xmin'], new_A['ymin']    = x_min_new, y_min_new

    new_A['last-move']              = 'center'

    return [new_A]


def linger(A: dict) -> list:

    new_A               = copy.deepcopy(A)

    new_A['last-move']  = 'linger'
     
    return [new_A]


def budge(A: dict, direction : str) -> list:   

    new_A                           = copy.deepcopy(A)

    x_min_new                       = int(A[direction]['xmin'] + 0.5 * A[direction]['width'] - 0.5 * A['width'])
    y_min_new                       = int(A[direction]['ymin'] + 0.5 * A[direction]['height'] - 0.5 * A['height'])

    new_A['xmin'], new_A['ymin']    = x_min_new, y_min_new

    new_A['last-move']              = 'budge'
     
    return [new_A]


def swap(A: dict, B: dict) -> list:

    new_A                           = copy.deepcopy(A)
    new_B                           = copy.deepcopy(B)
     
    x_min_new_A                     = int(B['freespace']['xmin'] + 0.5 * B['freespace']['width'] - 0.5 * A['width'])
    y_min_new_A                     = int(B['freespace']['ymin'] + 0.5 * B['freespace']['height'] - 0.5 * A['height'])

    x_min_new_B                     = int(A['freespace']['xmin'] + 0.5 * A['freespace']['width'] - 0.5 * B['width'])
    y_min_new_B                     = int(A['freespace']['ymin'] + 0.5 * A['freespace']['height'] - 0.5 * B['height'])

    new_A['xmin'], new_A['ymin']    = x_min_new_A, y_min_new_A
    new_B['xmin'], new_B['ymin']    = x_min_new_B, y_min_new_B

    new_A['last-move']              = 'swap with ' + new_B['idx']

    return [new_A, new_B]


def pair(A : dict, B : dict, direction : str, layout_zone : dict) -> list:

    new_A                           = copy.deepcopy(A)
    new_B                           = copy.deepcopy(B)

    if direction == 'horizontal-push-right' :
    
        x_min_new_A     = int(B['xmin'] - 0.5 * A['width'])
        x_min_new_B     = int(B['xmin'] + 0.5 * A['width'])
        y_min_new_A     = B['ymin']
        y_min_new_B     = B['ymin']

    elif direction == 'horizontal-push-left' :
        
        x_min_new_A     = int(B['xmin'] + B['width'] - 0.5 * A['width'])
        x_min_new_B     = int(B['xmin'] - 0.5 * A['width'])
        y_min_new_A     = B['ymin']
        y_min_new_B     = B['ymin']

    elif direction == 'vertical-push-up' :

        x_min_new_A     = B['xmin']
        x_min_new_B     = B['xmin']
        y_min_new_A     = int(B['ymin'] - 0.5 * A['height'])
        y_min_new_B     = int(B['ymin'] + 0.5 * A['height'])

    elif direction == 'vertical-push-down':
        x_min_new_A     = B['xmin']
        x_min_new_B     = B['xmin']
        y_min_new_A     = int(B['ymin'] + B['height'] - 0.5 * A['height'])
        y_min_new_B     = int(B['ymin'] - 0.5 * A['height'])

    new_A['xmin'], new_A['ymin']    = x_min_new_A, y_min_new_A
    new_B['xmin'], new_B['ymin']    = x_min_new_B, y_min_new_B

    # Action correction to not push other participants out of the safe zone
    new_B                           = action_correction(new_B, layout_zone)

    new_A['last-move']              = 'pair with ' + new_B['idx']

    return [new_A, new_B]


def hustle(A : dict, layout_zone : dict, participants : dict) -> list:

    new_A                           = copy.deepcopy(A)

    #print('A ' + A['idx'])

    moved_participants              = []

    for idx in A['overlap-with-idx']:

        #print(idx)

        B                               = participants[idx]

        new_B                           = copy.deepcopy(B)
        
        overlap, locations              = calculate_overlap(A, new_B)

        if locations[1]:    # B fully encloses A -> A can not hustle but must flee // Added to prevent stuck state in case of full overlap

            if B['ymin'] > 0.5 * (layout_zone['ymin'] + layout_zone['height']):     # Enclosure in the upper half of the layout zone -> A flees south

                new_A['xmin']               = int(new_B['xmin'] + 0.5 * new_B['width'] - 0.5 * new_A['width'])
                new_A['ymin']               = int(new_B['ymin'] - 0.5 * new_A['height'])

            else:   # A flees north

                new_A['xmin']               = int(new_B['xmin'] + 0.5 * new_B['width'] - 0.5 * new_A['width'])
                new_A['ymin']               = int(new_B['ymin'] + new_B['height'] - 0.5 * new_A['height'])

            new_A['last-move']              = 'flee'

            break

        else:

            if overlap['width'] <= overlap['height']:

                delta_x                     = overlap['width'] if B['xmin'] > A['xmin'] else overlap['width'] * -1
                delta_y                     = 0

            else:
                
                delta_x                     = 0
                delta_y                     = overlap['height'] if B['ymin'] >= A['ymin'] else overlap['height'] * -1


            x_min_new_B                     = B['xmin'] + delta_x

            y_min_new_B                     = B['ymin'] + delta_y

            new_B['xmin'], new_B['ymin']    = x_min_new_B, y_min_new_B

            # Action correction to not push other participants out of the safe zone
            new_B                           = action_correction(new_B, layout_zone)


            moved_participants.append(new_B)

            new_A['last-move']                  = 'hustle'

    return [new_A] + moved_participants


def yielt(A : dict) -> list:      # Intentional typo in "yield" to avoid keyword

    new_A                           = copy.deepcopy(A)
     
    x_center_yield_poly             = A['yield-polygon']['xmin'] + 0.5 * A['yield-polygon']['width']

    y_center_yield_poly             = A['yield-polygon']['ymin'] + 0.5 * A['yield-polygon']['height']

    x_min_new_A                     = x_center_yield_poly - 0.5 * A['width']

    y_min_new_A                     = y_center_yield_poly - 0.5 * A['height']

    new_A['xmin'], new_A['ymin']    = x_min_new_A, y_min_new_A

    new_A['last-move']              = 'yield'
    
    return [new_A]