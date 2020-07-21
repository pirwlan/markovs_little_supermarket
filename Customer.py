import numpy as np
import utils

INIT_PROB = utils.read_initial_probabilities()


class Customer:
    """
    Class for customer
    """
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.location = np.random.choice(a=INIT_PROB['location'].values,
                                         p=INIT_PROB['initial_probability'])
