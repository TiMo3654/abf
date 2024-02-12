import pandas as pd


def positions2csv(participants : dict, layout_zone : dict):

    df          = pd.DataFrame.from_dict(participants, orient = 'index')

    df_reduced  = df[['idx', 'xmin', 'ymin', 'width', 'height', 'color']]

    df_zone     = pd.DataFrame.from_dict(layout_zone, orient = 'index').transpose()

    df_final    = pd.concat([df_zone, df_reduced])

    df_final.to_csv('module_positions.csv', index = False)

    return 