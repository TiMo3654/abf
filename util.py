import random
import math
from matplotlib import pyplot as plt, patches

## Test functions

def generate_participant() -> dict:

    xmin        = random.randint(-10,100)
    ymin        = random.randint(-10,100)

    width       = random.randint(1,60)
    height      = random.randint(1,60)


    participant = {
        "idx":          "0",  
        "xmin":         xmin,
        "ymin":         ymin,
        "width":        width,
        "height":       height,
        "clashes":      {},         #{'idx' : 100}
        "aversions":    {},         #{'idx' : 17,5}
        "inference":    0,
        "connections":  {},         #{'idx' : 2}
        "turmoil":      0,
        "wounds":       [],
        "freespace":    {}
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
                  #print('Overlap at nort and east edge!')
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

def calculate_protrusion(layout_zone : dict, B : dict) -> str:  #layout zone is participant A for this function

    overlap_locations   = calculate_overlap(layout_zone, B)[1]

    if any(overlap_locations):
        if overlap_locations[0]:
            protrusion  = 'safe'
        else:
            protrusion  = 'prone'
    else:
        protrusion      = 'lost'
        
    return protrusion


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

      emphasis                = A['connections'][idx_B]

      strength                = len(A['connections']) + len(B['connections']) - 1

      distance                = calculate_euclidean_distance(A, B)

      relaxation_threshold    = calculate_relaxation_threshold(leeway_coefficient, A, B)

      if distance <= relaxation_threshold * emphasis:
            tension           = distance * strength * emphasis
      else:
            tension           = ((distance + 0.5 - relaxation_threshold * emphasis)**2 - 0.25 + relaxation_threshold * emphasis) * strength * emphasis

      return tension


def calculate_intensity(A : dict, B : dict) -> float:
    
    overlap             = calculate_overlap(A, B)[0]
    
    if overlap:
        overlap_area	= overlap['width'] * overlap['height']
        area_B			= calculate_participant_area(B)
        intensity		= overlap_area * area_B
    else:
        intensity       = 0.0       
    
    return intensity


def calculate_aversion(A : dict, B : dict) -> float:

    idx_B = B['idx']

    current_aversion    = A['aversion'][idx_B]
    current_clashes     = A['clashes'][idx_B]

    intensity           = calculate_intensity(A,B)

    new_aversion        = (current_aversion + intensity) * (current_clashes + 1)

    return new_aversion 


def calculate_trouble(A : dict, B : dict) -> float:

    overlap               = calculate_overlap(A, B)[0]

    if overlap:
        overlap_area      = overlap['width'] * overlap['height']
        idx_B             = B['idx']
        aversion          = A['aversion'][idx_B]
        area_B            = calculate_participant_area(B)
        intensity         = overlap_area * area_B
        trouble           = intensity + aversion
    else:
        trouble           = 0.0

    return trouble


def calculate_interference(A : dict, participants : dict) -> float:

    interference        = 0
       
    for idx in participants:
        trouble         = calculate_trouble(A, participants[idx])

        interference    += trouble

    return interference


def calculate_turmoil(A : dict, participants : dict, leeway_coefficient : float) -> float:

    turmoil             = 0

    for idx in participants:
        tension         = calculate_tension(leeway_coefficient, A, participants[idx])

        turmoil         += tension
    
    return turmoil


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


def calclulate_secondary_free_space(A : dict, vertex : str, participants : dict, layout_zone : dict) -> dict:   # Budging Move p.137
    
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


## MOVEMENTS

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

        x_min_new_at_center         = layout_zone['xmin'] + 0.5 * layout_zone['width'] - 0.5 * A['width']
        y_min_new_at_center         = (layout_zone['ymin'] + layout_zone['height'] - A['height'])

        x_min_new_at_right_vertex   = layout_zone['xmin'] + layout_zone['width'] - A['width']
        y_min_new_at_right_vertex   = (layout_zone['ymin'] + layout_zone['height'] - A['height'])

    elif layout_zone_edge == 'east':    # Rotate layout zone clockwise virtually for edge orientation
         
        x_min_new_at_left_vertex    = layout_zone['xmin'] + layout_zone['width'] - A['width']
        y_min_new_at_left_vertex    = (layout_zone['ymin'] + layout_zone['height'] - A['height'])

        x_min_new_at_center         = layout_zone['xmin'] + layout_zone['width'] - A['width']
        y_min_new_at_center         = (layout_zone['ymin'] + 0.5 * layout_zone['height'] -  0.5 * A['height'])

        x_min_new_at_right_vertex   = layout_zone['xmin'] + layout_zone['width'] - A['width']
        y_min_new_at_right_vertex   = layout_zone['ymin']

    elif layout_zone_edge == 'south':
         
        x_min_new_at_left_vertex    = layout_zone['xmin']
        y_min_new_at_left_vertex    = layout_zone['ymin']

        x_min_new_at_center         = layout_zone['xmin'] + 0.5 * layout_zone['width'] - 0.5 * A['width']
        y_min_new_at_center         = layout_zone['ymin']

        x_min_new_at_right_vertex   = layout_zone['xmin'] + layout_zone['width'] - A['width']
        y_min_new_at_right_vertex   = layout_zone['ymin']

    elif layout_zone_edge == 'west':    # Rotate layout zone counter-clockwise virtually for edge naming orientation
         
        x_min_new_at_left_vertex    = layout_zone['xmin']
        y_min_new_at_left_vertex    = (layout_zone['ymin'] + layout_zone['height'] - A['height'])

        x_min_new_at_center         = layout_zone['xmin']
        y_min_new_at_center         = (layout_zone['ymin'] + 0.5 * layout_zone['height'] -  0.5 * A['height'])

        x_min_new_at_right_vertex   = layout_zone['xmin']
        y_min_new_at_right_vertex   = layout_zone['ymin']

    else:
        
        print('No correct edge given!')      

    return [(x_min_new_at_left_vertex, y_min_new_at_left_vertex), (x_min_new_at_center, y_min_new_at_center), (x_min_new_at_right_vertex, y_min_new_at_right_vertex)]


def center(A: dict) -> tuple:
     
    x_min_new   = A['freespace']['xmin'] + 0.5 * A['freespace']['width']
    y_min_new   = A['freespace']['ymin'] + 0.5 * A['freespace']['height']

    return x_min_new, y_min_new








