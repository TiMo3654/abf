from util import *


def calculate_dead_space(participants : dict, layout_zone : dict) -> float:

    total_layout_area               = calculate_layout_area(layout_zone)

    widths                          = [sub_dict.get('width') for sub_dict in participants.values()]

    heights                         = [sub_dict.get('height') for sub_dict in participants.values()]

    summed_participants_area        = sum([a * b for a, b in zip(widths, heights)])

    
    dead_space                      = 100 - (summed_participants_area/total_layout_area)*100

    return dead_space