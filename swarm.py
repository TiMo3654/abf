from util import *
from moves import *
from exploration import *
from conditions import *
from interaction import *
from multiprocess.pool import ThreadPool

import copy
import time

def determine_initial_conditions(participants : dict, layout_zone : dict, conciliation_quota : float, critical_amount : int) -> dict:

    leeway_coefficient          = calculate_leeway_coefficient(layout_zone, participants)

    new_participants            = copy.deepcopy(participants)

    id_list                     = [p['idx'] for p in (new_participants.values())]

    #new_participants            = {participant['idx'] : participant | calculate_conditions(participant, new_participants, layout_zone, leeway_coefficient, conciliation_quota, critical_amount)}

    for idx in id_list:

        participant             = new_participants.pop(idx)

        participant_conditions  = calculate_conditions(participant, new_participants, layout_zone, leeway_coefficient, conciliation_quota, critical_amount)

        participant             = participant | participant_conditions

        new_participants        = new_participants | {participant['idx'] : participant}

    return new_participants



def one_round_of_interaction(participants : dict, layout_zone : dict, metric : str, conciliation_quota : float, critical_amount : int) -> dict:

    tic                             = time.time()

    leeway_coefficient              = calculate_leeway_coefficient(layout_zone, participants)

    new_participants                = copy.deepcopy(participants)

    id_list                         = [p['idx'] for p in (new_participants.values())]

    for idx in id_list:             # For loop is important here, because the participants have to act sequentially

        new_participants            = determine_initial_conditions(new_participants, layout_zone, conciliation_quota, critical_amount)  # Each participant gets the currrent position of all other blocks (no old information)

        A                           = new_participants.pop(idx)  

        A_rotated                   = rotate(A)
        A_rotated_conditions        = calculate_conditions(A_rotated, new_participants, layout_zone, leeway_coefficient, conciliation_quota, critical_amount)

        A_rotated                   = A_rotated | A_rotated_conditions
        
        possible_new_positions      = action_exploration(A, new_participants, layout_zone, leeway_coefficient, conciliation_quota, critical_amount)

        possible_new_positions_rot  = action_exploration(A_rotated, new_participants, layout_zone, leeway_coefficient, conciliation_quota, critical_amount)

        new_position                = determine_best_move(possible_new_positions + possible_new_positions_rot, participants, metric)


        new_participants            = new_participants | new_position


    toc                             = time.time()

    runtime                         = toc - tic

    return new_participants, runtime