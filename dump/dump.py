"""Implements saving data to different targets. Implemented FileHandler that
saves data to json file, but one can imagine other possibilities like sending
data via sockets or SMTP"""
import json

WRITE_ONLY = 'w'


class Dumper:
    def __init__(self, handler):
        self._handler = handler

    def save(self, data):
        self._handler.emit(data)


class FileHandler:
    def __init__(self, filepath):
        self._filepath = filepath

    def emit(self, data):
        with open(self._filepath, WRITE_ONLY) as file:
            json.dump(data, file, indent=2)


class SocketHandler:
    def emit(self, data):
        raise NotImplementedError


class SMTPHandler:
    def emit(self, data):
        raise NotImplementedError
