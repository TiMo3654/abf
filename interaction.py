# Interaction control
import copy
import math

from collections import namedtuple

def scale_layout_zone(layout_zone : namedtuple, scaling_factor : float) -> dict:

    new_layout_zone = layout_zone._replace(width = layout_zone.width * scaling_factor, height = layout_zone.height * scaling_factor)

    return new_layout_zone



def reset_after_tightening(participants : namedtuple) -> namedtuple:

    # Create defaults for clashes and aversion

    idx_list            = [p.idx for p in participants]
    idx_str             = ' '.join(idx_list)

    Clashes             = namedtuple('Clashes', idx_str)

    Aversions           = namedtuple('Aversions', idx_str)

    clashes_default     = Clashes(*(len(participants) * [0]))

    aversions_default   = Aversions(*(len(participants) * [0]))

    # Insert default values

    reset_participants  = {p.idx : p._replace(aversions = aversions_default, clashes = clashes_default) for p in participants}

    all_participants    = participants._replace(**reset_participants)

    return all_participants