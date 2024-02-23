
from moves import *
from util import *
from conditions import *
from heuristics import *
from multiprocess import Pool

import math
import os
import functools

## Action exploration and evaluation

def check_non_trivial_action(A : dict, A_new : dict) -> bool:

    moving_distance         = calculate_euclidean_distance(A, A_new)

    minimal_moving_distance = A['freespace']['height'] * 0.01 if (A['freespace']['width'] > A['freespace']['height']) else A['freespace']['width'] * 0.01

    return (moving_distance > minimal_moving_distance)


def classify_action(A : dict) -> str:

    # if A['idx'] == '0':
    #     print(A['overlap-with-idx'])
     
    if (A['protrusion-status'] == 'safe') and A['healthy'] and A['compliant'] and (len(A['overlap-with-idx']) == 0) and (A['relaxed-connections'] == len(A['connections'])):
        
        action_classification   = 'adjuvant'
    
    elif (A['protrusion-status'] == 'safe') and A['healthy'] and A['compliant']:
        
        action_classification   = 'valid'

    else:
         
        action_classification   = 'invalid'

    return action_classification


def explore_action(A : dict, participants : dict, layout_zone : dict, leeway_coeffcient : float, conciliation_quota : float, critical_amount : int, action) -> tuple:

    tic                                 = time.time()

    adjuvant_position                   = []
    valid_position                      = []
    invalid_position                    = []

    actual_participants                 = copy.deepcopy(participants) # A not included yet

    moved_participants                  = action(A)     # list with either one entry (only a moved A) or two entries (moved A and B) or more in case of hustle/ the actions make deep copies of the moved participants

    moved_participant_dict              = {moved_participant['idx'] : moved_participant for moved_participant in moved_participants}

    actual_participants                 = actual_participants | moved_participant_dict

    for participant in moved_participants:
    
        participant_new                 = actual_participants.pop(participant['idx'])   # Remove the leading participant from the overall dict to calculate the conditions (No overlap with itself)

        moved_participant_conditions    = calculate_conditions(participant_new, actual_participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount)

        participant_new                 = participant_new | moved_participant_conditions

        if participant_new['last-move'] == 'reenter':    # classification irrelevant in this case
            
            valid_position              = valid_position + [participant_new]

        else:

            action_classification       = classify_action(participant_new)

            if action_classification == 'adjuvant':
                
                adjuvant_position       = adjuvant_position + [participant_new]  
            
            elif action_classification == 'valid':
                    
                valid_position          = valid_position + [participant_new]

            else:   # invalid action

                invalid_position        = invalid_position + [participant_new]

        actual_participants             = actual_participants | {participant_new['idx'] : participant_new}  # Put the moved participant back into the dictionary for the condition calculation of the other moved participants

    toc = time.time()

    #print('explore_action took: ' + str(toc-tic))
    
    return adjuvant_position, valid_position, invalid_position



def action_exploration(A : dict, participants : dict, layout_zone : dict, leeway_coeffcient : float, conciliation_quota : float, critical_amount : int) -> list:

    possible_next_positions = []    # [ [A_center], [A_budge], [A_swap, B_swap], [A_hustle, B_hustle, F_hustle, G_hustle] ... ] -> A list of lists

    parallel_workers        = min(len(participants), os.cpu_count() - 1)

    #print(str(A['idx']) + ' takes a turn!')
 
    # start of the action exploration

    if A['protrusion-status'] == 'lost':

        action                              = lambda P: reenter(P, layout_zone)

        _, valid_position, __               = explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)

        return [valid_position]
    
    else:   # A is prone or safe
         
        # explore centering

        if A['freespace']:

            tic = time.time()

            action                              = lambda P: center(P)

            adjuvant_position, valid_position, _= explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)

            #print(adjuvant_position)

            if adjuvant_position and check_non_trivial_action(A, adjuvant_position[0]):   
                #print('center is adjuvant')         
                return [adjuvant_position]  # [ [A_center] ]
            
            if valid_position and check_non_trivial_action(A, valid_position[0]):      
                #print('center is valid')       
                possible_next_positions         = possible_next_positions + [valid_position] # [ [A_center] ]

            toc = time.time()

            #print('Center Exploration took: ' +str(toc-tic))


        # explore lingering
            
        action                              = lambda P: linger(P)

        adjuvant_position, valid_position, _= explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)      

        if adjuvant_position:    
            #print('linger is adjuvant')        
            return [adjuvant_position]  # [ [A_linger] ]
        
        if valid_position:            
            possible_next_positions         = possible_next_positions + [valid_position]  # [ [A_center], [A_linger] ]
        
        # explore budging, swapping, pairing, hustling only if A is safe, otherwise only centering, evasion or yielding is possible

        if A['protrusion-status'] == 'safe':

            # explore budging

            tic = time.time()


            free_secondary_spaces                   = [f'secondary-freespace-{corner}' 
                                                       for corner in ['north-west', 'north-east', 'south-east', 'south-west'] 
                                                       if A[f'secondary-freespace-{corner}']]

            for direction in free_secondary_spaces:

                action                              = lambda P: budge(P, direction)

                adjuvant_position, valid_position, _= explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)

                if adjuvant_position:            
                    return [adjuvant_position]
        
                if valid_position:            
                    possible_next_positions         = possible_next_positions + [valid_position]

            toc = time.time()

            #print('Budge Exploration took: ' +str(toc-tic))

            # explore hustling

            tic = time.time()
                                
            action                              = lambda P: hustle(P, layout_zone, participants)

            adjuvant_position, valid_position, _= explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)

            if adjuvant_position or valid_position:
                possible_next_positions         = possible_next_positions + [adjuvant_position + valid_position] # new positions for all participants in valid positions

            toc = time.time()

            #print('Hustle Exploration took: ' +str(toc-tic))

            tic = time.time()
            
            # explore swapping

            swap_exploration                                        = lambda B: explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, lambda P: swap(P, B))

            swap_results                                            = [swap_exploration(B) for B in list(participants.values())]
          
            adjuvant_swap_move                                      = [mytup[0] for mytup in swap_results if len(mytup[0]) == 2]

            if adjuvant_swap_move:

                return adjuvant_swap_move
            
            else:

                valid_swap_positions                                = [mytup[0] + mytup[1] for mytup in swap_results if not mytup[2]] 

                possible_next_positions                             = possible_next_positions + valid_swap_positions

                toc = time.time()

                #print('Swap Exploration took: ' +str(toc-tic))

                tic = time.time()

                # explore pairing

                length_pairing_options = 0

                for direction in ['horizontal-push-right', 'horizontal-push-left', 'vertical-push-up', 'vertical-push-down']:

                    pairing_options                                         = [(x, direction) for x in list(participants.values()) if estimate_pair_success(A, x, direction)]    # returns a list of tuples -> Each participant with each pairing direction

                    length_pairing_options                                  = length_pairing_options + len(pairing_options)

                    pair_exploration                                        = lambda pair_tuple: explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, lambda P: pair(P, pair_tuple[0], pair_tuple[1], layout_zone))

                    pair_results                                            = [pair_exploration(B) for B in pairing_options]

                    adjuvant_pair_move                                      = [mytup[0] for mytup in pair_results if len(mytup[0]) == 2]

                    if adjuvant_pair_move:

                        return adjuvant_pair_move
                    
                    else:
                    
                        valid_pair_positions                                    = [mytup[0] + mytup[1] for mytup in pair_results if not mytup[2]] 

                        possible_next_positions                                 = possible_next_positions + valid_pair_positions

                #print('No. of pairing options explored: ' + str(length_pairing_options))

                toc = time.time()

                #print('Pair Exploration took: ' + str(toc-tic))

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
                    possible_next_positions         = possible_next_positions + [valid_position]
                
        # explore yield in case of not lost and interference

        if len(possible_next_positions) == 0 and A['interference'] != 0 and A['yield-polygon']:             

            action                                          = lambda P: yielt(P)

            adjuvant_position, valid_position, __           = explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)         
            
            if valid_position or adjuvant_position:            
                possible_next_positions         = possible_next_positions + [adjuvant_position + valid_position]

                    
    return possible_next_positions



## Action evaluation

def determine_best_move(possible_next_positions : list, partcipants : dict, metric : str) -> dict:

    next_position                                   = []

    if possible_next_positions:

        if len(possible_next_positions) != 1:

            prospective_interference_minimum    = math.inf

            relaxation_deltas_list              = []

            summed_interference_list            = []


            for idx, positions in enumerate(possible_next_positions):   # [ [A_center], [A_budge], [A_swap, B_swap], [A_hustle, B_hustle, F_hustle, G_hustle] ... ] -> A list of lists

                summed_interference             = 0

                summed_relaxation_delta         = 0

                for moved_participant in positions: # [A_hustle, B_hustle, F_hustle, G_hustle] or [A_center]

                    summed_interference         = summed_interference + moved_participant['interference']   # TODO: Do not count interference twice in case of mutual overlap

                    relaxation_delta            = partcipants[moved_participant['idx']]['relaxed-connections'] - moved_participant['relaxed-connections']   # Negative means relaxation

                    summed_relaxation_delta     = summed_relaxation_delta + relaxation_delta

                # For interference metric

                if summed_interference < prospective_interference_minimum:

                    prospective_interference_minimum    = summed_interference

                    best_position_due_to_interference   = idx

                # For turmoil metric

                relaxation_deltas_list.append(summed_relaxation_delta)

                summed_interference_list.append(summed_interference)

            
            if metric == 'interference':

                next_position                           = possible_next_positions[best_position_due_to_interference]

            else:   # 'turmoil'

                most_relaxed_connections                = min(relaxation_deltas_list)
                best_positions_due_to_turmoil_ids       = [i for i, x in enumerate(relaxation_deltas_list) if x == most_relaxed_connections]

                if len(best_positions_due_to_turmoil_ids) == 1: # Only one best relaxing action

                    next_position                       = possible_next_positions[best_positions_due_to_turmoil_ids[0]]

                else:   # Multiple best relaxing actions

                    prospective_interference_minimum    = math.inf

                    for idx in best_positions_due_to_turmoil_ids:

                        if summed_interference_list[idx] < prospective_interference_minimum:

                            prospective_interference_minimum                = summed_interference_list[idx]

                            best_position_due_to_interference_and_turmoil   = idx

                    next_position                       = possible_next_positions[best_position_due_to_interference_and_turmoil]
        
        else:

            next_position                               = possible_next_positions[0]

    
    next_position_dict                                  = {moved_participant['idx'] : moved_participant for moved_participant in next_position}

    return next_position_dict

