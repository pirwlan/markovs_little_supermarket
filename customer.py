from dotenv import load_dotenv

import numpy as np
import utils

load_dotenv('./config.env')

INIT_PROB = utils.read_initial_probabilities()
TRANS_PROB = utils.read_transition_probabilities()


class Customer:
    """
    Class for customer

    Args:
        customer_id: int - unique identifier per customer

    """
    def __init__(self, customer_id):

        # unique identifier
        self.customer_id = customer_id
        self.size = 20

        # start coordinates out of the super market in super market
        self.x = -500
        self.y = -300

        # start localisation based in initial probabilities
        self.location_current = np.random.choice(
                                        a=INIT_PROB['location'].values,
                                        p=INIT_PROB['initial_probability'])

        self.location_history = list()
        self.location_target = str()

        # random color per customer, to allow identification
        self.color = (np.random.randint(0, 255),
                      np.random.randint(0, 255),
                      np.random.randint(0, 255))

    def __repr__(self):

        return f'Customer no: {self.customer_id}'

    def transition(self):
        """
        appends location to location history appends location to history
        updates target location accoring to markov chain prediction
        """

        self.location_history.append(self.location_current)

        if len(self.location_target) > 0:
            self.location_current = self.location_target

        # gets index of current location
        target_index = TRANS_PROB.index.get_loc(self.location_current)

        # create curr state vector with index = 1
        curr_state = np.zeros([1, 5])
        curr_state[:, target_index] = 1

        prob_matrix = TRANS_PROB.values

        # markov chain dotproduct and selection of new location
        curr_trans_prob = curr_state.dot(prob_matrix)[0]

        self.location_target = np.random.choice(a=TRANS_PROB.columns.values,
                                                p=curr_trans_prob)

    def update_location(self, updated_x, updated_y):
        """
        allows for update of localitsation to keep track of customer
        Args:
            updated_x: int - new x localisation
            updated_y: int - new y localisation
        """
        self.x = updated_x
        self.y = updated_y




