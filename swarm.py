from util import *
from moves import *
from exploration import *
from conditions import *
from interaction import *
from collections import namedtuple

import time

def determine_initial_conditions(participants : set, layout_zone : namedtuple, conciliation_quota : float, critical_amount : int) -> set:

    leeway_coefficient          = calculate_leeway_coefficient(layout_zone, participants)

    participants_updated        = set([calculate_conditions(A, participants, layout_zone, leeway_coefficient, conciliation_quota, critical_amount) for A in participants])

    return participants_updated



def one_round_of_interaction(participants : set, layout_zone : namedtuple, metric : str, conciliation_quota : float, critical_amount : int) -> set:

    tic                             = time.time()

    leeway_coefficient              = calculate_leeway_coefficient(layout_zone, participants)


    for A in participants:             # For loop is important here, because the participants have to act sequentially

        new_participants            = determine_initial_conditions(new_participants, layout_zone, conciliation_quota, critical_amount)  # Each participant gets the currrent position of all other blocks (no old information)

        A_rotated                   = rotate(A)
        A_rotated_updated           = calculate_conditions(A_rotated, new_participants, layout_zone, leeway_coefficient, conciliation_quota, critical_amount)

        
        possible_new_positions      = action_exploration(A, new_participants, layout_zone, leeway_coefficient, conciliation_quota, critical_amount)

        possible_new_positions_rot  = action_exploration(A_rotated, new_participants, layout_zone, leeway_coefficient, conciliation_quota, critical_amount)

        new_position                = determine_best_move(possible_new_positions + possible_new_positions_rot, participants, metric)

        moved_participants_ids      = [p.idx for p in new_position]

        new_participants            = set([p for p in participants if p.idx not in moved_participants_ids] + new_position)


    toc                             = time.time()

    runtime                         = toc - tic

    return new_participants, runtime