from customer import Customer
from dotenv import load_dotenv
from supermarket import Supermarket

import cv2
import get_transitional_probabilities as tp
import logging
import numpy as np
import os
import utils


def shopping_simulator():
    supermarket_img = cv2.imread(os.getenv('SUPERMARKET_IMG_PATH'))

    tp.calculate_tp()

    supermarche = Supermarket()
    canvas = np.zeros([780, 1637, 3], dtype='uint8')
    for cust_id in range(100):
        supermarche.add_customer(customer=Customer(customer_id=cust_id))

    while supermarche.step < 100:
        # print(f'[MAIN] Start of step {supermarche.step}')
        frame = canvas.copy()
        frame[0:int(os.getenv('SUPERMARKET_IMG_HEIGHT')), 0:int(os.getenv('SUPERMARKET_IMG_WIDTH'))] = supermarket_img

        supermarche.update_step(frame)
        test = supermarche.update_cust_distribution()
        print(test)


        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    utils.make_dist_plot(supermarche.cust_dist)


if __name__ == '__main__':
    load_dotenv('./config.env')

    logging.basicConfig(
        filename='./logs/shopping.log',
        filemode='w',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
            )

    logger = logging.getLogger(__file__.split('/')[-1][:-3])
    logger.info(f'Programm has started...')

    shopping_simulator()
    #utils.draw_debugging()
    logger.info(f'Programm has finished...')
