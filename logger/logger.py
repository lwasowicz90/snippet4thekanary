"""Module for configuring logger"""
import datetime
import logging
from os import path, mkdir


LOG_DIR = "log"
DATE_FORMATTER = logging.Formatter(fmt='%(asctime)s - %(name)s -  %(levelname)s - %(message)s',
                                   datefmt='%d-%m-%Y %H:%M:%S')


def configure_logger(level: int):
    """Execute this on app startup"""
    _create_log_dir(LOG_DIR)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    stream_handler = _create_stream_handler(level)
    root_logger.addHandler(stream_handler)

    filepath = datetime.datetime.today().strftime("{}/%Y-%m-%d-%H-%M-%S.log".format(LOG_DIR))
    file_handler = _create_file_handler(filepath=filepath, level=level)
    root_logger.addHandler(file_handler)
    root_logger.info("Configured logger.")


def _create_log_dir(dir_name: str):
    """Creates log directory if needed"""
    if not path.exists(dir_name):
        mkdir(dir_name)


def _create_file_handler(filepath: str, level: int):
    """Helper function for creating file logger"""
    assert filepath, "Expecting not empty filename!!!"
    file_handler = logging.FileHandler(filepath)
    file_handler.setLevel(level)
    file_handler.setFormatter(DATE_FORMATTER)
    return file_handler


def _create_stream_handler(level: int):
    """Helper function for creating console logger"""
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(DATE_FORMATTER)
    return stream_handler
