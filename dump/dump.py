"""Implements saving data to different targets. Implemented FileHandler that
saves data to json file, but one can imagine other possibilities like sending
data via sockets or SMTP"""
import json

WRITE_ONLY = 'w'
ENCODING = 'utf-8'


class Dumper:
    """Class that takes saving handler and delegates saving there"""
    # pylint: disable=R0903
    def __init__(self, handler):
        self._handler = handler

    def save(self, data):
        """Executes saving on handler"""
        self._handler.emit(data)


class FileHandler:
    """Handler for json file"""
    # pylint: disable=R0903
    def __init__(self, filepath):
        self._filepath = filepath

    def emit(self, data):
        """Saves json data to file"""
        with open(self._filepath, WRITE_ONLY, encoding=ENCODING) as file:
            json.dump(data, file, indent=2)


class SocketHandler:
    # pylint: disable=C0115
    # pylint: disable=R0903
    def emit(self, data):
        # pylint: disable=C0116
        raise NotImplementedError


class SMTPHandler:
    # pylint: disable=C0115
    # pylint: disable=R0903
    def emit(self, data):
        # pylint: disable=C0116
        raise NotImplementedError
