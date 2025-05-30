import unittest
from unittest.mock import patch, AsyncMock, MagicMock
import requests

from Source.response import send_request


class TestSendRequest(unittest.IsolatedAsyncioTestCase):

    @patch("Source.response.requests.get")
    @patch("Source.response.return_address_if_exist", new_callable=AsyncMock)
    @patch("Source.response.parse.parse_output_address", new_callable=AsyncMock)
    async def test_send_request_success(self, mock_parse, mock_return, mock_get):
        mock_return.return_value = None

        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.return_value = [{
            "display_name": "Екатеринбург, Россия",
            "lat": "56.8389",
            "lon": "60.6057"
        }]
        mock_get.return_value = mock_resp

        await send_request("Екатеринбург")
        mock_get.assert_called_once()
        mock_parse.assert_awaited_once()

    @patch("Source.response.requests.get")
    @patch("Source.response.return_address_if_exist", new_callable=AsyncMock)
    async def test_send_request_empty_result(self, mock_return, mock_get):
        # Адреса нет в БД — запрос вернул пустой список
        mock_return.return_value = None

        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.return_value = []
        mock_get.return_value = mock_resp

        with patch("builtins.print") as mock_print:
            await send_request("пустой адрес")
            mock_print.assert_any_call("Адрес не найден")

    @patch("Source.response.requests.get")
    @patch("Source.response.return_address_if_exist", new_callable=AsyncMock)
    async def test_send_request_http_error(self, mock_return, mock_get):
        mock_return.return_value = None

        mock_resp = MagicMock()
        mock_resp.ok = False
        mock_resp.status_code = 500
        mock_get.return_value = mock_resp

        with patch("builtins.print") as mock_print:
            await send_request("ошибочный адрес")
            mock_print.assert_any_call("Ошибка HTTP: 500")

    @patch("Source.response.requests.get", side_effect=requests.exceptions.RequestException("timeout"))
    @patch("Source.response.return_address_if_exist", new_callable=AsyncMock)
    async def test_send_request_request_exception(self, mock_return, mock_get):
        mock_return.return_value = None

        with patch("builtins.print") as mock_print:
            await send_request("ошибочный адрес")
            mock_print.assert_any_call("Ошибка запроса: timeout")

    @patch("Source.response.return_address_if_exist", new_callable=AsyncMock)
    async def test_send_request_from_cache(self, mock_return):
        mock_address = MagicMock()
        mock_address.latitude = "56.8389"
        mock_address.longitude = "60.6057"
        mock_address.full_address = "Екатеринбург, Россия"
        mock_return.return_value = mock_address

        with patch("builtins.print") as mock_print:
            await send_request("Екатеринбург")
            mock_print.assert_any_call("Широта: 56.8389")
            mock_print.assert_any_call("Долгота: 60.6057")
            mock_print.assert_any_call("Полный адрес: Екатеринбург, Россия")

if __name__ == "__main__":
    unittest.main()
