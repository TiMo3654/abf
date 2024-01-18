import random
import math
from matplotlib import pyplot as plt, patches

## Test functions

def generate_participant() -> dict:

    xmin        = random.randint(1,100)
    ymin        = random.randint(1,100)

    width       = random.randint(1,60)
    height      = random.randint(1,60)


    participant = {
        "idx":          0,  
        "xmin":         xmin,
        "ymin":         ymin,
        "width":        width,
        "height":       height,
        "clashes":      {},         #{'idx' : 100}
        "aversions":    {},         #{'idx' : 17,5}
        "inference":    0,
        "connections":  {},         #{'idx' : 2}
        "turmoil":      0,
        "wounds":       []
    }

    return participant


def plot_participants(participants):

    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True

    figure, ax = plt.subplots(1)
    ax.plot([0], c='white')

    for key in participants:

        p = participants[key]

        origin = (p['xmin'], p['ymin'])

        rectangle = patches.Rectangle(origin, p['width'], p['height'], edgecolor='orange',
        facecolor="blue", linewidth=1)

        ax.add_patch(rectangle)

    plt.ylim(0,120)
    plt.xlim(0,120)

    plt.grid()
    plt.show()

    return 0

## Geometric relationships


def calculate_overlap(A : dict, B : dict) -> float:

    x_A_min             = A['xmin']
    y_A_min             = A['ymin']
    x_A_max             = A['xmin'] + A['width']
    y_A_max             = A['ymin'] + A['height']

    x_B_min             = B['xmin']
    y_B_min             = B['ymin']
    x_B_max             = B['xmin'] + B['width']
    y_B_max             = B['ymin'] + B['height']

    north_edge_overlap      = False
    south_edge_overlap      = False
    west_edge_overlap       = False
    east_edge_overlap       = False
    A_fully_encloses_B      = False
    B_fully_encloses_A      = False
    overlap                 = True

    # Determine overlap direction (multiple can be true)

    if  x_A_min >= x_B_max or x_A_max <= x_B_min:    # No horizontal overlap
            overlap = False

    if  y_A_min >= y_B_max or y_A_max <= y_B_min:      # No vertical overlap
            overlap = False

    if  ( (x_A_min <= x_B_min <= x_A_max) and (x_A_min <= x_B_max <= x_A_max) and 
        (y_A_min <= y_B_min <= y_A_max) and (y_A_min <= y_B_max <= y_A_max) ):
            A_fully_encloses_B = True

    if  ( (x_B_min <= x_A_min <= x_B_max) and (x_B_min <= x_A_max <= x_B_max) and 
        (y_B_min <= y_A_min <= y_B_max) and (y_B_min <= y_A_max <= y_B_max) ):
            B_fully_encloses_A = True

    if  x_A_min > x_B_min and x_A_min < x_B_max:
            west_edge_overlap = True

    if  x_A_max > x_B_min and x_A_max < x_B_max:
            east_edge_overlap = True

    if  y_A_max > y_B_min and y_A_max < y_B_max:
            north_edge_overlap = True

    if  y_A_min > y_B_min and y_A_min < y_B_max:
            south_edge_overlap = True

    # Determine overlap coordinates
    
    if overlap == False:
        print("party!")
    else:
          if A_fully_encloses_B:
                print('A fully encloses B!')
                x_Overlap_min = x_B_min
                x_Overlap_max = x_B_max
                y_Overlap_min = y_B_min
                y_Overlap_max = y_B_max
          elif B_fully_encloses_A:
                print('B fully encloses A!')
                x_Overlap_min = x_A_min
                x_Overlap_max = x_A_max
                y_Overlap_min = y_A_min
                y_Overlap_max = y_A_max
          elif north_edge_overlap and east_edge_overlap and west_edge_overlap:
                print('Overlap at north, east and west edge!')
                x_Overlap_min = x_A_min
                x_Overlap_max = x_A_max
                y_Overlap_min = y_B_min
                y_Overlap_max = y_A_max
          elif north_edge_overlap and east_edge_overlap and south_edge_overlap:
                print('Overlap at north, east and south edge!')
                x_Overlap_min = x_A_min
                x_Overlap_max = x_B_max
                y_Overlap_min = y_A_min
                y_Overlap_max = y_A_max
          elif north_edge_overlap and west_edge_overlap and south_edge_overlap:
                print('Overlap at north, west and south edge!')
                x_Overlap_min = x_B_min
                x_Overlap_max = x_A_max
                y_Overlap_min = y_A_min
                y_Overlap_max = y_B_max
          elif south_edge_overlap and east_edge_overlap and west_edge_overlap:
                print('Overlap at south, east and west edge!')
                x_Overlap_min = x_A_min
                x_Overlap_max = x_A_max
                y_Overlap_min = y_A_min
                y_Overlap_max = y_B_max
          elif north_edge_overlap and east_edge_overlap:
                print('Overlap at nort and east edge!')
                x_Overlap_min = x_B_min
                x_Overlap_max = x_A_max
                y_Overlap_min = y_B_min
                y_Overlap_max = y_A_max
          elif north_edge_overlap and west_edge_overlap:
                print('Overlap at north and west edge!')
                x_Overlap_min = x_A_min
                x_Overlap_max = x_B_max
                y_Overlap_min = y_B_min
                y_Overlap_max = y_A_max
          elif north_edge_overlap and south_edge_overlap:
                print('Overlap at north and south edge!')
                x_Overlap_min = x_B_min
                x_Overlap_max = x_B_max
                y_Overlap_min = y_A_min
                y_Overlap_max = y_A_max
          elif south_edge_overlap and east_edge_overlap:
                print('Overlap at south and east edge!')
                x_Overlap_min = x_B_min
                x_Overlap_max = x_A_max
                y_Overlap_min = y_A_min
                y_Overlap_max = y_B_max
          elif south_edge_overlap and west_edge_overlap:
                print('Overlap at south and west edge!')
                x_Overlap_min = x_A_min
                x_Overlap_max = x_B_max
                y_Overlap_min = y_A_min
                y_Overlap_max = y_B_max
          elif east_edge_overlap and west_edge_overlap:
                print('Overlap at east and west edge')
                x_Overlap_min = x_A_min
                x_Overlap_max = x_A_max
                y_Overlap_min = y_B_min
                y_Overlap_max = y_B_max
          elif north_edge_overlap:
                print('Overlap at north edge!')
                x_Overlap_min = x_B_min
                x_Overlap_max = x_B_max
                y_Overlap_min = y_B_min
                y_Overlap_max = y_A_max
          elif east_edge_overlap:
                print('Overlap at east edge!')
                x_Overlap_min = x_B_min
                x_Overlap_max = x_A_max
                y_Overlap_min = y_B_min
                y_Overlap_max = y_B_max
          elif south_edge_overlap:
                print('Overlap at south edge!')
                x_Overlap_min = x_B_min
                x_Overlap_max = x_B_max
                y_Overlap_min = y_A_min
                y_Overlap_max = y_B_max
          elif west_edge_overlap:
                print('Overlap at west edge!')
                x_Overlap_min = x_A_min
                x_Overlap_max = x_B_max
                y_Overlap_min = y_B_min
                y_Overlap_max = y_B_max       

    if overlap == 0:
          return 0
    else:    
        return (x_Overlap_min, y_Overlap_min), (x_Overlap_max, y_Overlap_max)
    

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
