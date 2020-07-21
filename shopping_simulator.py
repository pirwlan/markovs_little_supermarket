from dotenv import load_dotenv

import logging
import os
import get_transitional_probabilities as tp


def shopping_simulator():

    trans_prob_matrix = tp.calculate_tp()
    print(trans_prob_matrix)


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
    
    logger.info(f'Programm has finished-..')