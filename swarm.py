from util import *
from moves import *
from exploration import *
from conditions import *
from interaction import *

import copy

def one_round_of_interaction(participants : dict, layout_zone : dict, conciliation_quota : float, critical_amount : int) -> dict:

    leeway_coefficient          = calculate_leeway_coefficient(layout_zone, participants)

    new_participants            = copy.deepcopy(participants)

    for i in range(len(participants)):

        A                       = new_participants.pop(str(i))  # TODO: Handle idx list instead of basic ascending numbers

        possible_new_positions  = action_exploration(A, new_participants, layout_zone, leeway_coefficient, conciliation_quota, critical_amount)

        new_position            = determine_best_move(possible_new_positions)

        for moved_participant in new_position:
            
            new_participants.update({moved_participant['idx'] : moved_participant})      

    return new_participants