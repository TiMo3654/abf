import random
import math
from matplotlib import pyplot as plt, patches
import matplotlib.colors as mcolors
from IPython import display
import pylab as pl
import time

from collections import namedtuple

from util import *

## Test functions

def generate_unconnected_participants(amount : int, layout_zone : dict, maxX : int, maxY : int, seed : int) -> dict:

    random.seed(seed)

    colors = list(mcolors.CSS4_COLORS.keys())

    participants    = []
        
    for i in range(amount):
            
        xmin        = random.randint(0,layout_zone.width)
        ymin        = random.randint(0,layout_zone.height)

        width       = random.randint(5,maxX)
        height      = random.randint(5,maxY)


        participant = {
            "idx"                           : 'p' + str(i),  
            "connections"                   : (),         #('idx' : 2)
            "xmin"                          : xmin,
            "ymin"                          : ymin,
            "width"                         : width,
            "height"                        : height,
            "clashes"                       : (),         #('idx' : 100)
            "aversions"                     : (),         #('idx' : 17,5)
            "interference"                  : 0,
            "overlap_with_idx"              : (),
            "turmoil"                       : 0,
            "relaxed_connections"           : 0,
            "protrusion_status"             : '',
            "protrusion_extend"             : 0,
            "protruded_zone_edges"          : (),
            "healthy"                       : True,
            "compliant"                     : True,
            "yield_polygon"                 : (),
            "freespace"                     : (),
            'secondary_freespace_north_east': (),
            'secondary_freespace_south_east': (),
            'secondary_freespace_south_west': (),
            'secondary_freespace_north_west': (),
            "last_move"                     : '',
            "color"                         : random.choice(colors)
        }

        participants.append(participant)

    # Create defaults for clashes and aversion

    idx_list            = [p['idx'] for p in participants]
    idx_str             = ' '.join(idx_list)

    Clashes             = namedtuple('Clashes', idx_str)

    Aversions           = namedtuple('Aversions', idx_str)

    clashes_default     = Clashes(*(len(participants) * [0]))

    aversions_default   = Aversions(*(len(participants) * [0]))

    # Turn list of dictionaries to list of namedtuples

    participants        = [namedtuple('Participant', participant)(**participant) for participant in participants] 

    # Put in defaults for clashes and aversions

    particpants_updated = [p._replace(clashes = clashes_default, aversions = aversions_default) for p in participants]

    # Put participants into named tuple

    Participants        = namedtuple('Participants', idx_str)

    all_participants    = Participants(*particpants_updated)

    return all_participants



def generate_connected_participants(amount : int, max_num_nets : int, max_num_connections : int, layout_zone : dict, maxX : int, maxY : int, seed : int) -> dict:

    participants    = generate_unconnected_participants(amount, layout_zone, maxX, maxY, seed)

    # Create connections

    for i in range(max_num_nets):   # for every net

        number_of_connected_participants    = random.choice(list(range(2, max_num_connections)))

        #print(number_of_connected_participants)

        connected_participants              = random.choices(list(range(amount)), k=number_of_connected_participants)

        #print(connected_participants)

        for idx in connected_participants:  # for every participant in that net

            #print(idx)

            for idc in connected_participants:  # write the id of all others into the connection dict

                #print(idc)
                
                if idx != idc:
                    participants[str(idx)]['connections'].update({str(idc) : 1})


    return participants


def generate_unconnected_zone_filling_participants(rows : int, cols : int, layout_zone : dict, seed : int) -> dict:

    random.seed(seed)

    colors                  = list(mcolors.CSS4_COLORS.keys())

    participants            = {}

    total_area              = layout_zone["height"] * layout_zone["width"]

    max_participant_height  = layout_zone["height"]/rows

    idx = 0
        
    for i in range(rows):

        xstart  = 0
        xend    = layout_zone["width"]

        for j in range(cols):

            
            xmin        = random.randint(0,layout_zone['width'])
            ymin        = random.randint(0,layout_zone['height'])

            width       = random.randint(xstart,xend) if j != cols-1 else (xend - xstart)

            xstart      = xstart + width

            participant = {
                "idx"                           : str(idx),  
                "connections"                   : {},         #{'idx' : 2}
                "xmin"                          : xmin,
                "ymin"                          : ymin,
                "width"                         : width,
                "height"                        : max_participant_height,
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

            participants[str(idx)]    = participant   

            idx += 1

    return participants




def generate_unconnected_equal_quadratic_participants(amount : int, layout_zone : dict, edge_length : int, seed : int) -> dict:

    random.seed(seed)

    colors = list(mcolors.CSS4_COLORS.keys())

    participants    = {}
        
    for i in range(amount):
            
        xmin        = random.randint(0,layout_zone['width'])
        ymin        = random.randint(0,layout_zone['height'])

        width       = edge_length
        height      = edge_length


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


def generate_unconnected_wheel_participants(layout_zone : dict, edge_length : int, seed : int) -> dict:

    random.seed(seed)

    colors = list(mcolors.CSS4_COLORS.keys())

    participants    = {}
        
    for i in range(5):
            
        xmin        = random.randint(0,layout_zone['width'])
        ymin        = random.randint(0,layout_zone['height'])

        width       = 1.5 * edge_length if (i == 0) else 2 * edge_length
        height      = 1.5 * edge_length if (i == 0) else 0.5 * edge_length


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


def random_place_mcnc(participants_list : list, layout_zone : dict, seed : int) -> dict:

    participants_list_pure      = participants_list[:-1]

    random.seed(seed)

    participants_dict           = {}

    colors                      = list(mcolors.CSS4_COLORS.keys())

    swarm_specifics             = { "clashes"                       : (),         #('idx' : 100)
                                    "aversions"                     : (),         #('idx' : 17,5)
                                    "interference"                  : 0,
                                    "overlap_with_idx"              : (),
                                    "turmoil"                       : 0,
                                    "relaxed_connections"           : 0,
                                    "protrusion_status"             : '',
                                    "protrusion_extend"             : 0,
                                    "protruded_zone_edges"          : (),
                                    "healthy"                       : True,
                                    "compliant"                     : True,
                                    "yield_polygon"                 : (),
                                    "freespace"                     : (),
                                    'secondary_freespace_north_east': (),
                                    'secondary_freespace_south_east': (),
                                    'secondary_freespace_south_west': (),
                                    'secondary_freespace_north_west': (),
                                    "last_move"                     : ''}
    
    # Create defaults for clashes and aversion

    idx_list            = [p['idx'] for p in participants_list_pure]
    idx_str             = ' '.join(idx_list)

    Clashes             = namedtuple('Clashes', idx_str)

    Aversions           = namedtuple('Aversions', idx_str)

    clashes_default     = Clashes(*(len(participants_list_pure) * [0]))

    aversions_default   = Aversions(*(len(participants_list_pure) * [0]))

    swarm_specifics['clashes']      = clashes_default
    swarm_specifics['aversions']    = aversions_default

    # Merge yal input with swarm specifics

    participants_updated_swarm      = [p | swarm_specifics for p in participants_list_pure]

    #print(participants_updated_swarm)

    # Turn connections into namedtuple

    # connections                     = {p.idx : namedtuple('Connections', p['connections'])(**p['connections']) for p in participants_updated_swarm}

    # print(connections)

    participants_updated_con        = [p | {'connections' : namedtuple('Connections', p['connections'])(**p['connections'])} for p in participants_updated_swarm]
    
    participants_updated_color      = [p | {"color" : random.choice(colors)} for p in participants_updated_con]

    #print(participants_updated_con)

    participants_list_tuple          = [namedtuple('Participant', p)(**p) for p in participants_updated_color]

    #print(participants_list_dict)

    Participants                    = namedtuple('Participants', idx_str)

    participants_final              = Participants(*participants_list_tuple)

    #print(participants_final)


    # # # Create complete dictionary

    # # participants_dict               = {p['idx'] : p for p in participants_updated_con}

    # # print(participants_dict)

    # participants_list_dict          = [namedtuple('Participants', p)(**p) for p in participants_dict]

    # # Create named tuple

    # participants_final              = namedtuple('Participants', participants_list_dict)(**participants_list_dict)



    # for participant in participants_list[:-1]:  # The last entry is the network

    #     participant_new             = copy.deepcopy(participant)
        
    #     xmin                        = random.randint(0,layout_zone['width'])
    #     ymin                        = random.randint(0,layout_zone['height'])

    #     participant_new['xmin']     = xmin
    #     participant_new['ymin']     = ymin
    #     participant_new['color']    = random.choice(colors)

    #     participant_new             = participant_new | swarm_specifics

    #     participants_dict.update({participant_new['idx'] : participant_new})

    
    return participants_final       



def plot_participants(layout_zone : namedtuple, participants : namedtuple, xmax : int, ymax : int, sleep_time = 0.0, plot_connections = False):

    plt.rcParams["figure.figsize"] = [7.00, 7.00]
    plt.rcParams["figure.autolayout"] = True

    #colors = ['blue', 'orange', 'black']

    figure, ax = plt.subplots(1)
    ax.plot([0], c='white')

    # Plot layout zone

    origin = (layout_zone.xmin, layout_zone.ymin)

    rectangle = patches.Rectangle(origin, layout_zone.width, layout_zone.height, edgecolor='red',
    facecolor='red', linewidth=2, fill = False)

    ax.add_patch(rectangle)

    # Plot participants

    for p in participants:

        origin = (p.xmin, p.ymin)

        rectangle   = patches.Rectangle(origin, p.width, p.height, edgecolor=p.color,
                        facecolor=p.color, linewidth=0.5, fill = True, alpha = 0.9, hatch = 'x')

        center_x    = p.xmin + 0.5 * p.width
        center_y    = p.ymin + 0.5 * p.height

        plt.text(center_x, center_y, p.idx)

        ax.add_patch(rectangle)

        #if plot_connections:

            # for key in p['connections']: #TODO: Rethink connection plot

            #     center_x_other_one  = participants[key]['xmin'] + 0.5 * participants[key]['width']
            #     center_y_other_one  = participants[key]['ymin'] + 0.5 * participants[key]['height']

            #     dx                  = -(center_x - center_x_other_one) 
            #     dy                  = -(center_y - center_y_other_one)

            #     plt.arrow(center_x, center_y, dx, dy)


    plt.ylim(-10,ymax)
    plt.xlim(-10,xmax)

    plt.grid()
    #plt.show()

    display.clear_output(wait=True)
    display.display(pl.gcf())
    time.sleep(sleep_time)

    plt.close()

    return 0