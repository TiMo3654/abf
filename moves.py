## MOVEMENTS

import copy

from util import *

def rotate(A: dict) -> tuple:

    new_width   = A['height']
    new_height  = A['width']
     
    return new_width, new_height


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

    return [new_A]


def center(A: dict) -> list:

    new_A                           = copy.deepcopy(A)
     
    x_min_new                       = int(A['freespace']['xmin'] + 0.5 * A['freespace']['width'] - 0.5 * A['width'])
    y_min_new                       = int(A['freespace']['ymin'] + 0.5 * A['freespace']['height'] - 0.5 * A['height'])

    new_A['xmin'], new_A['ymin']    = x_min_new, y_min_new

    return [new_A]


def linger(A: dict) -> list:

    new_A   = copy.deepcopy(A)
     
    return [new_A]


def budge(A: dict, direction : str) -> list:   

    new_A                           = copy.deepcopy(A)

    x_min_new       = int(A[direction]['xmin'] + 0.5 * A[direction]['width'] - 0.5 * A['width'])
    y_min_new       = int(A[direction]['ymin'] + 0.5 * A[direction]['height'] - 0.5 * A['height'])

    new_A['xmin'], new_A['ymin']    = x_min_new, y_min_new
     
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

    return [new_A, new_B]


def pair(A : dict, B : dict, direction : str) -> list:

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


    return [new_A, new_B]


def hustle(A : dict, B : dict) -> list:

    new_A                           = copy.deepcopy(A)
    new_B                           = copy.deepcopy(B)
    
    overlap, locations  = calculate_overlap(A, B)

    #print(overlap)

    if overlap['width'] <= overlap['height']:

        delta_x         = overlap['width'] if B['xmin'] >= A['xmin'] else overlap['width'] * -1
        delta_y         = 0

    else:
         
        delta_x         = 0
        delta_y         = overlap['height'] if B['ymin'] >= A['ymin'] else overlap['height'] * -1


    x_min_new_B         = B['xmin'] + delta_x

    y_min_new_B         = B['ymin'] + delta_y

    new_A['xmin'], new_A['ymin']    = A['xmin'], A['ymin']
    new_B['xmin'], new_B['ymin']    = x_min_new_B, y_min_new_B

    return [new_A, new_B]


def yielt(A : dict) -> list:      # Intentional typo in "yield" to avoid keyword

    new_A             = copy.deepcopy(A)
     
    x_center_yield_poly     = A['yield-polygon']['xmin'] + 0.5 * A['yield-polygon']['width']

    y_center_yield_poly     = A['yield-polygon']['ymin'] + 0.5 * A['yield-polygon']['height']

    x_min_new_A             = x_center_yield_poly - 0.5 * A['width']

    y_min_new_A             = y_center_yield_poly - 0.5 * A['height']

    new_A['xmin'], new_A['ymin']    = x_min_new_A, y_min_new_A
    
    return [new_A]


## Action exploration and evaluation

def classify_action(A : dict) -> str:
     
    if (A['protrusion-status'] == 'safe') and A['healthy'] and A['compliant'] and (A['interference'] == 0) and (A['relaxed-connections'] == len(A['connections'])):
        
        action_classification   = 'adjuvant'
    
    elif (A['protrusion-status'] == 'safe') and A['healthy'] and A['compliant']:
        
        action_classification   = 'valid'

    else:
         
        action_classification   = 'invalid'

    return action_classification


def explore_action(A : dict, participants : dict, layout_zone : dict, leeway_coeffcient : float, conciliation_quota : float, critical_amount : int, action : function) -> tuple:

    adjuvant_position                   = []
    valid_position                      = []
    invalid_position                    = []

    moved_participants                  = action(A)     # list with either one entry (only a moved A) or two entries (moved A and B) / the action make deep copies of A and B

    for participant in moved_participants:
    
        # Implement action correction here

        moved_participant_conditions    = calculate_conditions(participant, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount)

        participant.update(moved_participant_conditions)

        participant['last-move']        = action.__name__

        if participant['last-move'] == 'reenter' or participant['last-move'] == 'yielt':    # classification irrelevant in this case
            
            valid_position.append(participant)

        else:

            action_classification       = classify_action(participant)

            if action_classification == 'adjuvant':
                
                adjuvant_position.append(participant)  
            
            elif action_classification == 'valid':
                    
                valid_position.append(participant)

            else:   # invalid action

                invalid_position.append(participant)
                adjuvant_position       = []
                valid_position          = []

                break  
    
    return adjuvant_position, valid_position, invalid_position

# Use map() fuction to try out different layout variants of the same participant?

def action_exploration(A : dict, participants : dict, layout_zone : dict, leeway_coeffcient : float, conciliation_quota : float, critical_amount : int) -> list:

    possible_next_positions = []    # [ [A_center], [A_budge], [A_swap, B_swap] ... ]

    # start of the action exploration

    if A['protrusion-status'] == 'lost':

        action                              = lambda P: reenter(P, layout_zone)

        _, valid_position, __               = explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)

        return [valid_position]
    
    else:   # A is prone or safe
         
        # explore centering

        action                              = lambda P: center(P)

        adjuvant_position, valid_position, _= explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)

        if adjuvant_position:            
            return [adjuvant_position]  # [ [A_center] ]
        
        if valid_position:            
            possible_next_positions.append(valid_position) # [ [A_center] ]

        # explore lingering
            
        action                              = lambda P: linger(P)

        adjuvant_position, valid_position, _= explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)      

        if adjuvant_position:            
            return [adjuvant_position]  # [ [A_linger] ]
        
        if valid_position:            
            possible_next_positions.append(valid_position)  # [ [A_center], [A_linger] ]
        
        # explore budging, swapping, pairing, hustling only if A is safe, otherwise only centering, evasion or yielding is possible

        if A['protrusion-status'] == 'safe':

            # explore budging

            free_secondary_spaces                   = [f'secondary-free-space-{corner}' 
                                                       for corner in ['north-west', 'north-east', 'south-east', 'south-west'] 
                                                       if A[f'secondary-free-space-{corner}']]

            for direction in free_secondary_spaces:

                action                              = lambda P: budge(P, direction)

                adjuvant_position, valid_position, _= explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)

                if adjuvant_position:            
                    return [adjuvant_position]
        
                if valid_position:            
                    possible_next_positions.append(valid_position)
                
            # explore hustling
                                
            for idx_B in A['overlap-with-idx']:
                
                B   = participants[idx_B]

                action                              = lambda P: hustle(P, B)

                adjuvant_position, valid_position   = explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)


            
            # explore swapping
            
            for B in participants.values:
                 
                action                                              = lambda P: swap(P, B)

                adjuvant_position, valid_position, invalid_position = explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)
                
                if len(adjuvant_position) == 2:            
                    return [adjuvant_position]
        
                if len(invalid_position) == 0:            
                    possible_next_positions.append(valid_position)
                
            # explore pairing
                
            for B in participants.values:
                 
                action                                              = lambda P: pair(P, B)

                adjuvant_position, valid_position, invalid_position = explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)                  

                if len(adjuvant_position) == 2:            
                    return [adjuvant_position]
        
                if len(invalid_position) == 0:            
                    possible_next_positions.append(valid_position)   

        else:   # participant is prone
             
            # explore evasion

            align_positions = ['left', 'center', 'right']

            for edge in A['protruded-zone-edges']:

                for position in align_positions:
                
                    action                                  = lambda P: evade(P, layout_zone, edge, position)

                    adjuvant_position, valid_position, _    = explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)  

                if adjuvant_position:            
                    return [adjuvant_position]
        
                if valid_position:            
                    possible_next_positions.append(valid_position)
                
        # explore yield in case of not lost and interference

        if len(possible_next_positions) == 0 and A['interference'] != 0:             

            action                              = lambda P: yielt(P)

            _, valid_position, __               = explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)         
            
            if valid_position:            
                possible_next_positions.append(valid_position)

                    
    return possible_next_positions


def action_evaluation(possible_next_positions : list, evaluation_metric : str) -> dict:
     
    return 0