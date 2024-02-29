from util import *
from collections import namedtuple

def calculate_dead_space(participants : namedtuple, layout_zone : namedtuple) -> float:

    total_layout_area               = calculate_area(layout_zone)

    widths                          = [p.width for p in participants]

    heights                         = [p.height for p in participants]

    summed_participants_area        = sum([a * b for a, b in zip(widths, heights)])

    
    dead_space                      = 100 - (summed_participants_area/total_layout_area)*100

    return dead_space