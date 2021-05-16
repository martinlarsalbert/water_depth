import pandas as pd
import numpy as np
import os
import src.data.request_water_depth as request_water_depth
import data


def get()->pd.Series:

    """Get all water depth data

    Returns:
        pd.Series: time series of water depth
    """    

    ## First load latest:
    data_depth=pd.Series(dtype=float)
    s_depth = request_water_depth.get()
    data_depth = data_depth.append(s_depth)

    ## then load the stored:
    data_dir = os.path.join(data.path,'raw')
    for file_name in os.listdir(data_dir):

        if not os.path.splitext(file_name)[-1] in ['.json','.csv']:
            continue

        file_path = os.path.join(data_dir, file_name)
        s_depth = pd.read_csv(file_path, index_col=0)['value']
        s_depth.index = pd.to_datetime(s_depth.index)

        data_depth = data_depth.append(s_depth)

    data_depth = data_depth[~data_depth.index.duplicated()]
    data_depth.sort_index(inplace=True)

    return data_depth