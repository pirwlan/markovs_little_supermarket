from Customer import Customer
from dotenv import load_dotenv
from Supermarket import Supermarket

import cv2
import get_transitional_probabilities as tp
import logging
import os


def shopping_simulator():
    img = cv2.imread(os.getenv('SUPERMARKET_IMG_PATH'))

    tp.calculate_tp()
    c_01 = Customer(1)
    c_02 = Customer(2)

    customers = [c_01, c_02]
    supermarche = Supermarket(customers)
    while True:

        frame = img.copy()

        supermarche.update(frame)
        print(supermarche)

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
