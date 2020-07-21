import gif
import logging
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
sns.set(style="whitegrid")
logger = logging.getLogger(__file__.split('/')[-1][:-3])


def read_initial_probabilities():
    """
    reads initial location probabilities
    Returns:
        df_init: pd.DataFrame -
    """

    df_init = pd.read_csv(os.getenv('INIT_PROB_PATH'))

    df_init.rename(columns={'Unnamed: 0': 'location',
                            'location': 'initial_probability'},
                   inplace=True)

    return df_init


def read_transition_probabilities():
    df_trans = pd.read_csv(os.getenv('TRANS_PROB_PATH'),
                           index_col=0)

    return df_trans


def make_dist_plot(dist_dict):
    """
    makes a gif image throught out all time points
    Args:
        dist_dict: dict - customer distribution history

    """
    df_dist = pd.DataFrame(dist_dict)
    cust_number = df_dist.iloc[0].sum()

    @gif.frame
    def plot_dist(idx):

        sns.barplot(x=df_dist.columns, y=df_dist.iloc[idx])
        plt.title(f'Timestep {idx}')
        plt.xlabel('location')
        plt.ylabel('')
        plt.ylim(0, cust_number)

    frames = []
    for timestep in range(len(df_dist)):
        frame = plot_dist(timestep)
        frames.append(frame)

    gif.save(frames, 'distribution.gif', duration=500)



