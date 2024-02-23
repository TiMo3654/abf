from collections import namedtuple

Rectangle   = namedtuple('Rectangle', 'xmin ymin width height')

Relation    = namedtuple('Relation', 'idx value')

Participant = namedtuple('Participant', [  'idx'                             # str
                                         , 'connections'                    # set 
                                         , 'xmin'                           # int
                                         , 'ymin'                           # int
                                         , 'width'                          # int
                                         , 'height'                         # int
                                         , 'clashes'                        # set of Relations
                                         , 'aversions'                      # set of Relations
                                         , 'interference'                   # float     
                                         , 'overlap_with_idx'               # set
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


                                                    



