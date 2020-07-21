import os
import pandas as pd


def read_data():
    """
    reads all .csv files and increments customer_no with every new day
    Returns:
        df: pd.DataFrame - df containing all shopping data
    """
    for idx, day_file in enumerate(os.listdir(os.getenv('DATA_PATH'))):

        if day_file[-3:] == 'csv':
            df_temp = pd.read_csv(os.path.join(os.getenv('DATA_PATH'), day_file),
                                  sep=';',
                                  index_col='timestamp',
                                  parse_dates=['timestamp'])

            df_temp['customer_no'] = df_temp['customer_no'] if idx == 0 \
                else df_temp['customer_no'] + df['customer_no'].max()

            df = df_temp if idx == 0 else pd.concat([df, df_temp])

    return df.sort_values(['customer_no', 'timestamp'])


def add_shift_and_filter(df):
    """
    Shifs location by -1, and filtes last step for each customer out.
    Assumption: checkout is the final entry per customer.
    Change end state of checkout always to checkout.

    Args:
        df: pd.DataFrame - containing all customer information data
    Returns:
        df_filtered: pd.DataFrame - shifted and filtered df

    """
    df['location_shifted'] = df['location'].shift(periods=-1)

    df.loc[df['location'] == 'checkout', 'location_shifted'] = 'checkout'

    # df_filtered = df[df['location'] != 'checkout']

    return df


def transition_dict_to_list(trans_dict):
    """
    transforms transition dictionary to list
    Args:
        trans_dict: dict - dictionary with (transition_start, transtion_stop):count as k:v

    Returns:
        trans: list - list of lists with ([transition_start, transition_stop, count])
    """
    trans = list()
    for (trans_start, trans_stop), trans_count in sorted(trans_dict.items()):
        trans.append([trans_start, trans_stop, trans_count])

    return trans


def sum_transitions(df):
    """
    Loos over all posible combinations and makes summation.
    When transition start and transition stop is the same -> skip
    Args:
        df: pd.DataFrame - dataframe containing shifted and filtered data
    Returns:

    """
    transition_dict = dict()

    for transition_idx in range(len(df)):
        curr_transition = df.iloc[transition_idx]

        transition_start = curr_transition['location']
        transition_stop = curr_transition['location_shifted']

        transition = (transition_start, transition_stop)

        if transition in transition_dict:
            transition_dict[transition] += 1
        else:
            transition_dict[transition] = 1

    trans_list = transition_dict_to_list(transition_dict)

    # read trans list to DataFrame
    df_test = pd.DataFrame(trans_list, columns=['trans_start', 'trans_stop', 'trans_count'])

    # transform to wide foramat
    df_piv = df_test.pivot(index='trans_start', columns='trans_stop', values='trans_count')

    return df_piv


def normalize_tp(df):
    """
    normalized transition matrix by total event count - 1
    Args:
        df: pd.DataFrame - transition matrix

    Returns:
        normalized_tp: pd.DataFrame - transition_probabilities matrix
    """
    # fills "cross values" with 0
    df = df.fillna(0)

    # normalize by n
    df = df.div(df.sum(axis=1), axis=0)

    return df


def calculate_tp():
    """
    Main landing of get_transtional_probabilities.py
    Returns:
        transitional_probabilites_matrix: pd.DataFrame - normalized matrix
    """

    df_data = read_data()
    df_data = add_shift_and_filter(df_data)

    trans_prob_unnormalized = sum_transitions(df_data)
    trans_prob = normalize_tp(trans_prob_unnormalized)

    return trans_prob
