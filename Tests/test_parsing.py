import unittest
from unittest.mock import patch
from Source import parsing


class TestParsingInputErrors(unittest.TestCase):

    @patch('builtins.print')
    def test_choose_input_non_number(self, mock_print):
        parsing.choose_input('abc')
        self.assertTrue(any("Ошибка:" in call[0][0] for call in mock_print.call_args_list))

    @patch('builtins.print')
    def test_choose_input_wrong_number(self, mock_print):
        parsing.choose_input('5')
        mock_print.assert_any_call("Ошибка: выберите 1 или 2.")

    @patch('builtins.input', side_effect=['abc', 'def'])
    @patch('builtins.print')
    def test_parse_input_coordinates_non_float(self, mock_print, mock_input):
        parsing.parse_input_coordinates()
        mock_print.assert_any_call("Ошибка ввода координат. Убедитесь, что вводите числа.")

    @patch('builtins.input', side_effect=['55.75', 'xyz'])
    @patch('builtins.print')
    def test_parse_input_coordinates_one_float_one_string(self, mock_print, mock_input):
        parsing.parse_input_coordinates()
        mock_print.assert_any_call("Ошибка ввода координат. Убедитесь, что вводите числа.")
