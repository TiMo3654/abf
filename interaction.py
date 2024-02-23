# Interaction control
import copy
import math

from collections import namedtuple

def scale_layout_zone(layout_zone : namedtuple, scaling_factor : float) -> dict:

    new_layout_zone = layout_zone._replace(width = layout_zone.width * scaling_factor, height = layout_zone.height * scaling_factor)

    return new_layout_zone



def reset_after_tightening(participants : set) -> set:

    reset_participants = {p._replace(aversions = {}, clashes = {}) for p in participants}        

    return reset_participants