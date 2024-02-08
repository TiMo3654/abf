# Interaction control
import copy
import math

def scale_layout_zone(layout_zone : dict, scaling_factor : float) -> dict:

    new_layout_zone             = copy.deepcopy(layout_zone)

    new_layout_zone['width']    = layout_zone['width'] * scaling_factor

    new_layout_zone['height']   = layout_zone['height'] * scaling_factor

    return new_layout_zone



def reset_after_tightening(participants : dict) -> dict:

    reset_participants                          = copy.deepcopy(participants)
        
    id_list                                     = [p['idx'] for p in (reset_participants.values())]


    for idx in id_list:

        reset_participants[idx]['aversions']    = {}
        reset_participants[idx]['clashes']      = {}
        

    return reset_participants