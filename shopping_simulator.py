from Customer import Customer
from dotenv import load_dotenv
from Supermarket import Supermarket

import cv2
import get_transitional_probabilities as tp
import logging
import os
import utils


def shopping_simulator():
    img = cv2.imread(os.getenv('SUPERMARKET_IMG_PATH'))

    tp.calculate_tp()
    c_01 = Customer(1)
    c_02 = Customer(2)
    c_03 = Customer(3)
    c_04 = Customer(4)
    c_05 = Customer(5)
    c_06 = Customer(6)
    c_07 = Customer(7)
    c_08 = Customer(8)
    c_09 = Customer(9)
    c_10 = Customer(10)

    customers = [c_01, c_02, c_03,
                 c_04, c_05, c_06,
                 c_07, c_08, c_09, c_10]

    supermarche = Supermarket(customers)
    while supermarche.step < 25:

        frame = img.copy()

        supermarche.update(frame)


        #cv2.imshow('frame', frame)

        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break

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

    logger.info(f'Programm has finished...')
