import cv2
import numpy as np
import os


class Supermarket:
    """
    The supermarket class
    """

    def __init__(self):

        # cust_list are customers currently in the supermarket
        self.cust_list = list()

        # cust_list_all keeps track of all customer ever in the supermarkg
        self.cust_list_all = list()

        # people at checkout
        self.checkout_list = list()

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

        self.location_dict = {
            'drinks': [(120, 210), (220, 420)],
            'dairy': [(360, 420), (220, 420)],
            'spices': [(580, 640), (220, 420)],
            'fruit': [(810, 900), (220, 420)],
            'checkout': [(170, 450), (660, 740)]}

        self.step = 0

    def __repr__(self):
        output_str = f'At time step {self.step}, there are {len(self.cust_list)} in the supermarket. \n Of those are: \n'
        for location, count in self.cust_dist.items():
            output_str += f'{count[-1]} in the {location} section. \n'

        return output_str

    def add_customer(self, customer):
        """
        allows for addition of customer, and initiliases there location
        by initial x,y location

        customer: list - list of Customer instances

        """
        self.cust_list.append(customer)
        self.cust_list_all.append(customer)

        for curr_cust in self.cust_list:
            self.update_cust_location(curr_cust)

    def update_step(self, frame):

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

    def draw(self, curr_cust, frame):

        loc_upper_y = int(curr_cust.y - (curr_cust.size / 2))
        loc_lower_y = int(curr_cust.y + curr_cust.size - (curr_cust.size / 2))
        loc_upper_x = int(curr_cust.x - (curr_cust.size / 2))
        loc_lower_x = int(curr_cust.x + curr_cust.size - (curr_cust.size / 2))

        frame[loc_upper_y: loc_lower_y, loc_upper_x: loc_lower_x] = curr_cust.color

    def update_cust_distribution(self):

        for cust in self.cust_list:
            self.curr_dist_dict[cust.current_location] += 1

        for location, curr_count in self.curr_dist_dict.items():
            self.cust_dist[location].append(curr_count)

        return self.curr_dist_dict()

    def update_checkout(self):
        if len(self.checkout_list) > 0:

            curr_cust = self.checkout_list.pop(0)

            for idx, cust in enumerate(self.cust_list):
                if curr_cust.customer_id == cust.customer_id:
                    self.cust_list.pop(idx)

    def checkout_list_update(self, curr_cust):

        if len(curr_cust.location_history) > 1:
            if curr_cust.location_history[-1] == 'checkout' and curr_cust.location_history[-2] != 'checkout':
                self.checkout_list.append(curr_cust)

    def update_cust_location(self, curr_cust):
        if curr_cust.current_location == 'checkout' \
                            and curr_cust.target_location == 'checkout':
            return True

        if self.step > 0:
            curr_cust.current_location = curr_cust.target_location

        updated_x = np.random.randint(*self.location_dict[curr_cust.current_location][0])
        updated_y = np.random.randint(*self.location_dict[curr_cust.current_location][1])

        curr_cust.update_location(updated_x=updated_x, updated_y=updated_y)

