# Interaction control
import copy

def scale_layout_zone_linear(layout_zone : dict, scaling_factor : float) -> dict:

    new_layout_zone             = copy.deepcopy(layout_zone)

    new_layout_zone['width']    = layout_zone['width'] * scaling_factor

    new_layout_zone['height']   = layout_zone['height'] * scaling_factor

    return new_layout_zone