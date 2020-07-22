import cv2
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
        cust_init = df_dist.iloc[0].sum()
        cust_curr = df_dist.iloc[idx].sum()
        sns.barplot(x=df_dist.columns, y=df_dist.iloc[idx])
        plt.title(f'Initial Cust: {cust_init}, Current Cust: {cust_curr}, Timestep {idx}')
        plt.xlabel('location')
        plt.ylabel('')
        plt.ylim(0, cust_init)

    frames = []
    for timestep in range(len(df_dist)):
        frame = plot_dist(timestep)
        frames.append(frame)

    gif.save(frames, 'distribution.gif', duration=500)


def draw_debugging():
    img = cv2.imread(os.getenv('SUPERMARKET_IMG_PATH'))
    y = 590
    x = 344

    size = 20
    loc_upper_y = int(y - (size / 2))
    loc_lower_y = int(y + size - (size / 2))
    loc_upper_x = int(x - (size / 2))
    loc_lower_x = int(x + size - (size / 2))

    while True:

        frame = img.copy()
        frame[loc_upper_y: loc_lower_y, loc_upper_x: loc_lower_x] = (0, 0, 255)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



