import random
import math
import copy
from matplotlib import pyplot as plt, patches

## Test functions

def generate_participant() -> dict:

    xmin        = random.randint(-10,100)
    ymin        = random.randint(-10,100)

    width       = random.randint(1,60)
    height      = random.randint(1,60)


    participant = {
        "idx"                           : "0",  
        "connections"                   : {},         #{'idx' : 2}
        "xmin"                          : xmin,
        "ymin"                          : ymin,
        "width"                         : width,
        "height"                        : height,
        "clashes"                       : {},         #{'idx' : 100}
        "aversions"                     : {},         #{'idx' : 17,5}
        "interference"                  : 0,
        "turmoil"                       : 0,
        "relaxed-connections"           : 0,
        "protrusion-status"             : 'safe',
        "healthy"                       : True,
        "compliant"                     : True,
        "yield-polygon"                 : {},
        "freespace"                     : {},
        'secondary-freespace-north-east': {},
        'secondary-freespace-south-east': {},
        'secondary-freespace-south-west': {},
        'secondary-freespace-north-west': {},
        "last-move"                     : 'center'
    }

    return participant


def plot_participants(participants):

    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True

    colors = ['blue', 'orange', 'black']

    figure, ax = plt.subplots(1)
    ax.plot([0], c='white')

    i = 0

    for key in participants:

        p = participants[key]

        origin = (p['xmin'], p['ymin'])

        rectangle = patches.Rectangle(origin, p['width'], p['height'], edgecolor=colors[i],
        facecolor=colors[i], linewidth=1)

        i += 1

        ax.add_patch(rectangle)

    plt.ylim(0,120)
    plt.xlim(0,120)

    plt.grid()
    plt.show()

    return 0

## Geometric relationships


def calculate_overlap(A : dict, B : dict) -> tuple:

    x_A_min             = A['xmin']
    y_A_min             = A['ymin']
    x_A_max             = A['xmin'] + A['width']
    y_A_max             = A['ymin'] + A['height']

    x_B_min             = B['xmin']
    y_B_min             = B['ymin']
    x_B_max             = B['xmin'] + B['width']
    y_B_max             = B['ymin'] + B['height']

    # Determine overlap direction (multiple can be true)

    if  (x_A_min >= x_B_max or x_A_max <= x_B_min) or (y_A_min >= y_B_max or y_A_max <= y_B_min):    # No horizontal or vertical overlap

        overlapped          = False
        locations           = [False, False, False, False, False, False]

    else:

        overlapped        = True
        
        if  ( (x_A_min <= x_B_min <= x_A_max) and (x_A_min <= x_B_max <= x_A_max) and 
                (y_A_min <= y_B_min <= y_A_max) and (y_A_min <= y_B_max <= y_A_max) ):
                    A_fully_encloses_B = True
        else:
                    A_fully_encloses_B = False

        if  ( (x_B_min <= x_A_min <= x_B_max) and (x_B_min <= x_A_max <= x_B_max) and 
                (y_B_min <= y_A_min <= y_B_max) and (y_B_min <= y_A_max <= y_B_max) ):
                    B_fully_encloses_A = True
        else:
                    B_fully_encloses_A = False

        if  x_A_min > x_B_min and x_A_min < x_B_max:
                    west_edge_overlap = True
        else:
                    west_edge_overlap = False

        if  x_A_max > x_B_min and x_A_max < x_B_max:
                    east_edge_overlap = True
        else:
                    east_edge_overlap = False

        if  y_A_max > y_B_min and y_A_max < y_B_max:
                    north_edge_overlap = True
        else:
                    north_edge_overlap = False

        if  y_A_min > y_B_min and y_A_min < y_B_max:
                    south_edge_overlap = True
        else:
                    south_edge_overlap = False
        
        locations   = [A_fully_encloses_B, B_fully_encloses_A, west_edge_overlap, east_edge_overlap, north_edge_overlap, south_edge_overlap]

# Determine overlap coordinates

    if not overlapped:
        overlap = {}
        #print("party!")
    else:
        if A_fully_encloses_B:
                #print('A fully encloses B!')
                x_Overlap_min = x_B_min
                x_Overlap_max = x_B_max
                y_Overlap_min = y_B_min
                y_Overlap_max = y_B_max
        elif B_fully_encloses_A:
                #print('B fully encloses A!')
                x_Overlap_min = x_A_min
                x_Overlap_max = x_A_max
                y_Overlap_min = y_A_min
                y_Overlap_max = y_A_max
        elif north_edge_overlap and east_edge_overlap and west_edge_overlap:
                #print('Overlap at north, east and west edge!')
                x_Overlap_min = x_A_min
                x_Overlap_max = x_A_max
                y_Overlap_min = y_B_min
                y_Overlap_max = y_A_max
        elif north_edge_overlap and east_edge_overlap and south_edge_overlap:
                #print('Overlap at north, east and south edge!')
                x_Overlap_min = x_A_min
                x_Overlap_max = x_B_max
                y_Overlap_min = y_A_min
                y_Overlap_max = y_A_max
        elif north_edge_overlap and west_edge_overlap and south_edge_overlap:
                #print('Overlap at north, west and south edge!')
                x_Overlap_min = x_B_min
                x_Overlap_max = x_A_max
                y_Overlap_min = y_A_min
                y_Overlap_max = y_B_max
        elif south_edge_overlap and east_edge_overlap and west_edge_overlap:
                #print('Overlap at south, east and west edge!')
                x_Overlap_min = x_A_min
                x_Overlap_max = x_A_max
                y_Overlap_min = y_A_min
                y_Overlap_max = y_B_max
        elif north_edge_overlap and east_edge_overlap:
                #print('Overlap at north and east edge!')
                x_Overlap_min = x_B_min
                x_Overlap_max = x_A_max
                y_Overlap_min = y_B_min
                y_Overlap_max = y_A_max
        elif north_edge_overlap and west_edge_overlap:
                #print('Overlap at north and west edge!')
                x_Overlap_min = x_A_min
                x_Overlap_max = x_B_max
                y_Overlap_min = y_B_min
                y_Overlap_max = y_A_max
        elif north_edge_overlap and south_edge_overlap:
                #print('Overlap at north and south edge!')
                x_Overlap_min = x_B_min
                x_Overlap_max = x_B_max
                y_Overlap_min = y_A_min
                y_Overlap_max = y_A_max
        elif south_edge_overlap and east_edge_overlap:
                #print('Overlap at south and east edge!')
                x_Overlap_min = x_B_min
                x_Overlap_max = x_A_max
                y_Overlap_min = y_A_min
                y_Overlap_max = y_B_max
        elif south_edge_overlap and west_edge_overlap:
                #print('Overlap at south and west edge!')
                x_Overlap_min = x_A_min
                x_Overlap_max = x_B_max
                y_Overlap_min = y_A_min
                y_Overlap_max = y_B_max
        elif east_edge_overlap and west_edge_overlap:
                #print('Overlap at east and west edge')
                x_Overlap_min = x_A_min
                x_Overlap_max = x_A_max
                y_Overlap_min = y_B_min
                y_Overlap_max = y_B_max
        elif north_edge_overlap:
                #print('Overlap at north edge!')
                x_Overlap_min = x_B_min
                x_Overlap_max = x_B_max
                y_Overlap_min = y_B_min
                y_Overlap_max = y_A_max
        elif east_edge_overlap:
                #print('Overlap at east edge!')
                x_Overlap_min = x_B_min
                x_Overlap_max = x_A_max
                y_Overlap_min = y_B_min
                y_Overlap_max = y_B_max
        elif south_edge_overlap:
                #print('Overlap at south edge!')
                x_Overlap_min = x_B_min
                x_Overlap_max = x_B_max
                y_Overlap_min = y_A_min
                y_Overlap_max = y_B_max
        elif west_edge_overlap:
                #print('Overlap at west edge!')
                x_Overlap_min = x_A_min
                x_Overlap_max = x_B_max
                y_Overlap_min = y_B_min
                y_Overlap_max = y_B_max       

        overlap_width       = x_Overlap_max - x_Overlap_min
    
        overlap_height      = y_Overlap_max - y_Overlap_min

        overlap             = { "xmin"   : x_Overlap_min,
                                "ymin"   : y_Overlap_min,
                                "width"  : overlap_width,
                                "height" : overlap_height}
        
    return overlap, locations
    

def calculate_participant_area(A : dict) -> float:

    return A['width'] * A['height']


def calculate_layout_area(layout_zone : dict) -> float:

    total_layout_area = layout_zone['width'] * layout_zone['height']      

    return total_layout_area


def calculate_euclidean_distance(A : dict, B : dict) -> float:

    center_A_x  = A['xmin'] + 0.5 * A['width']

    center_A_y  = A['ymin'] + 0.5 * A['height']

    center_B_x  = B['xmin'] + 0.5 * B['width']

    center_B_y  = B['ymin'] + 0.5 * B['height']

    distance    = math.sqrt((center_A_x - center_B_x)**2 + (center_A_y - center_B_y)**2)

    return distance


## SWARM specifics   

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

            protrusion_extend   = ()

        else:
            protrusion          = 'prone'

            protrusion_extend_x = (B['width'] - overlap['width'])   if west_edge_overlap    else (B['width'] - overlap['width']) * -1       # negative in case of east edge, else zero (0 in the brackets in case of pure north or south overlap)
            protrusion_extend_y = (B['height'] - overlap['height']) if south_edge_overlap   else (B['height'] - overlap['height']) * -1     # negative in case of north edge, else zero

            protrusion_extend   = (protrusion_extend_x, protrusion_extend_y)

    else:
        protrusion              = 'lost'

        protrusion_extend       = ()
        
    return protrusion, protrusion_extend   # The protrusion extend is signed and can therefore be simply added to the origin of a rectangle to correct a prone state


def calculate_leeway_coefficient(layout_zone : dict, participants : dict) -> float:                         # Equation 7.33 p. 120

    total_layout_area             = calculate_layout_area(layout_zone)

    widths                        = [sub_dict.get('width') for sub_dict in participants.values()]

    heights                       = [sub_dict.get('height') for sub_dict in participants.values()]

    summed_participants_area      = sum([a * b for a, b in zip(widths, heights)])

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
    
    if overlap:

        idx_B       = B['idx']
        
        new_clashes = A['clashes'][idx_B] + 1
    
    else:
         
        new_clashes = A['clashes'][idx_B]

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

    if overlap:

        idx_B = B['idx']

        current_aversion    = A['aversion'][idx_B]
        current_clashes     = A['clashes'][idx_B]

        intensity           = calculate_intensity(A,B)

        new_aversion        = (current_aversion + intensity) * (current_clashes + 1)
    
    else:
        
        new_aversion        = A['aversion'][idx_B] * conciliation_quota

    return new_aversion 


def calculate_trouble(A : dict, B : dict, overlap : dict) -> float:

    if overlap:

        overlap_area      = overlap['width'] * overlap['height']
        idx_B             = B['idx']
        aversion          = A['aversion'][idx_B] if idx_B in A['aversion'] else 0.0
        area_B            = calculate_participant_area(B)
        intensity         = overlap_area * area_B
        trouble           = intensity + aversion

    else:

        trouble           = 0.0

    return trouble


# def calculate_interference(A : dict, participants : dict) -> float:

#     interference        = 0
       
#     for idx in participants:
#         trouble         = calculate_trouble(A, participants[idx])

#         interference    += trouble

#     return interference


# def calculate_turmoil(A : dict, participants : dict, leeway_coefficient : float) -> float:

#     turmoil             = 0

#     for idx in participants:
#         tension         = calculate_tension(leeway_coefficient, A, participants[idx])

#         turmoil         += tension
    
#     return turmoil


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

    else:

        free_space = {}                                             # If no free edges are available, then there is no free space


    return free_space


def calculate_secondary_free_space(A : dict, vertex : str, participants : dict, layout_zone : dict) -> dict:   # Budging Move p.137

    northern_boundary   = []
    western_boundary    = []
    southern_boundary   = []
    eastern_boundary    = []

    # Get vertex coordinates
        
    if vertex == "north-east":
        print('Free at north-east!')

        x   = A['xmin'] + A['width']
        y   = A['ymin'] + A['height']

    elif vertex == "south-east":
        print('Free at south-east!')

        x   = A['xmin'] + A['width']
        y   = A['ymin']

    elif vertex == 'south-west':
        print('Free at south-west!')

        x   = A['xmin']
        y   = A['ymin']

    elif vertex == "north-west":
        print('Free at north-west!')

        x   = A['xmin']
        y   = A['ymin'] + A['height']

    else:
        print("No correct vertex given!")

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
                northern_boundary.appen(layout_zone['height'])
        
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


    for B in participants.values:
        
        overlap, locations          = calculate_overlap(A, B)                                   # locations   = [A_fully_encloses_B, B_fully_encloses_A, west_edge_overlap, east_edge_overlap, north_edge_overlap, south_edge_overlap]

        overlap_counter             = overlap_counter + 1 if overlap else overlap_counter

        idx_B                       = B['idx']

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

        if south_edge_overlap and west_edge_overlap and ('south-east' in free_vertices):
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
            
        one_sick_overlap            = not healthy

    
    # Calculate compliance
        
    compliance                      = calculate_compliance(A)

    # Calculate protrusion

    protrusion_status, _            = calculate_protrusion(layout_zone, A)

    # Calculate space values

    yield_polygon                   = calculate_yield_polygon(A, participants, layout_zone)

    free_space                      = calclulate_free_space(A, free_edges, participants, layout_zone)

    sfs_nw, sfs_ne, sfs_se, sfs_sw  = calclulate_all_secondary_free_spaces(A, free_vertices, participants, layout_zone)     

    conditions  = {
                    "clashes"                       : new_clashes,
                    "aversions"                     : new_aversions,
                    "interference"                  : interference,
                    "turmoil"                       : turmoil,
                    "relaxed-connections"           : relaxed_connections,
                    "protrusion-status"             : protrusion_status,
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

## MOVEMENTS

def rotate(A: dict) -> tuple:

    new_width   = A['height']
    new_height  = A['width']
     
    return new_width, new_height


def reenter(A : dict, layout_zone : dict) -> tuple:                      # Only activated and working in case of a totally lost participant

    participant_left_of_layout_zone     = (A['xmin'] < layout_zone['xmin'])

    participant_right_of_layout_zone    = (A['xmin'] + A['width'] >= layout_zone['xmin'] + layout_zone['width']) # To detect if an participant is at the north eastern corner of the layout zone

    participant_above_layout_zone       = (A['ymin'] >= layout_zone['ymin'] + layout_zone['height'])
    
    participant_below_layout_zone       = (A['ymin'] < layout_zone['ymin'])

    x_min_new                           = A['xmin']

    y_min_new                           = A['ymin']

     
    x_min_new                           = layout_zone['xmin'] if participant_left_of_layout_zone else x_min_new

    x_min_new                           = (layout_zone['xmin'] + layout_zone['width'] - A['width']) if participant_right_of_layout_zone else x_min_new

    y_min_new                           = layout_zone['ymin'] if participant_below_layout_zone else y_min_new

    y_min_new                           = (layout_zone['ymin'] + layout_zone['height'] - A['height']) if participant_above_layout_zone else y_min_new     
    
    return x_min_new, y_min_new


def evade(A : dict, layout_zone : dict, layout_zone_edge : str) -> list:

    if layout_zone_edge == 'north':
         
        x_min_new_at_left_vertex    = layout_zone['xmin']
        y_min_new_at_left_vertex    = (layout_zone['ymin'] + layout_zone['height'] - A['height'])

        x_min_new_at_center         = int(layout_zone['xmin'] + 0.5 * layout_zone['width'] - 0.5 * A['width'])
        y_min_new_at_center         = (layout_zone['ymin'] + layout_zone['height'] - A['height'])

        x_min_new_at_right_vertex   = layout_zone['xmin'] + layout_zone['width'] - A['width']
        y_min_new_at_right_vertex   = (layout_zone['ymin'] + layout_zone['height'] - A['height'])

    elif layout_zone_edge == 'east':    # Rotate layout zone clockwise virtually for edge orientation
         
        x_min_new_at_left_vertex    = layout_zone['xmin'] + layout_zone['width'] - A['width']
        y_min_new_at_left_vertex    = (layout_zone['ymin'] + layout_zone['height'] - A['height'])

        x_min_new_at_center         = layout_zone['xmin'] + layout_zone['width'] - A['width']
        y_min_new_at_center         = int((layout_zone['ymin'] + 0.5 * layout_zone['height'] -  0.5 * A['height']))

        x_min_new_at_right_vertex   = layout_zone['xmin'] + layout_zone['width'] - A['width']
        y_min_new_at_right_vertex   = layout_zone['ymin']

    elif layout_zone_edge == 'south':
         
        x_min_new_at_left_vertex    = layout_zone['xmin']
        y_min_new_at_left_vertex    = layout_zone['ymin']

        x_min_new_at_center         = int(layout_zone['xmin'] + 0.5 * layout_zone['width'] - 0.5 * A['width'])
        y_min_new_at_center         = layout_zone['ymin']

        x_min_new_at_right_vertex   = layout_zone['xmin'] + layout_zone['width'] - A['width']
        y_min_new_at_right_vertex   = layout_zone['ymin']

    elif layout_zone_edge == 'west':    # Rotate layout zone counter-clockwise virtually for edge naming orientation
         
        x_min_new_at_left_vertex    = layout_zone['xmin']
        y_min_new_at_left_vertex    = (layout_zone['ymin'] + layout_zone['height'] - A['height'])

        x_min_new_at_center         = layout_zone['xmin']
        y_min_new_at_center         = int((layout_zone['ymin'] + 0.5 * layout_zone['height'] -  0.5 * A['height']))

        x_min_new_at_right_vertex   = layout_zone['xmin']
        y_min_new_at_right_vertex   = layout_zone['ymin']

    else:
        
        print('No correct edge given!')      

    return [(x_min_new_at_left_vertex, y_min_new_at_left_vertex), (x_min_new_at_center, y_min_new_at_center), (x_min_new_at_right_vertex, y_min_new_at_right_vertex)]


def center(A: dict) -> tuple:
     
    x_min_new   = int(A['freespace']['xmin'] + 0.5 * A['freespace']['width'] - 0.5 * A['width'])
    y_min_new   = int(A['freespace']['ymin'] + 0.5 * A['freespace']['height'] - 0.5 * A['height'])

    return x_min_new, y_min_new


def linger(A: dict) -> tuple:
     
    return A['xmin'], A['ymin']


def budge(A: dict, direction : str) -> tuple:   

    x_min_new       = int(A[direction]['xmin'] + 0.5 * A[direction]['width'] - 0.5 * A['width'])
    y_min_new       = int(A[direction]['ymin'] + 0.5 * A[direction]['height'] - 0.5 * A['height'])
     
    return x_min_new, y_min_new


def swap(A: dict, B: dict) -> tuple:
     
    x_min_new_A     = int(B['freespace']['xmin'] + 0.5 * B['freespace']['width'] - 0.5 * A['width'])
    y_min_new_A     = int(B['freespace']['ymin'] + 0.5 * B['freespace']['height'] - 0.5 * A['height'])

    x_min_new_B     = int(A['freespace']['xmin'] + 0.5 * A['freespace']['width'] - 0.5 * B['width'])
    y_min_new_B     = int(A['freespace']['ymin'] + 0.5 * A['freespace']['height'] - 0.5 * B['height'])

    return (x_min_new_A, y_min_new_A), (x_min_new_B, y_min_new_B)


def pair(A : dict, B : dict, pair_direction : str) -> tuple:
     
    if pair_direction == 'horizontal-push-right':
         
        x_min_new_A = int(B['xmin'] - 0.5 * A['width'])
        x_min_new_B = int(B['xmin'] + 0.5 * A['width'])

        y_min_new_A = B['ymin']
        y_min_new_B = B['ymin']

    elif pair_direction == 'horizontal-push-left':
         
        x_min_new_A = int(B['xmin'] + B['width'] - 0.5 * A['width'])
        x_min_new_B = int(B['xmin'] - 0.5 * A['width'])

        y_min_new_A = B['ymin']
        y_min_new_B = B['ymin']

    elif pair_direction == 'vertikal-push-up':
         
        x_min_new_A = B['xmin']
        x_min_new_B = B['xmin']

        y_min_new_A = int(B['ymin'] - 0.5 * A['height'])
        y_min_new_B = int(B['ymin'] + 0.5 * A['height'])

    elif pair_direction == 'vertikal-push-down':
         
        x_min_new_A = B['xmin']
        x_min_new_B = B['xmin']

        y_min_new_A = int(B['ymin'] + B['height'] - 0.5 * A['height'])
        y_min_new_B = int(B['ymin'] - 0.5 * A['height'])

    else:
        
        print('No valid pair direction!')

    return (x_min_new_A, y_min_new_A), (x_min_new_B, y_min_new_B)


def hustle(A : dict, B : dict) -> tuple:
    
    overlap, locations  = calculate_overlap(A, B)

    #print(overlap)

    if overlap['width'] <= overlap['height']:

        delta_x         = overlap['width'] if B['xmin'] >= A['xmin'] else overlap['width'] * -1
        delta_y         = 0

    else:
         
        delta_x         = 0
        delta_y         = overlap['height'] if B['ymin'] >= A['ymin'] else overlap['height'] * -1


    x_min_new_B         = B['xmin'] + delta_x

    y_min_new_B         = B['ymin'] + delta_y

    return x_min_new_B, y_min_new_B


def yielt(A : dict) -> tuple:      # Intentional typo in "yield" to avoid keyword
     
    x_center_yield_poly     = A['yield-polygon']['xmin'] + 0.5 * A['yield-polygon']['width']

    y_center_yield_poly     = A['yield-polygon']['ymin'] + 0.5 * A['yield-polygon']['height']

    x_min_new_A             = x_center_yield_poly - 0.5 * A['width']

    y_min_new_A             = y_center_yield_poly - 0.5 * A['height']
    
    return x_min_new_A, y_min_new_A


## Action exploration and evaluation

def classify_action(A : dict) -> str:
     
    if (A['protrusion-status'] == 'safe') and A['healthy'] and A['compliant'] and (A['interference'] == 0) and (A['relaxed-connections'] == len(A['connections'])):
        
        action_classification   = 'adjuvant'
    
    elif (A['protrusion-status'] == 'safe') and A['healthy'] and A['compliant']:
        
        action_classification   = 'valid'

    else:
         
        action_classification   = 'invalid'

    return action_classification


def action_exploration(A : dict, participants : dict, layout_zone : dict, leeway_coeffcient : float, conciliation_quota : float, critical_amount : int) -> list:

    possible_next_positions = []

    # start of the action exploration

    if A['protrusion-status'] == 'lost':

        new_A                           = copy.deepcopy(A)
        
        new_A['xmin'], new_A['ymin']    = reenter(new_A, layout_zone)

        moved_A_conditions              = calculate_conditions(new_A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount)

        new_A.update(moved_A_conditions)

        new_A['last-move']              = 'reenter'

        return list(new_A)

    else:   # A is prone or safe
         
        # explore centering

        new_A                           = copy.deepcopy(A)
         
        new_A['xmin'], new_A['ymin']    = center(new_A)

        moved_A_conditions              = calculate_conditions(new_A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount)

        new_A.update(moved_A_conditions)

        new_A['last-move']              = 'center'

        action_classification           = classify_action(new_A)

        if action_classification == 'adjuvant':
            
            return list(new_A)  # direct exit in case of adjuvant move
        
        elif action_classification == 'valid':
             
            possible_next_positions.append(new_A)


        # explore lingering
            
        new_A                           = copy.deepcopy(A)

        new_A['xmin'], new_A['ymin']    = linger(A)

        new_A['last-move']              = 'linger'

        action_classification           = classify_action(new_A)

        if action_classification == 'adjuvant':
            
            return list(new_A)  # direct exit in case of adjuvant move
        
        
        # explore budging, swapping, pairing, hustling only if A is safe, otherwise only centering, evasion or yielding is possible

        if A['protrusion-status'] == 'safe':

            # explore budging

            free_secondary_spaces                   = [f'secondary-free-space-{corner}' 
                                                       for corner in ['north-west', 'north-east', 'south-east', 'south-west'] 
                                                       if A[f'secondary-free-space-{corner}']]

            for direction in free_secondary_spaces:
                
                new_A                               = copy.deepcopy(A)

                new_A['xmin'], new_A['ymin']        = budge(new_A, direction)

                moved_A_conditions                  = calculate_conditions(new_A, participants, layout_zone, leeway_coeffcient, conciliation_quota, critical_amount)

                new_A['last-move']                  = 'budge'

                action_classification               = classify_action(new_A)

                if action_classification == 'adjuvant':
                    
                    return list(new_A)  # direct exit in case of adjuvant move
                
                elif action_classification == 'valid':
                    
                    possible_next_positions.append(new_A)

    return 0


def action_evaluation(possible_next_positions : list, evaluation_metric : str) -> dict:
     
    return 0




        










