import os

from Customer import Customer
from dotenv import load_dotenv

import cv2
import get_transitional_probabilities as tp
import logging
import os
import time


def shopping_simulator():
    img = cv2.imread(os.getenv('SUPERMARKET_IMG_PATH'))

    tp.calculate_tp()
    c_01 = Customer(1)
    c_02 = Customer(2)
    c_03 = Customer(3)
    c_04 = Customer(4)
    c_05 = Customer(5)
    c_06 = Customer(6)

    customers = [c_01]

    while True:

        frame = img.copy()

        for customer in customers:
            customer.draw(frame)
            customer.transition()

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


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
