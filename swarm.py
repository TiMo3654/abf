from util import *
from moves import *
from exploration import *
from conditions import *
from interaction import *
from collections import namedtuple

import time

def determine_initial_conditions(participants : namedtuple, layout_zone : namedtuple, conciliation_quota : float, critical_amount : int) -> namedtuple:

    leeway_coefficient          = calculate_leeway_coefficient(layout_zone, participants)

    participants_updated_dict   = {A. idx : calculate_conditions(A, participants, layout_zone, leeway_coefficient, conciliation_quota, critical_amount) for A in participants}

    participants_updated        = participants._replace(**participants_updated_dict)

    return participants_updated



def one_round_of_interaction(participants : namedtuple, layout_zone : namedtuple, metric : str, conciliation_quota : float, critical_amount : int) -> namedtuple:

    tic                             = time.time()

    leeway_coefficient              = calculate_leeway_coefficient(layout_zone, participants)

    new_participants                = participants


    for A in participants:             # For loop is important here, because the participants have to act sequentially

        new_participants            = determine_initial_conditions(new_participants, layout_zone, conciliation_quota, critical_amount)  # Each participant gets the currrent position of all other blocks (no old information)

        A_rotated                   = rotate(A)
        A_rotated_updated           = calculate_conditions(A_rotated, new_participants, layout_zone, leeway_coefficient, conciliation_quota, critical_amount)

        
        possible_new_positions      = action_exploration(A, new_participants, layout_zone, leeway_coefficient, conciliation_quota, critical_amount)

        possible_new_positions_rot  = action_exploration(A_rotated_updated, new_participants, layout_zone, leeway_coefficient, conciliation_quota, critical_amount)

        new_position                = determine_best_move(possible_new_positions + possible_new_positions_rot, metric)

        moved_participants_dict     = {p.idx : p for p in new_position}

        new_participants            = new_participants._replace(**moved_participants_dict)


    toc                             = time.time()

    runtime                         = toc - tic

    return new_participants, runtime