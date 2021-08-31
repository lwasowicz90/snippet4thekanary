"""Entry file for application"""
from logging import DEBUG
import datetime


from argparser.argparser import get_input_args
from dump.dump import Dumper, FileHandler
from logger import configure_logger
from provider.manager import ProviderManager


if __name__ == '__main__':
    configure_logger(DEBUG)
    config_path = get_input_args()['config']
    provider = ProviderManager(config_path)
    provider.process()

    filepath = datetime.datetime.today().strftime("data/%Y-%m-%d-%H-%M-%S-headlines.json")
    Dumper(handler=FileHandler(filepath)).save(provider.headlines)
