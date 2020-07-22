from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

import cv2
import numpy as np
import os


class Supermarket:
    """
    The supermarket class
    """

    def __init__(self):

        self.cust_list = list()
        self.cust_dist = {
            'checkout': list(),
            'dairy': list(),
            'fruit': list(),
            'drinks': list(),
            'spices': list()
        }

        self.checkout_list = list()

        self.location_dict = {
            'drinks': [(120, 210), (220, 420)],
            'dairy': [(360, 420), (220, 420)],
            'spices': [(580, 640), (220, 420)],
            'fruit': [(810, 900), (220, 420)],
            'checkout': [(660, 740), (170, 450)]}

        self.step = 0

        self.mask = cv2.imread(os.getenv('SUPERMARKET_MASK_PATH'))
        self.img_mask_binary = np.where(self.mask.mean(axis=2) == 0, 0, 1)
        self.grid = Grid(matrix=self.img_mask_binary)

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

        for cust in self.cust_list:
            updated_x = np.random.randint(*self.location_dict[cust.current_location][0])
            updated_y = np.random.randint(*self.location_dict[cust.current_location][1])
            cust.update_location(updated_x=updated_x, updated_y=updated_y)

    def update_step(self, frame):

        self.step += 1

        for cust in self.cust_list:
            # check whether there are steps do step length
            if len(cust.next_steps) <= 1:
                cust.transition()
                self.calc_next_steps(cust)

            elif len(cust.next_steps) > 1:
                cust.walk()

            # draw customers on image
            self.draw(cust, frame)

             #self.checkout_list_update(curr_cust=cust)

        # see who is new in chekout and pop one
        #self.update_checkout()

        # update distribution
        #self.update_cust_distribution()


        ####self.update_cust_locations()

    def draw(self, curr_cust, frame):

        loc_upper_y = int(curr_cust.y - (curr_cust.size / 2))
        loc_lower_y = int(curr_cust.y + curr_cust.size - (curr_cust.size / 2))
        loc_upper_x = int(curr_cust.x - (curr_cust.size / 2))
        loc_lower_x = int(curr_cust.x + curr_cust.size - (curr_cust.size / 2))

        frame[loc_upper_y: loc_lower_y, loc_upper_x: loc_lower_x] = curr_cust.color

    def update_cust_distribution(self):

        curr_dist_dict = {
            'checkout': 0,
            'dairy': 0,
            'fruit': 0,
            'drinks': 0,
            'spices': 0
        }

        for cust in self.cust_list:
            curr_dist_dict[cust.current_location] += 1

        for location, curr_count in curr_dist_dict.items():
            self.cust_dist[location].append(curr_count)

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

    def calc_next_steps(self, curr_cust):
        self.grid.cleanup()
        start = self.grid.node(curr_cust.x, curr_cust.y)

        target_x = np.random.randint(*self.location_dict[curr_cust.target_location][0])
        target_y = np.random.randint(*self.location_dict[curr_cust.target_location][1])
        print(f'[CALC NEXT STEPS] Next target coordinates: x: {target_x}, y: {target_y}')
        end = self.grid.node(target_x, target_y)

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, end, self.grid)

        curr_cust.update_next_steps(path)





