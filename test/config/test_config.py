import json
import unittest
from unittest.mock import mock_open, patch, Mock
from json.decoder import JSONDecodeError

from config.config import JsonDataLoader, ContextManagerError, READ_ONLY, validate, ENCODING


class TestJsonDataLoaderStatic(unittest.TestCase):
    def test_load_file(self):
        uut = JsonDataLoader._load_file

        dummy_filepath = 'some/path/file.ext'
        dummy_file = "some_file"

        with patch('builtins.open', mock_open()) as open_mock:
            open_mock.return_value = dummy_file
            result = uut(dummy_filepath)
            open_mock.assert_called_once_with(dummy_filepath, READ_ONLY, encoding=ENCODING)

        self.assertEqual(result, dummy_file)

    def test_load_file_when_not_exists(self):
        uut = JsonDataLoader._load_file

        dummy_filepath = 'some/path/file.ext'

        with patch('builtins.open', mock_open()) as open_mock:
            open_mock.side_effect = FileNotFoundError
            with self.assertRaises(SystemExit) as e:
                uut(dummy_filepath)

        self.assertEqual(e.exception.code, 1)

    def test_load_file_when_unexpected_error(self):
        uut = JsonDataLoader._load_file

        dummy_filepath = 'some/path/file.ext'

        with patch('builtins.open', mock_open()) as open_mock:
            open_mock.side_effect = Exception
            with self.assertRaises(SystemExit) as e:
                uut(dummy_filepath)

        self.assertEqual(e.exception.code, 10)

    @patch('config.config.json.load')
    def test_load_json(self, load_json_mock):
        uut = JsonDataLoader._load_json

        dummy_file = "some_file"  # for simplicity use str instead of TextIOWrapper
        dummy_config = {'x': 1, 'b': 'xzx'}
        load_json_mock.return_value = dummy_config

        result = uut(dummy_file)

        self.assertEqual(result, dummy_config)

    @patch('config.config.json.load')
    def test_load_json_decode_error(self, load_json_mock):
        uut = JsonDataLoader._load_json

        dummy_file = "some_file"  # for simplicity use str instead of TextIOWrapper
        load_json_mock.side_effect = JSONDecodeError(msg='', doc='', pos=0)

        with self.assertRaises(SystemExit) as e:
            uut(dummy_file)

        self.assertEqual(e.exception.code, 2)

    @patch('config.config.json.load')
    def test_load_json_unknown_error(self, load_json_mock):
        uut = JsonDataLoader._load_json

        dummy_file = "some_file"  # for simplicity use str instead of TextIOWrapper
        load_json_mock.side_effect = Exception

        with self.assertRaises(SystemExit) as e:
            uut(dummy_file)

        self.assertEqual(e.exception.code, 10)


class TestJsonDataLoader(unittest.TestCase):
    def setUp(self):
        self._dummy_filepath = 'some/path/file.json'

    def test_data_property_wo_context_manager(self):
        uut = JsonDataLoader(self._dummy_filepath)

        result = None
        with self.assertRaises(ContextManagerError):
            result = uut.data

        self.assertEqual(result, None)

    @patch('config.config.JsonDataLoader._load_json')
    @patch('config.config.JsonDataLoader._load_file')
    def test_data_property(self, load_file_mock, load_json_mock):
        dummy_file_mock = Mock()
        dummy_data = {'some_key': 'some_value'}
        load_file_mock.return_value = dummy_file_mock
        load_json_mock.return_value = dummy_data

        with JsonDataLoader(dummy_file_mock) as uut:
            data = uut.data

        dummy_file_mock.close.assert_called_once()
        self.assertEqual(data, dummy_data)

class TestValidateConfig(unittest.TestCase):
    def setUp(self):
        self.uut = validate

    def test_validate(self):
        valid_config = {
            "some_site": {
                "url": "https://hostname.com",
                "xhr": "xxx"
            },
            "some_site2": {
                "url": "https://hostname2.com",
                "xhr": "xxx"
            }
        }

        self.uut(valid_config)

    def test_validate_when_url_not_string(self):
        broken_config = {
            "some_site": {
                "url": "https://hostname.com",
                "xhr": "xxx"
            },
            "some_site2": {
                "url": 123,
                "xhr": "xxx"
            }
        }
        with self.assertRaises(SystemExit) as e:
            self.uut(broken_config)

        self.assertEqual(e.exception.code, 3)

    def test_validate_when_xhr_not_string(self):
        broken_config = {
            "some_site": {
                "url": "https://hostname.com",
                "xhr": "xxx"
            },
            "some_site2": {
                "url": "https://hostname2.com",
                "xhr": 22
            }
        }
        with self.assertRaises(SystemExit) as e:
            self.uut(broken_config)

        self.assertEqual(e.exception.code, 3)

    def test_validate_when_missing_xhr_key(self):
        broken_config = {
            "some_site": {
                "url": "https://hostname.com",
                "xhr": "xxx"
            },
            "some_site2": {
                "url": "https://hostname2.com",
                "other": 'xxx'
            }
        }
        with self.assertRaises(SystemExit) as e:
            self.uut(broken_config)

        self.assertEqual(e.exception.code, 3)

    def test_validate_when_missing_url_key(self):
        broken_config = {
            "some_site": {
                "url": "https://hostname.com",
                "xhr": "xxx"
            },
            "some_site2": {
                "other": "https://hostname2.com",
                "xhr": 'xxx'
            }
        }
        with self.assertRaises(SystemExit) as e:
            self.uut(broken_config)

        self.assertEqual(e.exception.code, 3)
