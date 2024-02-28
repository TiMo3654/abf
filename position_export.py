import pandas as pd
from matplotlib import colors

# Plot in tikz: https://gist.github.com/AugustUnderground/fc914edbc007c37ad3008d50701a7a7e

# TODO: Update exort function

def positions2csv(participants : dict, layout_zone : dict, file_name : str):


    df              = pd.DataFrame.from_dict(participants, orient = 'index')

    df['color_hex'] = [colors.to_hex(x)[1:] for x in list(df['color'].values)]

    df_reduced      = df[['idx', 'xmin', 'ymin', 'width', 'height', 'color_hex']]

    df_zone         = pd.DataFrame.from_dict(layout_zone | {'idx' : "~", 'color_hex' : 'ffffff'}, orient = 'index').transpose()

    df_final        = pd.concat([df_zone, df_reduced])

    df_final.to_csv(file_name, index = False)

    return 