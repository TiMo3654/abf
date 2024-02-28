
from moves import *
from util import *
from conditions import *
from heuristics import *
from collections import namedtuple

import math
import os
import functools

## Action exploration and evaluation

def check_non_trivial_action(A : namedtuple, A_new : namedtuple) -> bool:

    moving_distance         = calculate_euclidean_distance(A, A_new)

    minimal_moving_distance = A.freespace.height * 0.01 if (A.freespace.width > A.freespace.height) else A.freespace.width * 0.01

    return (moving_distance > minimal_moving_distance)


def classify_action(A : namedtuple) -> str:

     
    if (A.protrusion_status == 'safe') and A.healthy and A.compliant and (len(A.overlap_with_idx) == 0) and (A.relaxed_connections == len(A.connections)):
        
        action_classification   = 'adjuvant'
    
    elif (A.protrusion_status == 'safe') and A.healthy and A.compliant:
        
        action_classification   = 'valid'

    else:
         
        action_classification   = 'invalid'

    return action_classification


def explore_action(A : namedtuple, participants : set, layout_zone : namedtuple, leeway_coeffcient : float, conciliation_quota : float, critical_amount : int, action) -> tuple:

    tic                           = time.time()

    adjuvant_position             = []
    valid_position                = []
    invalid_position              = []

    # Try action

    moved_participants            = action(A)     # list with either one entry (only a moved A) or two entries (moved A and B) or more in case of hustle/ the actions make deep copies of the moved participants

    moved_participants_ids        = [p.idx for p in moved_participants]

    # Update positions

    participants_updated        = set([p for p in participants if p.idx not in moved_participants_ids] + moved_participants)

    # Evaluate new positions (update conditions for the moved participants)

    moved_participants_updated  = [calculate_conditions(A, participants_updated, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount) for A in moved_participants]

    # Classify moves

    classifications             = [classify_action(A) for A in moved_participants_updated]

    classified_moves            = list(zip(*(moved_participants_updated, classifications)))

    # Sort moves

    adjuvant_position           = [p[0] for p in classified_moves if p[1] == 'adjuvant']        
    valid_position              = [p[0] for p in classified_moves if p[1] == 'valid']  
    invalid_position            = [p[0] for p in classified_moves if p[1] == 'invalid']  

    toc = time.time()

    #print('explore_action took: ' + str(toc-tic))
    
    return adjuvant_position, valid_position, invalid_position



def action_exploration(A : namedtuple, participants : set, layout_zone : namedtuple, leeway_coeffcient : float, conciliation_quota : float, critical_amount : int) -> list:

    possible_next_positions = []    # [ [A_center], [A_budge], [A_swap, B_swap], [A_hustle, B_hustle, F_hustle, G_hustle] ... ] -> A list of lists

    #print(str(A['idx']) + ' takes a turn!')
 
    # start of the action exploration

    if A.protrusion_status == 'lost':

        action                              = lambda P: reenter(P, layout_zone)

        _, valid_position, __               = explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)

        return [valid_position]
    
    else:   # A is prone or safe
         
        # explore centering

        if A.freespace:

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

        if A.protrusion_status == 'safe':

            # explore budging

            tic = time.time()


            free_secondary_spaces                   = ['secondary_freespace_north_west', 'secondary_freespace_north_east', 'secondary_freespace_south_west', 'secondary_freespace_south_east']

            for direction in free_secondary_spaces:

                if getattr(A, direction):

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

            swap_results                                            = [swap_exploration(B) for B in participants if B.idx != A.idx]
          
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

                    pairing_options                                         = [(B, direction) for B in participants if estimate_pair_success(A, B, direction) and B.idx != A.idx]    # returns a list of tuples -> Each participant with each pairing direction

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

            for edge in A.protruded_zone_edges:

                for position in align_positions:
                
                    action                                  = lambda P: evade(P, layout_zone, edge, position)

                    adjuvant_position, valid_position, _    = explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)  

                if adjuvant_position:            
                    return [adjuvant_position]
        
                if valid_position:            
                    possible_next_positions         = possible_next_positions + [valid_position]
                
        # explore yield in case of not lost and interference

        # if len(possible_next_positions) == 0 and A['interference'] != 0 and A['yield-polygon']:             #TODO: Rethink yield

        #     action                                          = lambda P: yielt(P)

        #     adjuvant_position, valid_position, __           = explore_action(A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount, action)         
            
        #     if valid_position or adjuvant_position:            
        #         possible_next_positions         = possible_next_positions + [adjuvant_position + valid_position]

                    
    return possible_next_positions



## Action evaluation

def determine_best_move(possible_next_positions : list, partcipants : set, metric : str) -> list:

    next_position                                   = []

    if possible_next_positions: # [ [A_center], [A_budge], [A_swap, B_swap], [A_hustle, B_hustle, F_hustle, G_hustle] ... ] -> A list of lists

        if len(possible_next_positions) != 1:


            # interference
            summed_interference                 = [sum([A.interference for A in moved_participants]) for moved_participants in possible_next_positions]

            best_position_due_to_interference   = summed_interference.index(min(summed_interference))

            # turmoil

            number_of_relaxed_connections       = [sum([A.relaxed_connections for A in moved_participants]) for moved_participants in possible_next_positions]

            max_no_of_relaxed_connections       = max(number_of_relaxed_connections)

            best_positions_due_to_turmoil_ids   = [i for (i, x) in enumerate(number_of_relaxed_connections) if x == max_no_of_relaxed_connections] # get idx of all equally relaxing position

            best_positions_due_to_turmoil       = [x for (i,x) in enumerate(possible_next_positions) if i in best_positions_due_to_turmoil_ids]

            summed_interference                 = [sum([A.interference for A in moved_participants]) for moved_participants in best_positions_due_to_turmoil]

            best_position_due_to_turmoil_and_interference  = summed_interference.index(min(summed_interference))

            # determine next position
            next_position                       = possible_next_positions[best_position_due_to_interference] if metric == 'interference' else best_positions_due_to_turmoil[best_position_due_to_turmoil_and_interference]

            
            # if metric == 'interference':

            #     next_position                           = possible_next_positions[best_position_due_to_interference]

            # else:   # 'turmoil'

            #     most_relaxed_connections                = min(relaxation_deltas_list)
            #     best_positions_due_to_turmoil_ids       = [i for i, x in enumerate(relaxation_deltas_list) if x == most_relaxed_connections]

            #     if len(best_positions_due_to_turmoil_ids) == 1: # Only one best relaxing action

            #         next_position                       = possible_next_positions[best_positions_due_to_turmoil_ids[0]]

            #     else:   # Multiple best relaxing actions

            #         prospective_interference_minimum    = math.inf

            #         for idx in best_positions_due_to_turmoil_ids:

            #             if summed_interference_list[idx] < prospective_interference_minimum:

            #                 prospective_interference_minimum                = summed_interference_list[idx]

            #                 best_position_due_to_interference_and_turmoil   = idx

            #         next_position                       = possible_next_positions[best_position_due_to_interference_and_turmoil]
        
        else:

            next_position                               = possible_next_positions[0]


    return next_position

