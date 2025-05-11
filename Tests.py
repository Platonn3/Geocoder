import unittest
import parsing as parse
from unittest.mock import patch


class TestChooseInput(unittest.TestCase):

    @patch('builtins.input', side_effect=['1'])
    @patch('parsing.parse_input_coordinates')
    def test_choose_input_coordinates(self, mock_coords, mock_input):
        parse.choose_input()
        mock_coords.assert_called_once()

    @patch('builtins.input', side_effect=['2'])
    @patch('parsing.parse_input_address')
    def test_choose_input_address(self, mock_address, mock_input):
        parse.choose_input()
        mock_address.assert_called_once()

    @patch('builtins.input', side_effect=['abc'])
    def test_choose_input_value_error(self, mock_input):
        with patch('builtins.print') as mock_print:
            parse.choose_input()
            mock_print.assert_any_call("Ошибка ввода, выберете 1 или 2 вариант")

    @patch('builtins.input', side_effect=['5'])
    def test_choose_input_out_of_range(self, mock_input):
        with patch('builtins.print') as mock_print:
            parse.choose_input()
            mock_print.assert_any_call("Ошибка ввода, выберете 1 или 2 вариант")



