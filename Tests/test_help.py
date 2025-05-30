import unittest
from unittest import mock
from unittest.mock import patch, AsyncMock
import sys
import asyncio

import main


class TestMain(unittest.IsolatedAsyncioTestCase):

    @patch("builtins.print")
    def test_show_help(self, mock_print):
        main.show_help()
        mock_print.assert_called()

    @patch("main.parse.choose_input", new_callable=AsyncMock)
    async def test_process_command_choose_input(self, mock_choose_input):
        await main.process_command("1")
        mock_choose_input.assert_awaited_once_with("1")

        mock_choose_input.reset_mock()
        await main.process_command("2")
        mock_choose_input.assert_awaited_once_with("2")

    @patch("builtins.print")
    async def test_process_command_help(self, mock_print):
        await main.process_command("--help")
        mock_print.assert_called()

        mock_print.reset_mock()
        await main.process_command("-h")
        mock_print.assert_called()

    @patch("builtins.print")
    async def test_process_command_unknown(self, mock_print):
        await main.process_command("unknown_command")
        mock_print.assert_called_with("Неизвестная команда. Введите --help для справки.")

    @patch("sys.exit")
    @patch("builtins.print")
    async def test_process_command_exit(self, mock_print, mock_exit):
        await main.process_command("exit")
        mock_exit.assert_called_once_with(0)
        mock_print.assert_called_with("Выход из программы.")

    @patch("builtins.input", side_effect=["exit"])
    @patch("main.process_command", new_callable=AsyncMock)
    async def test_interactive_mode_exit(self, mock_process_command, mock_input):
        with self.assertRaises(SystemExit):
            await main.interactive_mode()
        mock_process_command.assert_awaited_once_with("exit")

    @patch("main.init_db", new_callable=AsyncMock)
    @patch("main.parse.choose_input", new_callable=AsyncMock)
    @patch("sys.argv", ["main.py", "1"])
    @patch("sys.exit")
    async def test_main_with_args_1(self, mock_exit, mock_choose_input, mock_init_db):
        await main.main()
        mock_choose_input.assert_awaited_once_with("1")
        mock_exit.assert_called_once_with(0)

    @patch("main.init_db", new_callable=AsyncMock)
    @patch("builtins.print")
    @patch("sys.argv", ["main.py", "--help"])
    @patch("sys.exit")
    async def test_main_with_help(self, mock_exit, mock_print, mock_init_db):
        await main.main()
        mock_print.assert_called()
        mock_exit.assert_called_once_with(0)

    @patch("main.init_db", new_callable=AsyncMock)
    @patch("builtins.print")
    @patch("sys.argv", ["main.py", "exit"])
    @patch("sys.exit")
    async def test_main_with_exit(self, mock_exit, mock_print, mock_init_db):
        await main.main()
        mock_print.assert_called_with("Выход из программы.")
        mock_exit.assert_called_once_with(0)

    @patch("main.init_db", new_callable=AsyncMock)
    @patch("builtins.print")
    @patch("sys.argv", ["main.py", "invalid"])
    @patch("sys.exit")
    async def test_main_invalid_arg(self, mock_exit, mock_print, mock_init_db):
        await main.main()
        mock_print.assert_any_call("Неизвестная команда: invalid")
        mock_exit.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
