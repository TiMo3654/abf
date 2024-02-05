
from moves import *
from util import *
from conditions import *

import math

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

    actual_participants                 = copy.deepcopy(participants)

    moved_participants                  = action(A)     # list with either one entry (only a moved A) or two entries (moved A and B) or more in case of hustle/ the actions make deep copies of the moved participants

    for participant in moved_participants:
        
        actual_participants.update(participant)         # consider the newest positions (important for hustle)
    

    for participant in moved_participants:
    
        # Implement action correction here

        moved_participant_conditions    = calculate_conditions(participant, actual_participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount)

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
    
    return adjuvant_position, valid_position, invalid_position

# Use map() fuction to try out different layout variants of the same participant?

def action_exploration(A : dict, participants : dict, layout_zone : dict, leeway_coeffcient : float, conciliation_quota : float, critical_amount : int) -> list:

    possible_next_positions = []    # [ [A_center], [A_budge], [A_swap, B_swap], [A_hustle, B_hustle, F_hustle, G_hustle] ... ] -> A list of lists
 
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
                                
            action                              = lambda P: hustle(P, participants)

            adjuvant_position, valid_position, _= explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)

            if adjuvant_position or valid_position:
                possible_next_positions.append(adjuvant_position + valid_position)  # new positions for all participants in valid positions
            
            # explore swapping
            
            for B in participants.values:
                 
                action                                              = lambda P: swap(P, B)

                adjuvant_position, valid_position, invalid_position = explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)
                
                if len(adjuvant_position) == 2:            
                    return [adjuvant_position]
        
                if len(invalid_position) == 0:            
                    possible_next_positions.append(adjuvant_position + valid_position)
                
            # explore pairing
                
            for B in participants.values:
                 
                action                                              = lambda P: pair(P, B)

                adjuvant_position, valid_position, invalid_position = explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)                  

                if len(adjuvant_position) == 2:            
                    return [adjuvant_position]
        
                if len(invalid_position) == 0:            
                    possible_next_positions.append(adjuvant_position + valid_position)   

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



## Action evaluation

def determine_best_move(possible_next_positions : list) -> list:

    prospective_interference_minimum    = math.inf

    for idx, positions in enumerate(possible_next_positions):   # [ [A_center], [A_budge], [A_swap, B_swap], [A_hustle, B_hustle, F_hustle, G_hustle] ... ] -> A list of lists

        summed_interference             = 0

        for moved_participant in positions: # [A_hustle, B_hustle, F_hustle, G_hustle]

            summed_interference         = summed_interference + moved_participant['interference']   # TODO: Do not count interference twice in case of mutual overlap

        if summed_interference < prospective_interference_minimum:

            prospective_interference_minimum    = summed_interference

            best_position                       = idx

    return possible_next_positions[best_position]

        
#TODO: Add turmoil metric to the choice of the next move metric

# def action_evaluation(possible_next_positions : list, evaluation_metric : str) -> dict:

#     if evaluation_metric == 'interference-only':
    


#     elif evaluation_metric == 'interference-and-turmoil':

#     else:

#         print('No valid metric given!')
     
#     return 0