import logging
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


def add_shift_and_checkout(df):
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
    df_trans_long = pd.DataFrame(trans_list, columns=['trans_start', 'trans_stop', 'trans_count'])

    # transform to wide foramat
    df_wide = df_trans_long.pivot(index='trans_start', columns='trans_stop', values='trans_count')

    return df_wide


def normalize_and_save_tp(df):
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
    total_trans_per_row = df.sum(axis=1)

    df = df.div(total_trans_per_row, axis=0)

    df.to_csv(os.getenv('TRANS_PROB_PATH'))


def add_missing_time_stamps(df):
    """
    adds missing time stamps to grasp time spend per state better

    Args:
        df: pd.DataFrame - input data mit missing time values

    Returns:
        df: pd.DataFrame - with missing values

    """
    df = df.sort_values(['customer_no', 'timestamp'])
    for idx, customer in enumerate(df['customer_no'].unique()):
        df_curr_cust = df[df['customer_no'] == customer]

        start_time = df_curr_cust.index[0]
        stop_time = df_curr_cust.index[-1]

        # create index
        date_idx = pd.date_range(start_time,
                                 stop_time,
                                 freq='min')

        # forward fill missing values
        df_curr_cust_filled = pd.DataFrame(df_curr_cust, index=date_idx).ffill()

        # build new DatrFrame
        df_full = df_curr_cust_filled if idx == 0 else pd.concat([df_full, df_curr_cust_filled])

    return df_full


def get_customer_index(df):
    """
    Creates index on the customer level.
    Args:
        df: pd.DataFrame

    Returns:
        df: pd.DataFrae
    """
    df_sorted = df.sort_values(['customer_no', 'timestamp'])

    customer_numbers = df_sorted['customer_no']

    counts = dict()
    cust_count = list()

    for customer in customer_numbers:

        if customer in counts:
            counts[customer] += 1

        else:
            counts[customer] = 1

        cust_count.append(counts[customer])

    df_sorted['customer_index'] = cust_count

    return df_sorted


def get_initial_probability(df):
    """
    Checks location of first occurence of each customer
    for initial probabilies
    Args:
        df: pd.DataFrame

    """
    df_ = df.copy()
    df_['timestamp'] = df_.index
    df_ = get_customer_index(df_)
    df_initial_prob = df_[df_['customer_index'] == 1]['location'].value_counts(normalize=True)
    df_initial_prob.to_csv(os.getenv('INIT_PROB_PATH'))


def get_cust_per_quarter(df):
    """
    Calculates overview of average customer per minuter
    on a 15 minute resolution
    Args:
        df:
    """
    df['timestamp'] = df.index
    df = get_customer_index(df)
    df_first = df[df['customer_index'] == 1]

    df_mon_ = df_first[df_first.index.day == 2]['customer_index'].resample('900s').sum()
    df_tue_ = df_first[df_first.index.day == 3]['customer_index'].resample('900s').sum()
    df_wed_ = df_first[df_first.index.day == 4]['customer_index'].resample('900s').sum()
    df_thu_ = df_first[df_first.index.day == 5]['customer_index'].resample('900s').sum()
    df_fri_ = df_first[df_first.index.day == 6]['customer_index'].resample('900s').sum()

    day_dict = {'monday': df_mon_.values,
                'tuesday': df_tue_.values,
                'wednesday': df_wed_.values,
                'thursday': df_thu_.values,
                'friday': df_fri_.values}

    df_days = pd.DataFrame.from_dict(day_dict)
    df_days['mean'] = df_days.mean(axis=1)
    df_days['std'] = df_days[['monday', 'tuesday', 'wednesday', 'thursday', 'friday']].std(axis=1)

    df_days['mean_normalized'] = df_days['mean'] / 15
    df_days['std_normalized'] = df_days['std'] / 15

    df = df_days[['mean_normalized', 'std_normalized']]
    df.to_csv(os.getenv('CUST_PER_MIN_PATH'))


def calculate_tp():
    """
    Main landing of get_transtional_probabilities.py
    """
    logger = logging.getLogger(__file__.split('/')[-1][:-3])

    if os.path.exists(os.getenv('INIT_PROB_PATH')) and \
            os.path.exists(os.getenv('TRANS_PROB_PATH')) and \
            os.path.exists(os.getenv('CUST_PER_MIN_PATH')):
        logger.info(f'''Initial location probabilities, transition probabilities and 
                        customers per quarter have already been calculated...''')
        return True

    df_data = read_data()
    df_data = add_missing_time_stamps(df_data)

    if not os.path.exists(os.getenv('CUST_PER_MIN_PATH')):
        get_cust_per_quarter(df_data)
        logger.info(f'cust_per_quarer.csv has been calculated and saved...')

    df_data = add_shift_and_checkout(df_data)

    if not os.path.exists(os.getenv('INIT_PROB_PATH')):
        get_initial_probability(df_data)
        logger.info(f'Initial location probabilities has been calculated and saved...')

    if not os.path.exists(os.getenv('TRANS_PROB_PATH')):

        trans_prob_unnormalized = sum_transitions(df_data)
        normalize_and_save_tp(trans_prob_unnormalized)
        logger.info(f'Transition probabilities has been calculated and saved...')




