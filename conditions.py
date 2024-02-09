## SWARM specifics   

import math

from util import *

def calculate_health(A : dict, B : dict, overlap : dict) -> bool:

    if overlap:
        
        healthy = B['healthy']  # in case of an overlap with a healthy other one, A is also healthy otherwise not

    else:
        
        healthy = True          # in case of no overlap, A is also healthy in this check

    return healthy    


def calculate_protrusion(layout_zone : dict, B : dict) -> tuple:  #layout zone is participant A for this function

    overlap, locations          = calculate_overlap(layout_zone, B)

    west_edge_overlap           = locations[2]
    south_edge_overlap          = locations[5]

    if any(locations):
        if locations[0]:
            protrusion          = 'safe'

            protrusion_extend   = (0,0)

        else:
            protrusion          = 'prone'

            protrusion_extend_x = (B['width'] - overlap['width'])   if west_edge_overlap    else (B['width'] - overlap['width']) * -1       # negative in case of east edge, else zero (0 in the brackets in case of pure north or south overlap)
            protrusion_extend_y = (B['height'] - overlap['height']) if south_edge_overlap   else (B['height'] - overlap['height']) * -1     # negative in case of north edge, else zero

            protrusion_extend   = (protrusion_extend_x, protrusion_extend_y)

    else:
        protrusion              = 'lost'

        protrusion_extend       = (0,0)
        
    return protrusion, protrusion_extend, locations[2:]   # The protrusion extend is signed and can therefore be simply added to the origin of a rectangle to correct a prone state


def calculate_leeway_coefficient(layout_zone : dict, participants : dict) -> float:                         # Equation 7.33 p. 120

    total_layout_area             = calculate_layout_area(layout_zone)

    summed_participants_area      = calculate_all_participants_area(participants)

    leeway_coeffcient             = math.sqrt(total_layout_area/summed_participants_area)

    return leeway_coeffcient


def calculate_relaxation_threshold(leeway_coeffcient : float, A : dict, B : dict) -> float:                 # Equation 7.42 p. 121

    idx_B                   = B['idx']

    emphasis                = A['connections'][idx_B]

    area_A                  = calculate_participant_area(A)
    area_B                  = calculate_participant_area(B)

    relaxation_threshold    = (leeway_coeffcient/(math.sqrt(2) * emphasis)) * (math.sqrt(area_A) + math.sqrt(area_B))

    return relaxation_threshold


def calculate_tension(leeway_coefficient : float, A : dict, B : dict) -> float:                             # Equation 7.48 p 122

    idx_B                   = B['idx']

    if idx_B in A['connections']:

        emphasis                = A['connections'][idx_B]

        strength                = len(A['connections']) + len(B['connections']) - 1

        distance                = calculate_euclidean_distance(A, B)

        relaxation_threshold    = calculate_relaxation_threshold(leeway_coefficient, A, B)

        if distance <= relaxation_threshold * emphasis:
            tension             = distance * strength * emphasis
        else:
            tension             = ((distance + 0.5 - relaxation_threshold * emphasis)**2 - 0.25 + relaxation_threshold * emphasis) * strength * emphasis

        
        connection_relaxed      = (distance <= relaxation_threshold)    

    else:

        tension                 = 0.0
        connection_relaxed      = False  

    return tension, connection_relaxed


def calculate_clashes(A : dict, B : dict, overlap : dict) -> int:

    idx_B               = B['idx']

    if idx_B in A['clashes']:
    
        if overlap:
            
            new_clashes = A['clashes'][idx_B] + 1
        
        else:
            
            new_clashes = A['clashes'][idx_B]

    else:

        new_clashes     = 1 if overlap else 0

    return new_clashes


def calculate_intensity(A : dict, B : dict, overlap : dict) -> float:
       
    if overlap:

        overlap_area	= overlap['width'] * overlap['height']
        area_B			= calculate_participant_area(B)
        intensity		= overlap_area * area_B

    else:

        intensity       = 0.0       
    
    return intensity


def calculate_aversion(A : dict, B : dict, overlap : dict, conciliation_quota : float) -> float:

    idx_B               = B['idx']

    intensity           = calculate_intensity(A,B, overlap)

    if idx_B in A['aversions']:

        if overlap:

            current_aversion    = A['aversions'][idx_B]
            current_clashes     = A['clashes'][idx_B]

            new_aversion        = (current_aversion + intensity) * (current_clashes + 1)
        
        else:
            
            new_aversion        = A['aversions'][idx_B] * conciliation_quota

    else:

        new_aversion            = intensity if overlap else 0.0

    return new_aversion 


def calculate_trouble(A : dict, B : dict, overlap : dict) -> float:

    if overlap:

        overlap_area      = overlap['width'] * overlap['height']
        idx_B             = B['idx']
        aversion          = A['aversions'][idx_B] if idx_B in A['aversions'] else 0.0
        intensity         = calculate_intensity(A,B,overlap)
        trouble           = intensity + aversion

    else:

        trouble           = 0.0

    return trouble



def calculate_corridor(A : dict, layout_zone : dict, edge : str) -> dict:
    
    if edge == "north":
        corridor   = {
              'xmin' :  A['xmin'],
              'ymin' :  A['ymin'] + A['height'],
              'width':  A['width'],
              'height': layout_zone['height'] - (A['ymin'] + A['height'])
        }
    elif edge == "west":
        corridor   = {
              'xmin' :  layout_zone['xmin'],
              'ymin' :  A['ymin'],
              'width':  A['xmin'],
              'height': A['height']
        }
    elif edge == "east":
        corridor   = {
              'xmin' :  A['xmin'] + A['width'],
              'ymin' :  A['ymin'],
              'width':  layout_zone['width'] - (A['xmin'] + A['width']),
              'height': A['height']
        }
    elif edge == "south":
        corridor   = {
              'xmin' :  A['xmin'],
              'ymin' :  layout_zone['ymin'],
              'width':  A['width'],
              'height': A['ymin']
        }
    else:
        corridor = {}
        print('No correct edge received!')

    return corridor    


def calclulate_free_space(A : dict, free_edges : list, participants : dict, layout_zone : dict) -> dict:

    if free_edges:

        northern_boundary   = []
        western_boundary    = []
        southern_boundary   = []
        eastern_boundary    = []

        for edge in free_edges:

            corridor   = calculate_corridor(A, layout_zone, edge)

            for idx in participants:
                
                B       = participants[idx]

                overlap, locations = calculate_overlap(corridor, B)

                # The minimum y coordinate of an overlap in the northern corridor is the northern border of A's free space
                # The minimum x coordinate of an overlap in the eastern corridor is the eastern border of A's free space
                # The maximum y coordinate of an overlap in the southern corridor is the southern border of A's free space
                # The maximum x coordinate of an overlap in the western corridor is the western border of A's free space
                # If a corridor has no overlaps, then A's free space is limited by the layout zone
                # Free space is only calculated on A's edges free of overlaps 
                # Free space is limited to the borders of the layout zone
                # In case of protrusion, all free edges have to be evaluated (also the one outside the layout area)

                if edge == 'north':
                    if overlap:
                        y_max_free_space    = overlap['ymin']
                    else:
                        y_max_free_space    = layout_zone['height']     # The algorithm enters this path when there is no object in the corridor or when this edge is outside the layout zone

                    northern_boundary.append(y_max_free_space)
                
                elif edge == 'east':
                    if overlap:
                        x_max_free_space    = overlap['xmin']
                    else:
                        x_max_free_space    = layout_zone['width']

                    eastern_boundary.append(x_max_free_space)
                
                elif edge == 'south':
                    if overlap:
                        y_min_free_space    = overlap['ymin'] + overlap['height']
                    else:
                        y_min_free_space    = layout_zone['ymin']

                    southern_boundary.append(y_min_free_space)

                elif edge == 'west':
                    if overlap:
                        x_min_free_space    = overlap['xmin'] + overlap['width']
                    else:
                        x_min_free_space    = layout_zone['xmin']

                    western_boundary.append(x_min_free_space)


        if northern_boundary:
            y_max_free_space            = min(northern_boundary)
        else:
            y_max_free_space            = A['ymin'] + A['height']   # Blocked edge in the northern direction

        if eastern_boundary:
            x_max_free_space            = min(eastern_boundary)
        else:
            x_max_free_space            = A['xmin'] + A['width']    # Blocked edge in the eastern direction

        if southern_boundary:
            y_min_free_space            = max(southern_boundary)
        else:
            y_min_free_space            = A['ymin']                 # Blocked edge in the southern direction

        if western_boundary:
            x_min_free_space            = max(western_boundary)
        else:
            x_min_free_space            = A['xmin']                 # Blocked edge in the western direction


        free_space          = {
            'xmin'    : x_min_free_space,
            'ymin'    : y_min_free_space,
            'width'   : x_max_free_space - x_min_free_space,
            'height'  : y_max_free_space - y_min_free_space
        }

    else:   # If no free edges are available, then the free space is defined as the participants current position and area to enable swap operations

        free_space          = {
            'xmin'    : A['xmin'],
            'ymin'    : A['ymin'],
            'width'   : A['width'],
            'height'  : A['height']
        }                                             


    return free_space


def calculate_secondary_free_space(A : dict, vertex : str, participants : dict, layout_zone : dict) -> dict:   # Budging Move p.137

    northern_boundary   = []
    western_boundary    = []
    southern_boundary   = []
    eastern_boundary    = []

    # Get vertex coordinates
        
    if vertex == "north-east":
        #print('Free at north-east!')

        x   = A['xmin'] + A['width']
        y   = A['ymin'] + A['height']

    elif vertex == "south-east":
        #print('Free at south-east!')

        x   = A['xmin'] + A['width']
        y   = A['ymin']

    elif vertex == 'south-west':
        #print('Free at south-west!')

        x   = A['xmin']
        y   = A['ymin']

    elif vertex == "north-west":
        #print('Free at north-west!')

        x   = A['xmin']
        y   = A['ymin'] + A['height']


    # Check for pairwise collisions

    for idx in participants:
        
        B   = participants[idx]

        B_somewhere_above_vertex            = B['ymin'] > y     # This can only be checked so easily due to the assumption, that B does not overlap the chosen vertex of A

        B_somewhere_right_of_vertex         = B['xmin'] > x     # This can only be checked so easily due to the assumption, that B does not overlap the chosen vertex of A

        vertex_vertical_cuts_edge_of_B      = (B['xmin'] <= x <= B['xmin'] + B['width'])

        vertex_horizontal_cuts_edge_of_B    = (B['ymin'] <= y <= B['ymin'] + B['height'])

        # Check upwards and downwards

        if B_somewhere_above_vertex:

            southern_boundary.append(layout_zone['ymin'])           # If B is above A, the southern boundary is automatically the layout zone minimum in this pairwise comparison
            
            if vertex_vertical_cuts_edge_of_B:
                northern_boundary.append(B['ymin'])
            else:
                northern_boundary.append(layout_zone['height'])
        
        else:

            northern_boundary.append(layout_zone['height'])         # If B is below A, the northern boundary is automatically the layout zone maximum in this pairwise comparison

            if vertex_vertical_cuts_edge_of_B:
                southern_boundary.append(B['ymin'] + B['height'])
            else:
                southern_boundary.append(layout_zone['ymin'])             
            
        # Check rightwards and leftwards
                
        if B_somewhere_right_of_vertex:

            western_boundary.append(layout_zone['xmin'])            # If B is right of A, the western boundary is automatically the layout zone minimum in this pairwise comparison
                
            if vertex_horizontal_cuts_edge_of_B:
                eastern_boundary.append(B['xmin'])
            else:
                eastern_boundary.append(layout_zone['width'])

        else:

            eastern_boundary.append(layout_zone['width'])           # If B is left of A, the eastern boundary is automatically the layout zone maximum in this pairwise comparison
            
            if vertex_horizontal_cuts_edge_of_B:
                western_boundary.append(B['xmin'] + B['width'])
            else:
                western_boundary.append(layout_zone['xmin'])

    # Get boundary values
                
    secondary_free_space    = {
            'xmin'     : max(western_boundary),
            'ymin'     : max(southern_boundary),
            'width'    : min(eastern_boundary) - max(western_boundary),
            'height'   : min(northern_boundary) - max(southern_boundary)

    }                 
    
    return secondary_free_space


def calclulate_all_secondary_free_spaces(A : dict, free_vertices : list, participants : dict, layout_zone : dict) -> tuple:
     
    secondary_free_space_north_west = calculate_secondary_free_space(A, 'north-west', participants, layout_zone) if 'north-west' in free_vertices else {}

    secondary_free_space_north_east = calculate_secondary_free_space(A, 'north-east', participants, layout_zone) if 'north-east' in free_vertices else {}

    secondary_free_space_south_east = calculate_secondary_free_space(A, 'south-east', participants, layout_zone) if 'south-east' in free_vertices else {}

    secondary_free_space_south_west = calculate_secondary_free_space(A, 'south-west', participants, layout_zone) if 'south-west' in free_vertices else {}

    return secondary_free_space_north_west, secondary_free_space_north_east, secondary_free_space_south_east, secondary_free_space_south_west


def calculate_yield_polygon(A : dict, participants : dict, layout_zone : dict) -> dict:     # For yield (here called "yielt") move p. 141

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

            wb  = (overlap['xmin'] + overlap['width'])  if west_edge_overlap    else (A['xmin'])

            eb  = (overlap['xmin'])                     if east_edge_overlap    else (A['xmin'] + A['width'])

            nb  = (overlap['ymin'])                     if north_edge_overlap   else (A['ymin'] + A['height'])

            sb  = (overlap['ymin'] + overlap['height']) if south_edge_overlap   else (A['ymin'])

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

    
    
def calculate_conditions(A : dict, participants : dict, layout_zone : dict, leeway_coeffcient : float, conciliation_quota : float, critical_amount : int) -> dict:

    free_edges              = ['north', 'east', 'south', 'west']       

    free_vertices           = ['north-west', 'north-east', 'south-east', 'south-west']

    interference            = 0.0

    turmoil                 = 0.0

    new_clashes             = A['clashes']

    new_aversions           = A['aversions']

    overlap_counter         = 0

    relaxed_connections     = 0

    one_sick_overlap        = False

    overlap_with_idx        = []


    for B in list(participants.values()):
        
        overlap, locations          = calculate_overlap(A, B)                                   # locations   = [A_fully_encloses_B, B_fully_encloses_A, west_edge_overlap, east_edge_overlap, north_edge_overlap, south_edge_overlap]

        overlap_counter             = overlap_counter + 1 if overlap else overlap_counter

        idx_B                       = B['idx']

        if overlap:
            overlap_with_idx.append(idx_B)

        A_fully_encloses_B          = locations[0]
        B_fully_encloses_A          = locations[1]
        west_edge_overlap           = locations[2]
        east_edge_overlap           = locations[3]
        north_edge_overlap          = locations[4]
        south_edge_overlap          = locations[5]

        # Determine free edges

        if B_fully_encloses_A:
            free_edges  = []
        
        if west_edge_overlap and ('west' in free_edges):
            free_edges.remove('west')

        if east_edge_overlap and ('east' in free_edges):
            free_edges.remove('east')

        if north_edge_overlap and ('north' in free_edges):
            free_edges.remove('north')

        if south_edge_overlap and ('south' in free_edges):
            free_edges.remove('south')

        # Determine free vertices
            
        if north_edge_overlap and west_edge_overlap and ('north-west' in free_vertices):    # Upper left
            free_vertices.remove('north-west')
        
        if north_edge_overlap and east_edge_overlap and ('north-east' in free_vertices):
            free_vertices.remove('north-east')

        if south_edge_overlap and east_edge_overlap and ('south-east' in free_vertices):
            free_vertices.remove('south-east')

        if south_edge_overlap and west_edge_overlap and ('south-west' in free_vertices):
            free_vertices.remove('south-west')

        # Calculate interference
        

        clashes                     = calculate_clashes(A, B, overlap)

        new_clashes[idx_B]          = clashes

        aversion                    = calculate_aversion(A, B, overlap, conciliation_quota)

        new_aversions[idx_B]        = aversion
            
        trouble                     = calculate_trouble(A, B, overlap)
            
        interference                = interference + trouble

        # Calculate turmoil

        tension, connection_relaxed	= calculate_tension(leeway_coeffcient, A, B)

        turmoil                     = turmoil + tension

        relaxed_connections         = relaxed_connections + 1 if connection_relaxed else relaxed_connections

        # Calculate health

        healthy                     = calculate_health(A, B, overlap) and (overlap_counter < critical_amount) and not one_sick_overlap
            
        if not healthy:    
            one_sick_overlap        = True

    
    # Calculate compliance
        
    compliance                      = calculate_compliance(A)

    # Calculate protrusion

    protrusion_status, extend, edges = calculate_protrusion(layout_zone, A)

    protruded_zone_edges             = [edge 
                                        for i,edge in enumerate(['west', 'east', 'north', 'south']) 
                                        if edges[i]]

    # Calculate space values

    yield_polygon                   = calculate_yield_polygon(A, participants, layout_zone)

    free_space                      = calclulate_free_space(A, free_edges, participants, layout_zone)

    sfs_nw, sfs_ne, sfs_se, sfs_sw  = calclulate_all_secondary_free_spaces(A, free_vertices, participants, layout_zone)     

    conditions  = {
                    "clashes"                       : new_clashes,
                    "aversions"                     : new_aversions,
                    "interference"                  : interference,
                    "overlap-with-idx"              : overlap_with_idx,
                    "turmoil"                       : turmoil,
                    "relaxed-connections"           : relaxed_connections,
                    "protrusion-status"             : protrusion_status,
                    "protrusion-extend"             : extend,
                    "protruded-zone-edges"          : protruded_zone_edges,
                    "healthy"                       : healthy,
                    "compliant"                     : compliance,
                    "yield-polygon"                 : yield_polygon,
                    "freespace"                     : free_space,
                    'secondary-freespace-north-east': sfs_ne,
                    'secondary-freespace-south-east': sfs_se,
                    'secondary-freespace-south-west': sfs_sw,
                    'secondary-freespace-north-west': sfs_nw
    }
    
    return conditions