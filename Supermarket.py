class Supermarket:
    """
    The supermarket class
    """

    def __init__(self, customers):

        self.cust_list = customers
        self.cust_dist = {
            'checkout': list(),
            'dairy': list(),
            'fruit': list(),
            'drinks': list(),
            'spices': list()
        }

        self.cust_size = 20

        self.location_dict = {
            'checkout': (120, 660),
            'dairy': (180, 350),
            'fruit': (180, 810),
            'drinks': (180, 120),
            'spices': (180, 580)
        }

        self.step = 0

    def __repr__(self):
        output_str = f'At time step {self.step}, there are {len(self.cust_list)} in the supermarket. \n Of those are: \n'
        for location, count in self.cust_dist.items():
            output_str += f'{count[-1]} in the {location} section. \n'

        return output_str

    def update(self, frame):

        self.step += 1
        self.update_cust_locations()
        self.draw(frame)
        self.update_cust_distribution()


    def draw(self, frame):

        for curr_cust in self.cust_list:
            curr_cust_locations = self.location_dict[curr_cust.current_location]
            curr_cust.update_location(curr_cust_locations)

            frame[curr_cust.y:(curr_cust.y + self.cust_size),
                  curr_cust.x:(curr_cust.x + self.cust_size)] = curr_cust.color

    def update_cust_locations(self):
        for cust in self.cust_list:
            cust.update_location(self.location_dict[cust.current_location])
            cust.transition()

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
