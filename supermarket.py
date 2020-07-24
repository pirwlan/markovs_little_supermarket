from customer import Customer

import math
import numpy as np
import utils

CUST_PER_MIN = utils.read_customer_per_minute()


class Supermarket:
    """
    The supermarket class

    Args:
        num_checkout: int - number of checkout people

    """

    def __init__(self, num_checkout):

        self.num_checkout = num_checkout

        # cust_list are customers currently in the supermarket
        self.cust_list = list()

        # cust_list_all keeps track of all customer ever in the supermarkg
        self.cust_list_all = list()

        # people at checkout
        self.checkout_list = list()

        # distribution dicts
        self.cust_dist = {
            'checkout': list(),
            'dairy': list(),
            'fruit': list(),
            'drinks': list(),
            'spices': list()
        }

        self.curr_dist_dict = {
            'checkout': 0,
            'dairy': 0,
            'fruit': 0,
            'drinks': 0,
            'spices': 0
        }

        # spawn coordinates of different locations
        self.location_dict = {
            'drinks': [(120, 210), (220, 420)],
            'dairy': [(360, 420), (220, 420)],
            'spices': [(580, 640), (220, 420)],
            'fruit': [(810, 900), (220, 420)],
            'checkout': [(170, 450), (660, 740)]}

        self.location_turnover = {
            'drinks': 6,
            'dairy': 5,
            'spices': 3,
            'fruit': 4,
            'checkout': 0}

        self.turnover = 0
        self.turnover_history = [0]

        self.step = 0

    def __repr__(self):
        output_str = f'At time step {self.step}, there are {len(self.cust_list)} in the supermarket. \n Of those are: \n'
        for location, count in self.cust_dist.items():
            output_str += f'{count[-1]} in the {location} section. \n'

        return output_str

    def add_customer(self, num_of_customer):
        """
        allows for addition of customer, and initiliases there location
        by initial x,y location

        number_of_customer: int - number of Customers to create

        """

        for num_cust in range(num_of_customer):
            curr_cust_id = len(self.cust_list_all)
            curr_cust = Customer(customer_id=curr_cust_id)

            self.update_cust_location(curr_cust)
            self.cust_list.append(curr_cust)
            self.cust_list_all.append(curr_cust)

    def update_step(self, frame):
        """
        updates supermarket
        Args:
            frame: np.Array - canvas
        """


        self.step += 1

        for cust in self.cust_list:

            # do transition for customer
            cust.transition()
            self.update_cust_location(curr_cust=cust)

            # draw customers on image
            self.draw(cust, frame)

            self.checkout_list_update(curr_cust=cust)

        # see who is new in chekout and pop one
        self.update_checkout()

        # update distribution
        self.update_cust_distribution()

        # calculate turnover
        self.calc_turnover()

        # spawn new customer
        self.spawn_customer()

    def draw(self, curr_cust, frame):
        """
        Draws each customer on the canvas
        Args:
            curr_cust: Customer - single customer instance
            frame: np.array - canvas to draw on
        """

        loc_upper_y = int(curr_cust.y - (curr_cust.size / 2))
        loc_lower_y = int(curr_cust.y + curr_cust.size - (curr_cust.size / 2))
        loc_upper_x = int(curr_cust.x - (curr_cust.size / 2))
        loc_lower_x = int(curr_cust.x + curr_cust.size - (curr_cust.size / 2))

        frame[loc_upper_y: loc_lower_y, loc_upper_x: loc_lower_x] = curr_cust.color

    def update_cust_distribution(self):
        """
        Counts current customer in each location, and appends count
        to history per location
        """

        self.curr_dist_dict = {
            'checkout': 0,
            'dairy': 0,
            'fruit': 0,
            'drinks': 0,
            'spices': 0
        }

        for cust in self.cust_list:
            self.curr_dist_dict[cust.current_location] += 1

        for location, curr_count in self.curr_dist_dict.items():
            self.cust_dist[location].append(curr_count)

    def update_checkout(self):
        """
        Deletes one customer who is in location checkout
        and deletes him from customer list.
        """

        for person in range(self.num_checkout):
            if len(self.checkout_list) > 0:

                curr_cust = self.checkout_list.pop(0)

                for idx, cust in enumerate(self.cust_list):
                    if curr_cust.customer_id == cust.customer_id:
                        self.cust_list.pop(idx)

    def checkout_list_update(self, curr_cust):
        """
        adds new customer to checkout_list
        Args:
            curr_cust: Customer - customer instance
        """

        if len(curr_cust.location_history) > 1:
            if curr_cust.location_history[-1] == 'checkout' and curr_cust.location_history[-2] != 'checkout':
                self.checkout_list.append(curr_cust)

    def update_cust_location(self, curr_cust):
        """
        Update location of customer dependent on new location.
        If checkout state has not changed for two turns, do not
        change location

        Args:
            curr_cust: Customer - Customer instance
        """

        if curr_cust.current_location == 'checkout' \
                            and curr_cust.target_location == 'checkout':
            return True

        if curr_cust.target_location:
            curr_cust.current_location = curr_cust.target_location

        updated_x = np.random.randint(*self.location_dict[curr_cust.current_location][0])
        updated_y = np.random.randint(*self.location_dict[curr_cust.current_location][1])

        curr_cust.update_location(updated_x=updated_x, updated_y=updated_y)

    def calc_turnover(self):
        """
        Calculates cumulative sum of turnover each round
        based on how much people are in each location.
        """

        for location, cust_no in self.curr_dist_dict.items():
            self.turnover += self.location_turnover[location] * cust_no

        self.turnover_history.append(self.turnover)

    def spawn_customer(self):
        """
        Checks how many steps (minutes) have passed, and
        calculates number of customers to spawn based on
        distribution of data
        """
        current_quarter = math.floor(self.step / 15)
        cust_per_min = int(np.random.normal(CUST_PER_MIN['mean_normalized'].iloc[current_quarter],
                                            CUST_PER_MIN['mean_normalized'].iloc[current_quarter]))

        if cust_per_min > 0:
            self.add_customer(num_of_customer=cust_per_min)
