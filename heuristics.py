
from collections import namedtuple

def estimate_pair_success(A : namedtuple, B: namedtuple , direction : str) -> bool:

    if B.freespace:

        if direction == 'vertical-push-down':

            height_of_freespace_above_B     = ((B.freespace.ymin + B.freespace.height) - (B.ymin + B.height) 
                                            if (B.freespace.ymin + B.freespace.height) > (B.ymin + B.height) 
                                            else 0 )
            
            promising                       = (0.5 * A.height < height_of_freespace_above_B)
            
        elif direction == 'vertical-push-up':

            height_of_freespace_below_B     = ((B.ymin - B.freespace.ymin) 
                                            if (B.ymin > B.freespace.ymin) 
                                            else 0)
            
            promising                       = (0.5 * A.height < height_of_freespace_below_B)
            
        elif direction == 'horizontal-push-left':
        
            width_of_freespace_right_of_B   = ((B.freespace.xmin + B.freespace.width) - (B.xmin + B.width)
                                            if (B.freespace.xmin + B.freespace.width) > (B.xmin + B.width)
                                            else 0)
            
            promising                       = (0.5 * A.width < width_of_freespace_right_of_B)

            
        elif direction == 'horizontal-push-right':
        
            width_of_freespace_left_of_B    = ((B.xmin - B.freespace.xmin)
                                            if (B.xmin > B.freespace.xmin)
                                            else 0)
            
            promising                       = (0.5 * A.width < width_of_freespace_left_of_B)  

    else:

        promising = False


    return promising