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

    supermarche = Supermarket()

    for i in range(20):
        supermarche.add_customer(customer=Customer(customer_id=i))

    while supermarche.step < 25:

        frame = img.copy()

        supermarche.update(frame)

        #cv2.imshow('frame', frame)

        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break

    #cv2.destroyAllWindows()
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
    #utils.get_supermarket_mask()
    logger.info(f'Programm has finished...')
