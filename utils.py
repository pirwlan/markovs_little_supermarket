import cv2
import datetime
import gif
import io
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns

sns.set(style="whitegrid")
logger = logging.getLogger(__file__.split('/')[-1][:-3])


def read_initial_probabilities():
    """
    reads initial location probabilities

    Returns:
        df_init: pd.DataFrame
    """

    df_init = pd.read_csv(os.getenv('INIT_PROB_PATH'))

    df_init.rename(columns={'Unnamed: 0': 'location',
                            'location': 'initial_probability'},
                   inplace=True)

    return df_init


def read_transition_probabilities():
    """
    reads transition probabilities

    Returns:
        df_trans: pd.DataFrame
    """
    df_trans = pd.read_csv(os.getenv('TRANS_PROB_PATH'),
                           index_col=0)

    return df_trans


def read_customer_per_minute():
    """
    reads customer_per_minute

    Returns:
        df_cust_min: pd.DataFrame
    """
    df_cust_min = pd.read_csv(os.getenv('CUST_PER_MIN_PATH'),
                              index_col=0)

    return df_cust_min


def make_dist_gif(dist_dict):
    """
    makes a gif image of the customer distribution
    throughtout all time points

    Args:
        dist_dict: dict - customer distribution history with location, history_list as k,v

    """
    plt.clf()
    df_dist = pd.DataFrame(dist_dict)

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


def get_img_from_fig(fig):
    """
    Converts fig object to numpy array for incorporation
    into bigger convas

    Args:
        fig: plt.figure object

    Returns:
        img: np.array

    """

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img


def get_current_dist(curr_dist_dict, step):
    """
    Creates figure object of current customer distribution

    Args:
        curr_dist_dict: dict - current distribution of customers
        step: int - time in minutes

    Returns:
        dist_img: np.array - figure as array
    """
    df_dist = pd.Series(curr_dist_dict)

    # plot the bargraph
    plt.clf()

    fig = plt.figure(figsize=(7, 4))
    ax = sns.barplot(x=df_dist.index, y=df_dist.values.astype(int))

    ax.set_xlabel("location")
    ax.set_ylabel("num of current customer")

    ax.legend()
    time_in_seconds = (step * 60) + (7 * 60 * 60)
    ax.set_title(f'Time: {str(datetime.timedelta(seconds=time_in_seconds))}')

    curr_fig = get_img_from_fig(fig)

    return curr_fig


def draw_distribution(frame, curr_dist_dict, step):
    """
    draw distribution on canvas frame

    Args:
        frame: np.array - canvas
        curr_dist_dict: dict - current distribution
        step: int - time in minutes

    Returns:
        frame_copy: np.Array - new canvas to show

    """
    frame_copy = frame.copy()
    curr_dist_fig = get_current_dist(curr_dist_dict, step)

    graph_height = curr_dist_fig.shape[0]
    graph_width = curr_dist_fig.shape[1]
    y_upper = 0
    y_lower = int(graph_height)

    x_upper = int(os.getenv('SUPERMARKET_IMG_WIDTH'))
    x_lower = int(os.getenv('SUPERMARKET_IMG_WIDTH')) + int(graph_width)

    frame_copy[y_upper:y_lower, x_upper:x_lower] = curr_dist_fig

    return frame_copy


def draw_turnover(frame, turnover_history):
    """
    draw distribution on canvas frame

    Args:
        frame: np.array - canvas
        turnover_history: list - history of turnover

    Returns:
        frame_copy: np.Array - new canvas to show

    """
    frame_copy = frame.copy()
    curr_turn_fig = get_current_turnover(turnover_history)

    graph_height = curr_turn_fig.shape[0]
    graph_width = curr_turn_fig.shape[1]

    y_upper = int(graph_height)
    y_lower = int(os.getenv('SUPERMARKET_IMG_HEIGHT'))

    x_upper = int(os.getenv('SUPERMARKET_IMG_WIDTH'))
    x_lower = int(os.getenv('SUPERMARKET_IMG_WIDTH')) + int(graph_width)

    frame_copy[y_upper:y_lower, x_upper:x_lower] = curr_turn_fig

    return frame_copy


def get_current_turnover(turnover_history):
    """

    Returns:

    """
    x_axis = [x for x in range(len(turnover_history))]
    # plot the bargraph
    plt.clf()

    fig = plt.figure(figsize=(7, 3.9))
    ax = sns.lineplot(x_axis, turnover_history)

    ax.set_xlabel("Time [min]")
    ax.set_ylabel("Turnover [s]")

    ax.legend()
    ax.set_title("Total turnover")

    curr_fig = get_img_from_fig(fig)

    return curr_fig
