import logging
import os
import pandas as pd

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
