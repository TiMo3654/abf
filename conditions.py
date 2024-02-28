## SWARM specifics   

import math
import time

from collections import namedtuple

from util import *

def calculate_health(A : namedtuple, B : namedtuple, overlap : namedtuple) -> bool:

    if overlap:
        
        healthy = B.healthy  # in case of an overlap with a healthy other one, A is also healthy otherwise not

    else:
        
        healthy = True          # in case of no overlap, A is also healthy in this check

    return healthy    


def calculate_protrusion(layout_zone : namedtuple, B : namedtuple) -> tuple:  #layout zone is participant A for this function

    overlap, locations          = calculate_overlap(layout_zone, B)

    west_edge_overlap           = locations[2]
    south_edge_overlap          = locations[5]

    if any(locations):
        if locations[0]:
            protrusion          = 'safe'

            protrusion_extend   = (0,0)

        else:
            protrusion          = 'prone'

            protrusion_extend_x = (B.width - overlap.width)   if west_edge_overlap    else (B.width - overlap.width) * -1       # negative in case of east edge, else zero (0 in the brackets in case of pure north or south overlap)
            protrusion_extend_y = (B.height - overlap.height) if south_edge_overlap   else (B.height - overlap.height) * -1     # negative in case of north edge, else zero

            protrusion_extend   = (protrusion_extend_x, protrusion_extend_y)

    else:
        protrusion              = 'lost'

        protrusion_extend       = (0,0)
        
    return protrusion, protrusion_extend, locations[2:]   # The protrusion extend is signed and can therefore be simply added to the origin of a rectangle to correct a prone state


def calculate_leeway_coefficient(layout_zone : namedtuple, participants : set) -> float:                         # Equation 7.33 p. 120

    total_layout_area             = calculate_area(layout_zone)

    summed_participants_area      = calculate_all_participants_area(participants)

    leeway_coeffcient             = math.sqrt(total_layout_area/summed_participants_area)

    return leeway_coeffcient


def calculate_relaxation_threshold(leeway_coeffcient : float, A : namedtuple, B : namedtuple, emphasis : int) -> float:                 # Equation 7.42 p. 121

    area_A                  = calculate_area(A)
    area_B                  = calculate_area(B)

    relaxation_threshold    = (leeway_coeffcient/(math.sqrt(2) * emphasis)) * (math.sqrt(area_A) + math.sqrt(area_B))

    return relaxation_threshold


def calculate_tension(leeway_coefficient : float, A : namedtuple, B : namedtuple) -> tuple:                             # Equation 7.48 p 122

    emphasis                    = getattr(A.connections, B.idx, 0)

    if emphasis:

        strength                = len(A.connections) + len(B.connections) - 1

        distance                = calculate_euclidean_distance(A, B)

        relaxation_threshold    = calculate_relaxation_threshold(leeway_coefficient, A, B, emphasis)

        if distance <= relaxation_threshold * emphasis:
            tension             = distance * strength * emphasis
        else:
            tension             = ((distance + 0.5 - relaxation_threshold * emphasis)**2 - 0.25 + relaxation_threshold * emphasis) * strength * emphasis

        
        connection_relaxed      = (distance <= relaxation_threshold)    

    else:

        tension                 = 0.0
        connection_relaxed      = False  

    return tension, connection_relaxed


def calculate_clashes(A : namedtuple, B : namedtuple, overlap : namedtuple) -> tuple:

    previous_clashes    = getattr(A.clashes, B.idx)

    new_clashes         = previous_clashes + 1 if overlap else previous_clashes

    return (B.idx, new_clashes)


def calculate_intensity(A : namedtuple, B : namedtuple, overlap : namedtuple) -> float:
       
    if overlap:

        overlap_area	= calculate_area(overlap)
        area_B			= calculate_area(B)
        intensity		= overlap_area * area_B

    else:

        intensity       = 0.0       
    
    return intensity


def calculate_aversion(A : namedtuple, B : namedtuple, overlap : namedtuple, conciliation_quota : float) -> tuple:

    intensity           = calculate_intensity(A,B, overlap)

    previous_clashes    = getattr(A.clashes, B.idx)
    previous_aversion   = getattr(A.aversions, B.idx)

    if overlap:

        new_aversion    = (previous_aversion + intensity) * (previous_clashes + 1)
    
    else:
        
        new_aversion    = previous_aversion * conciliation_quota


    return (B.idx, new_aversion)


def calculate_trouble(A : namedtuple, B : namedtuple, overlap : namedtuple) -> float:

    if overlap:

        aversion          = getattr(A.aversions, B.idx)         #TODO: Check if the reihenfolge passt
        intensity         = calculate_intensity(A,B,overlap)
        trouble           = intensity + aversion

    else:

        trouble           = 0.0

    return trouble



def calculate_corridor(A : namedtuple, layout_zone : namedtuple, edge : str) -> namedtuple:
    
    if edge == "north":

        corridor   = Rectangle(A.xmin, A.ymin + A.height, A.width, layout_zone.height - (A.ymin + A.height))
    
    elif edge == "west":

        corridor   = Rectangle(layout_zone.xmin, A.ymin, A.xmin, A.height)

    elif edge == "east":

        corridor   = Rectangle(A.xmin + A.width, A.ymin, layout_zone.width - (A.xmin + A.width))

    elif edge == "south":
        corridor   = Rectangle(A.xmin, layout_zone.ymin, A.width, A.ymin)

    else:
        corridor = ()
        print('No correct edge received!')

    return corridor    


def calclulate_free_space(A : namedtuple, free_edges : list, participants : set, layout_zone : namedtuple) -> namedtuple:

    if free_edges:

        overlaps                    = [calculate_overlap(calculate_corridor(A, layout_zone, edge), B)[0] for B in participants if B.idx != A.idx for edge in free_edges]

        overlaps_filtered           = [overlap for overlap in overlaps if overlap]  # filter out empty tuples


        northern_boundary           = [overlap.ymin                     for overlap in overlaps_filtered if overlap.ymin > A.ymin + A.height]

        western_boundary            = [overlap.xmin + overlap.width     for overlap in overlaps_filtered if overlap.xmin + overlap.width < A.xmin]

        eastern_boundary            = [overlap.xmin                     for overlap in overlaps_filtered if overlap.xmin > A.xmin + A.width]

        southern_boundary           = [overlap.ymin + overlap.height    for overlap in overlaps_filtered if overlap.ymin + overlap.height < A.ymin]


        northern_freespace_border   = min(northern_boundary)    if northern_boundary    else (layout_zone.ymin + layout_zone.height)    if 'north'  in free_edges  else A.ymin + A.height

        western_freespace_border    = max(western_boundary)     if western_boundary     else (layout_zone.xmin)                         if 'west'   in free_edges  else A.xmin

        eastern_freespace_border    = min(eastern_boundary)     if eastern_boundary     else (layout_zone.xmin + layout_zone.width)     if 'east'   in free_edges  else A.xmin + A.width

        southern_freespace_border   = max(southern_boundary)    if southern_boundary    else (layout_zone.ymin)                         if 'south'  in free_edges  else A.ymin

        free_space                  = Rectangle(western_freespace_border, southern_freespace_border, eastern_freespace_border - western_freespace_border, northern_freespace_border - southern_freespace_border)


    else:

        free_space                  = ()                                           


    return free_space


def calculate_secondary_free_space(A                                        : namedtuple
                                   , vertex                                 : tuple
                                   , horizontal_south_inline_participants   : list
                                   , horizontal_north_inline_participants   : list
                                   , vertical_west_inline_participants      : list
                                   , vertical_east_inline_participants      : list
                                   , layout_zone                            : namedtuple) -> namedtuple:   # Budging Move p.137

    corner_x                                = A.xmin    if vertex[0] == 'left'      else A.xmin + A.width
    corner_y                                = A.ymin    if vertex[1] == 'bottom'    else A.ymin + A.height

    # Catch cases when there are no other participants in line -> Set layout zone as border

    horizontal_south_inline_participants_f   = horizontal_south_inline_participants  if horizontal_south_inline_participants     else [(layout_zone.xmin + layout_zone.width, layout_zone.xmin )]
    horizontal_north_inline_participants_f   = horizontal_north_inline_participants  if horizontal_north_inline_participants     else [(layout_zone.xmin + layout_zone.width, layout_zone.xmin )]
    vertical_west_inline_participants_f      = vertical_west_inline_participants     if vertical_west_inline_participants        else [(layout_zone.ymin + layout_zone.height, layout_zone.ymin)]
    vertical_east_inline_participants_f      = vertical_east_inline_participants     if vertical_east_inline_participants        else [(layout_zone.ymin + layout_zone.height, layout_zone.ymin)]

    # Calculate border

    lower_border_vertical                   = max([lb[1] for lb in vertical_west_inline_participants_f if lb[1] < corner_y]) if vertex[0] == 'left' else max([lb[1] for lb in vertical_east_inline_participants_f if lb[1] < corner_y])
    upper_border_vertical                   = min([ub[0] for ub in vertical_west_inline_participants_f if ub[0] > corner_y]) if vertex[0] == 'left' else min([ub[0] for ub in vertical_east_inline_participants_f if ub[0] > corner_y])


    left_border_horizontal                  = max([lb[1] for lb in horizontal_south_inline_participants_f if lb[1] < corner_x]) if vertex[1] == 'bottom' else max([lb[1] for lb in horizontal_north_inline_participants_f if lb[1] < corner_x])
    right_border_horizontal                 = min([rb[0] for rb in horizontal_south_inline_participants_f if rb[0] > corner_x]) if vertex[1] == 'bottom' else min([rb[0] for rb in horizontal_north_inline_participants_f if rb[0] > corner_x])


    secondary_free_space                    = Rectangle(left_border_horizontal, lower_border_vertical, right_border_horizontal - left_border_horizontal, upper_border_vertical - lower_border_vertical)
               
    
    return secondary_free_space


def calclulate_all_secondary_free_spaces(A : dict, free_vertices : list, participants : dict, layout_zone : dict) -> tuple:

    hsip                            = [(B.ymin, B.ymin + B.heigth)  for B in participants if B.ymin <= A.ymin <= B.ymin + B.height]

    hnip                            = [(B.ymin, B.ymin + B.heigth)  for B in participants if B.ymin <= A.ymin + A.height <= B.ymin + B.height]

    vwip                            = [(B.xmin, B.xmin + B.width)   for B in participants if B.xmin <= A.xmin <= B.xmin + B.width]

    veip                            = [(B.xmin, B.xmin + B.width)   for B in participants if B.xmin <= A.xmin + A.width <= B.xmin + B.width]
     
    secondary_free_space_north_west = calculate_secondary_free_space(A, ('left', 'top'), hsip, hnip, vwip, veip, participants, layout_zone) if ('left', 'top') in free_vertices else ()

    secondary_free_space_north_east = calculate_secondary_free_space(A, ('right', 'top'), hsip, hnip, vwip, veip, participants, layout_zone) if ('right', 'top') in free_vertices else ()

    secondary_free_space_south_east = calculate_secondary_free_space(A, ('right', 'bottom'), hsip, hnip, vwip, veip, participants, layout_zone) if ('right', 'bottom') in free_vertices else ()

    secondary_free_space_south_west = calculate_secondary_free_space(A, ('left', 'bottom'), hsip, hnip, vwip, veip, participants, layout_zone) if ('left', 'bottom') in free_vertices else ()

    return secondary_free_space_north_west, secondary_free_space_north_east, secondary_free_space_south_east, secondary_free_space_south_west


def calculate_yield_polygon(A : namedtuple, participants : set, layout_zone : namedtuple) -> namedtuple:     # For yield (here called "yielt") move p. 141

    northern_boundary   = []
    western_boundary    = []
    southern_boundary   = []
    eastern_boundary    = []

    for idx in participants:
        
        B                   = participants[idx]

        overlap, locations  = calculate_overlap(A, B)

        B_fully_encloses_A  = locations[1]
        west_edge_overlap   = locations[2]
        east_edge_overlap   = locations[3]
        north_edge_overlap  = locations[4]
        south_edge_overlap  = locations[5]

        if not B_fully_encloses_A:

            wb  = (overlap['xmin'] + overlap.width)  if west_edge_overlap    else (A['xmin'])

            eb  = (overlap['xmin'])                     if east_edge_overlap    else (A['xmin'] + A.width)

            nb  = (overlap['ymin'])                     if north_edge_overlap   else (A['ymin'] + A.height)

            sb  = (overlap['ymin'] + overlap.height) if south_edge_overlap   else (A['ymin'])

            western_boundary.append(wb)
            eastern_boundary.append(eb)
            northern_boundary.append(nb)
            southern_boundary.append(sb)

        else:
            
            return {}   # No yield polygon can be calculated in case of A beeing fully enclosed by B
        

    yield_polygon    = {
    'xmin'     : max(western_boundary),
    'ymin'     : max(southern_boundary),
    'width'    : min(eastern_boundary) - max(western_boundary),
    'height'   : min(northern_boundary) - max(southern_boundary)
    }     

    return yield_polygon


def calculate_compliance(A : dict) -> bool:
     
    # placeholder

    return True

    
def calculate_lateral_condition(A: namedtuple, B : namedtuple, leeway_coeffcient : float, conciliation_quota : float, critical_amount : int) -> tuple:

    overlap, locations          = calculate_overlap(A, B)

    free_edges                  = [not elem for elem in locations][2:]  # location has True for non free edges

    clashes                     = calculate_clashes(A, B, overlap)

    aversion                    = calculate_aversion(A, B, overlap, conciliation_quota)

    trouble                     = calculate_trouble(A, B, overlap)

    tension, relaxed_connection	= calculate_tension(leeway_coeffcient, A, B)

    
    return Lateral_Conditions(B.idx, overlap, free_edges, clashes, aversion, trouble, tension, relaxed_connection) 




def calculate_conditions(A : namedtuple, participants : set, layout_zone : namedtuple, leeway_coeffcient : float, conciliation_quota : float, critical_amount : int) -> namedtuple:

    tic                 = time.time()

    lateral_conditions  = [calculate_lateral_condition(A, B, leeway_coeffcient, conciliation_quota, critical_amount) for B in participants if B.idx != A.idx]

    # determine overlapping participants

    overlap_with_idx    = set([cond.idx for cond in lateral_conditions if cond.overlap])

    # determine free edges

    masks_edges         = [cond.locations for cond in lateral_conditions]

    free_edges_bool     = [all(mask[i] for mask in masks_edges) for i in range(4)]

    free_edges_str      = [y for (x,y) in zip(free_edges_bool, ['west', 'east', 'north', 'south']) if x]

    # determine free vertices

    overlaps            = [cond.overlap for cond in lateral_conditions if cond.overlap]

    masks_corners       = [calculate_free_corners(A, Ov) for Ov in overlaps]

    free_vertices_bool  = [all(mask[i] for mask in masks_corners) for i in range(4)]

    free_vertices_str   = [y for (x,y) in zip(free_vertices_bool, [('left', 'top'), ('right', 'top'), ('left', 'bottom'), ('left', 'right')]) if x]

    # calculate interference

    interference        = sum([cond.trouble for cond in lateral_conditions])

    # calculate turmoil

    turmoil             = sum([cond.tension for cond in lateral_conditions])

    # count number of relaxed connections

    relaxed_connections = [cond.relaxed_connection for cond in lateral_conditions].count(True)

    # update clashes

    new_clashes         = dict([cond.clashes for cond in lateral_conditions])
    new_clashes_tuple   = namedtuple('Clashes', new_clashes)(**new_clashes)

    # update aversion

    new_aversion        = dict([cond.aversion for cond in lateral_conditions])
    new_aversions_tuple = namedtuple('Aversions', new_aversion)(**new_aversion)
    
    # Calculate compliance
        
    compliance          = calculate_compliance(A)

    # Calculate protrusion

    protrusion_status, extend, edges = calculate_protrusion(layout_zone, A)

    protruded_zone_edges             = set([edge for i,edge in enumerate(['west', 'east', 'north', 'south']) if edges[i]])

    # Calculate space values

    yield_polygon                   = () # TODO: Rethink yield function

    free_space                      = calclulate_free_space(A, free_edges_str, participants, layout_zone)

    sfs_nw, sfs_ne, sfs_se, sfs_sw  = calclulate_all_secondary_free_spaces(A, free_vertices_str, participants, layout_zone)     

    # update A

    new_A = A._replace(  clashes                = new_clashes_tuple
                       , aversions              = new_aversions_tuple
                       , interference           = interference
                       , overlap_with_idx       = overlap_with_idx
                       , turmoil                = turmoil
                       , relaxed_connections    = relaxed_connections
                       , protrusion_status      = protrusion_status
                       , protrusion_extend      = extend
                       , protruded_zone_edges   = protruded_zone_edges
                       , healthy                = True
                       , compliant              = compliance
                       , yield_polygon          = yield_polygon
                       , freespace              = free_space
                       , secondary_freespace_north_east = sfs_ne
                       , secondary_freespace_south_east = sfs_se
                       , secondary_freespace_south_west = sfs_sw
                       , secondary_freespace_north_west = sfs_nw )

    toc = time.time()

    #print('Condition Calculation took: ' + str(toc-tic))    # typ. 0.0002 seconds on PLASMA Server
    
    return new_A