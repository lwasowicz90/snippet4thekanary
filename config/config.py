"""Module for reading and validating the config. Config keeps metadata of data provider"""
import collections
import logging
import sys
import json
from io import TextIOWrapper

READ_ONLY = 'r'
ENCODING = 'utf-8'
logger = logging.getLogger('config')


class ContextManagerError(Exception):
    """Exception when user would not use class JsonDataLoader as context manager"""


class JsonDataLoader:
    """Kind of wrapper for reading data from json file. Instead using this class one could make a use of
    contexlib.contextmanager combined with free function instead of class"""
    def __init__(self, filepath: str):
        self._filepath = filepath
        self._context = False
        self._data = None
        self._file = None

    def __enter__(self):
        """contextmanager support"""
        self._context = True
        self._file = JsonDataLoader._load_file(self._filepath)
        self._data = JsonDataLoader._load_json(self._file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """contextmanager support"""
        self._file.close()
        return False  # do not swallow the exceptions

    @property
    def data(self) -> dict:
        """Property for obtaining config data"""
        if not self._context:
            raise ContextManagerError("Usage of the class is allowed only through context manager!")
        return self._data

    @staticmethod
    def _load_file(filepath: str) -> TextIOWrapper:
        """Loads file"""
        try:
            return open(filepath, READ_ONLY, encoding=ENCODING)
        except OSError:
            logger.exception("Cannot load file {}!".format(filepath))  # pylint: disable=W1202
            sys.exit(1)
        except Exception:  # pylint: disable=W0703
            logger.exception("Unexpected exception when reading the file {}!".format(filepath))  # pylint: disable=W1202
            sys.exit(10)

    @staticmethod
    def _load_json(file: TextIOWrapper) -> dict:
        """Reads json content"""
        try:
            return json.load(file)
        except ValueError:
            logger.exception("Incorrect json format!")
            sys.exit(2)
        except Exception:  # pylint: disable=W0703
            logger.exception("Unexpected exception when loading json data")
            sys.exit(10)


ConfigField = collections.namedtuple('ConfigField', 'key type')
MANDATORY_FIELDS = [ConfigField('url', str), ConfigField('xhr', str)]


def validate(config: dict) -> None:
    """Validates if config has all necessary fields, otherwise exit"""

    for field in MANDATORY_FIELDS:
        for config_value in config.values():
            if not (field.key in config_value and isinstance(config_value[field.key], field.type)):
                # pylint: disable=W1202
                logger.error("Config validation failed. Expecting key: {} of type {}".format(field.key,field.type))
                sys.exit(3)
