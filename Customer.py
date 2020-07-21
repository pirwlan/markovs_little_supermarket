from dotenv import load_dotenv

import numpy as np
import utils

load_dotenv('./config.env')

INIT_PROB = utils.read_initial_probabilities()
TRANS_PROB = utils.read_transition_probabilities()




class Customer:
    """
    Class for customer
    """
    def __init__(self, customer_id):
        self.customer_id = customer_id

        self.current_location = np.random.choice(
                                        a=INIT_PROB['location'].values,
                                        p=INIT_PROB['initial_probability'])

        self.location_history = list()

        self.color = (np.random.randint(0, 255),
                      np.random.randint(0, 255),
                      np.random.randint(0, 255))

        # coordinates for supermarket
        self.x = -500
        self.y = -300

        self.width = 20
        self.height = 20

        self.location_dict = {
            'checkout': (660, 120),
            'dairy': (180, 350),
            'fruit': (180, 810),
            'drinks': (180, 120),
            'spices': (180, 580)
        }

    def __repr__(self):
        return f'''Customer {self.customer_id} is in section {self.current_location} 
                    and has visited {self.location_history} before.'''

    def transition(self):
        self.location_history.append(self.current_location)

        target_index = TRANS_PROB.index.get_loc(self.current_location)

        curr_state = np.zeros([1, 5])
        curr_state[:, target_index] = 1

        prob_matrix = TRANS_PROB.values
        curr_trans_prob = curr_state.dot(prob_matrix)[0]

        self.current_location = np.random.choice(a=TRANS_PROB.columns.values,
                                                 p=curr_trans_prob)

    def draw(self, frame):

        locations = self.location_dict[self.current_location]

        self.x = locations[1]
        self.y = locations[0]

        frame[self.y:(self.y + self.width), self.x:(self.x + self.height)] = self.color



