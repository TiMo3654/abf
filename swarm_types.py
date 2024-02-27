from collections import namedtuple

Rectangle           = namedtuple('Rectangle', 'xmin ymin width height')

Lateral_Conditions  = namedtuple('Lateral_Conditions', [ 'overlap'
                                                       , 'locations'
                                                       , 'clashes'
                                                       , 'aversion'
                                                       , 'trouble'
                                                       , 'tension'
                                                       , 'relaxed_connection'])


Participant         = namedtuple('Participant', [  'idx'                            # str
                                                , 'connections'                    # namedtuple 
                                                , 'xmin'                           # int
                                                , 'ymin'                           # int
                                                , 'width'                          # int
                                                , 'height'                         # int
                                                , 'clashes'                        # namedtuple    # Initialized with all ids and zeros
                                                , 'aversions'                      # namedtuple    # Initialized with all ids and zeros
                                                , 'interference'                   # float     
                                                , 'overlap_with_idx'               # set of ids
                                                , 'turmoil'                        # float
                                                , 'relaxed_connections'            # int
                                                , 'protrusion_status'              # str
                                                , 'protrusion_extend'              # tuple
                                                , 'protruded_zone_edges'           # set of tuples
                                                , 'healthy'                        # boolean
                                                , 'compliant'                      # boolean
                                                , 'yield_polygon'                  # Rectangle
                                                , 'freespace'                      # Rectangle
                                                , 'secondary_freespace_north_east' # Rectangle
                                                , 'secondary_freespace_south_east' # Recatngle
                                                , 'secondary-freespace-south-west' # Rectangle
                                                , 'secondary-freespace-north-west' # Rectangle
                                                , 'last_move'                      # str
                                                , 'color'])                        # str


                                                    



