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
    start = False
    tp.calculate_tp()

    supermarche = Supermarket(num_checkout=int(os.getenv('NUMBER_OF_CHECKOUTS')))

    canvas = np.zeros([780, 1752, 3], dtype='uint8')

    while supermarche.step < 1000:
        frame = canvas.copy()
        frame[0:int(os.getenv('SUPERMARKET_IMG_HEIGHT')), 0:int(os.getenv('SUPERMARKET_IMG_WIDTH'))] = supermarket_img

        if start:

            supermarche.update_step(frame)

            frame = utils.draw_distribution(frame, supermarche.dist_curr, supermarche.step)
            frame = utils.draw_turnover(frame, supermarche.turnover_history)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        elif cv2.waitKey(1) & 0xFF == ord('w'):
            start = True

    cv2.destroyAllWindows()
    utils.make_dist_gif(supermarche.dist_cust)


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
