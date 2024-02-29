# Interaction control
import copy
import math

from collections import namedtuple

def scale_layout_zone(layout_zone : namedtuple, scaling_factor : float) -> dict:

    new_layout_zone = layout_zone._replace(width = layout_zone.width * scaling_factor, height = layout_zone.height * scaling_factor)

    return new_layout_zone



def reset_after_tightening(participants : namedtuple) -> namedtuple:

    reset_participants  = [p._replace(aversions = (), clashes = ()) for p in participants]  

    idx_list            = [p['idx'] for p in participants]
    idx_str             = ' '.join(idx_list)  

    Participants        = namedtuple('Participants', idx_str)

    all_participants    = Participants(*reset_participants)

    return all_participants