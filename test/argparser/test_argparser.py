import unittest
from unittest.mock import Mock, patch

from argparser.argparser import get_input_args as uut


class Dummy:
    """Class to provide __dict__ in tests for vars(...)"""
    def __init__(self, item):
        self._item = item


class TestArgparser(unittest.TestCase):
    @patch('argparser.argparser.argparse.ArgumentParser')
    def test_get_input_args(self, argument_parser_type_mock):
        dummy_args = Dummy('dummy_value')
        expected_dict = {'_item': 'dummy_value'}

        parser_mock = Mock()
        parser_mock.parse_args.return_value = dummy_args

        argument_parser_type_mock.return_value = parser_mock

        result = uut()

        self.assertEqual(result, expected_dict)
        argument_parser_type_mock.assert_called_once()
        parser_mock.add_argument.assert_called_once_with('-c',
                                                         '--config',
                                                         help='Path to config with www pages metadata',
                                                         required=True)

    def test_get_input_args_when_no_args_provided(self):
        with self.assertRaises(SystemExit):
            uut()
