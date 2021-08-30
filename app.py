"""Entry file for application"""
from logging import DEBUG

from argparser.argparser import get_input_args
from logger import configure_logger


if __name__ == '__main__':
    configure_logger(DEBUG)
    input_args = get_input_args()
