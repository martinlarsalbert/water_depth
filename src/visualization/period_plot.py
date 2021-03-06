import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('dark_background')
import docs
import os.path

import src.data.water_depth as water_depth

def plot():

    data_depth = water_depth.get()
    
    periods = data_depth[::12]
    df_depth = pd.DataFrame(index=data_depth.index)
    df_depth['depth'] = data_depth 
    df_depth.loc[periods.index,'period'] = np.arange(len(periods))
    df_depth.fillna(method='ffill', inplace=True)

    groups = df_depth.groupby(by=['period'])

    ## Plotting:
    
    fig,ax=plt.subplots()
    fig.set_size_inches(18,15)

    for period,group in groups:
        group.index-=group.index[0]

        group.plot(y='depth', ax=ax, label=f'period:{int(period)}')

    group.iloc[[-1]].plot(y='depth', style='ro', label='Now', ax=ax)

    ax.grid()

    ## Save?
    save_path = os.path.join(docs.path,'periods.png')
    fig.savefig(save_path)
