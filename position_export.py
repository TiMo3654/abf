import pandas as pd
from matplotlib import colors


def positions2csv(participants : dict, layout_zone : dict):

    df              = pd.DataFrame.from_dict(participants, orient = 'index')

    df['color_hex'] = [colors.to_hex(x) for x in list(df['color'].values)]

    df_reduced      = df[['idx', 'xmin', 'ymin', 'width', 'height', 'color_hex']]

    df_zone         = pd.DataFrame.from_dict(layout_zone, orient = 'index').transpose()

    df_final        = pd.concat([df_zone, df_reduced])

    df_final.to_csv('module_positions.csv', index = False)

    return 