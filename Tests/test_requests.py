import unittest
from unittest.mock import patch, MagicMock

from requests import RequestException

from Sourse import response


class TestSendRequest(unittest.TestCase):

    @patch('Sourse.response.parse.parse_output_address')
    @patch('Sourse.response.requests.get')
    def test_send_request_successful_ekb(self, mock_get, mock_parse_output):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = '[{"display_name": "Храм на Крови, Екатеринбург, Россия", "lat": "56.837", "lon": "60.605"}]'
        mock_response.json.return_value = [
            {"display_name": "Храм на Крови, Екатеринбург, Россия", "lat": "56.837", "lon": "60.605"}
        ]
        mock_get.return_value = mock_response

        response.send_request("Храм на Крови Екатеринбург")

        mock_get.assert_called_once()
        mock_parse_output.assert_called_once_with({
            "display_name": "Храм на Крови, Екатеринбург, Россия",
            "lat": "56.837",
            "lon": "60.605"
        })

    @patch('builtins.print')
    @patch('Sourse.response.requests.get')
    def test_send_request_http_error(self, mock_get, mock_print):
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        response.send_request("Плотинка Екатеринбург")

        mock_print.assert_any_call("Ошибка HTTP: 500")

    @patch('builtins.print')
    @patch('Sourse.response.requests.get')
    def test_send_request_empty_response_text(self, mock_get, mock_print):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = ''
        mock_get.return_value = mock_response

        response.send_request("Улица Вайнера Екатеринбург")

        mock_print.assert_any_call("Пустой ответ от сервера")

    @patch('builtins.print')
    @patch('Sourse.response.requests.get')
    def test_send_request_no_data(self, mock_get, mock_print):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = '[]'
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        response.send_request("Неизвестное место в Екатеринбурге")

        mock_print.assert_any_call("Адрес не найден")

    @patch('builtins.print')
    @patch('Sourse.response.requests.get', side_effect=RequestException("Сетевая ошибка"))
    def test_send_request_network_error(self, mock_get, mock_print):
        response.send_request("Парк Маяковского Екатеринбург")
        mock_print.assert_any_call("Ошибка запроса Сетевая ошибка")
