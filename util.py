import random
import math
from matplotlib import pyplot as plt, patches
import matplotlib.colors as mcolors
from IPython import display
import pylab as pl
import time

## Test functions

def generate_unconnected_participants(amount : int, layout_zone : dict, maxX : int, maxY : int, seed : int) -> dict:

    random.seed(seed)

    colors = list(mcolors.CSS4_COLORS.keys())

    participants    = {}
        
    for i in range(amount):
            
        xmin        = random.randint(0,layout_zone['width'])
        ymin        = random.randint(0,layout_zone['height'])

        width       = random.randint(5,maxX)
        height      = random.randint(5,maxY)


        participant = {
            "idx"                           : str(i),  
            "connections"                   : {},         #{'idx' : 2}
            "xmin"                          : xmin,
            "ymin"                          : ymin,
            "width"                         : width,
            "height"                        : height,
            "clashes"                       : {},         #{'idx' : 100}
            "aversions"                     : {},         #{'idx' : 17,5}
            "interference"                  : 0,
            "overlap-with-idx"              : [],
            "turmoil"                       : 0,
            "relaxed-connections"           : 0,
            "protrusion-status"             : '',
            "protrusion-extend"             : 0,
            "protruded-zone-edges"          : [],
            "healthy"                       : True,
            "compliant"                     : True,
            "yield-polygon"                 : {},
            "freespace"                     : {},
            'secondary-freespace-north-east': {},
            'secondary-freespace-south-east': {},
            'secondary-freespace-south-west': {},
            'secondary-freespace-north-west': {},
            "last-move"                     : '',
            "color"                         : random.choice(colors)
        }

        participants[str(i)]    = participant

    return participants


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
        "overlap-with-idx"              : [],
        "turmoil"                       : 0,
        "relaxed-connections"           : 0,
        "protrusion-status"             : 'safe',
        "protrusion-extend"             : 0,
        "protruded-edges"               :[],
        "healthy"                       : True,
        "compliant"                     : True,
        "yield-polygon"                 : {},
        "freespace"                     : {},
        'secondary-freespace-north-east': {},
        'secondary-freespace-south-east': {},
        'secondary-freespace-south-west': {},
        'secondary-freespace-north-west': {},
        "last-move"                     : 'center',
        "color"                         : 'black'
    }

    return participant


def plot_participants(layout_zone : dict, participants : dict, xmax : int, ymax : int):

    plt.rcParams["figure.figsize"] = [7.00, 7.00]
    plt.rcParams["figure.autolayout"] = True

    #colors = ['blue', 'orange', 'black']

    figure, ax = plt.subplots(1)
    ax.plot([0], c='white')

    # Plot layout zone

    origin = (layout_zone['xmin'], layout_zone['ymin'])

    rectangle = patches.Rectangle(origin, layout_zone['width'], layout_zone['height'], edgecolor='red',
    facecolor='red', linewidth=2, fill = False)

    ax.add_patch(rectangle)

    # Plot participants
    i = 0

    for key in participants:

        p = participants[key]

        origin = (p['xmin'], p['ymin'])

        rectangle   = patches.Rectangle(origin, p['width'], p['height'], edgecolor=p['color'],
                        facecolor=p['color'], linewidth=2, fill = True, alpha = 0.9)

        center_x    = p['xmin'] + 0.5 * p['width']
        center_y    = p['ymin'] + 0.5 * p['height']

        plt.text(center_x, center_y, p['idx'])

        i += 1

        ax.add_patch(rectangle)

    plt.ylim(-10,ymax)
    plt.xlim(-10,xmax)

    plt.grid()
    #plt.show()

    display.clear_output(wait=True)
    display.display(pl.gcf())
    time.sleep(1.0)

    plt.close()

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






        










