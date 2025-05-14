import unittest
from unittest.mock import patch
import main


class TestMainHelp(unittest.TestCase):

    @patch('builtins.print')
    def test_show_help_output(self, mock_print):
        main.show_help()
        mock_print.assert_any_call("""
Доступные команды:
1 — Ввести координаты (широта и долгота)
2 — Ввести адрес (город, улица, дом)
--help — Показать справку
exit — Выйти из программы
""")

    @patch('builtins.input', side_effect=['--help', 'exit'])
    @patch('builtins.print')
    def test_main_help_command(self, mock_print, mock_input):
        main.main()
        mock_print.assert_any_call("""
Доступные команды:
1 — Ввести координаты (широта и долгота)
2 — Ввести адрес (город, улица, дом)
--help — Показать справку
exit — Выйти из программы
""")
        mock_print.assert_any_call("Выход из программы.")

