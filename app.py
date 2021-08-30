"""Entry file for application"""
from logging import DEBUG

from logger import configure_logger


if __name__ == '__main__':
    configure_logger(DEBUG)
