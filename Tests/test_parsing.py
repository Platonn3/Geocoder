import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from Source.parsing import (
    clean_address,
    build_normalized_address,
    sanitize_input,
    parse_input_address,
    parse_input_coordinates,
    parse_output_address,
    choose_input,
)

MOCK_CLEANED_ADDRESS = {
    "street": "Урицкого",
    "house": "7",
    "city": "Екатеринбург",
    "region": "Свердловская",
    "country": "Россия"
}

MOCK_OUTPUT_ADDRESS = {
    "display_name": "Урицкого 7, Екатеринбург, Свердловская, Россия",
    "lat": "56.8389",
    "lon": "60.6057"
}

class TestGeocoderLogic(unittest.IsolatedAsyncioTestCase):
    @patch("Source.parsing.dadata.clean")
    def test_clean_address_success(self, mock_clean):
        mock_clean.return_value = MOCK_CLEANED_ADDRESS
        result = clean_address("Урицкого 7 Екатеринбург Россия")
        self.assertEqual(result, MOCK_CLEANED_ADDRESS)

    @patch("Source.parsing.dadata.clean", side_effect=Exception("Dadata error"))
    def test_clean_address_failure(self, mock_clean):
        result = clean_address("Некорректный адрес")
        self.assertIsNone(result)

    def test_build_normalized_address_full(self):
        result = build_normalized_address(MOCK_CLEANED_ADDRESS)
        self.assertEqual(result, "Урицкого 7 Екатеринбург Свердловская Россия")

    def test_build_normalized_address_empty(self):
        self.assertIsNone(build_normalized_address({}))

    @patch("builtins.input", side_effect=["екатеринбург", "урицкого", "7"])
    @patch("Source.parsing.clean_address", return_value=MOCK_CLEANED_ADDRESS)
    @patch("Source.parsing.build_normalized_address", return_value="Урицкого 7 Екатеринбург Свердловская Россия")
    @patch("Source.parsing.req.send_request", new_callable=AsyncMock)
    async def test_parse_input_address_success(self, mock_send, mock_build, mock_clean, mock_input):
        await parse_input_address()
        mock_send.assert_awaited_once()

    @patch("builtins.input", side_effect=["екатеринбург", "урицкого", "7"])
    @patch("Source.parsing.clean_address", return_value=None)
    async def test_parse_input_address_clean_fail(self, mock_clean, mock_input):
        await parse_input_address()

    @patch("builtins.input", return_value="56.8389 60.6057")
    @patch("Source.parsing.req.send_request", new_callable=AsyncMock)
    async def test_parse_input_coordinates_success(self, mock_send, mock_input):
        await parse_input_coordinates()
        mock_send.assert_awaited_once_with("56.8389 60.6057")

    @patch("builtins.input", return_value="abc def")
    async def test_parse_input_coordinates_invalid(self, mock_input):
        await parse_input_coordinates()

    async def test_parse_output_address_success(self):
        with patch("Source.parsing.add_new_address", new_callable=AsyncMock) as mock_add:
            await parse_output_address("Урицкого 7 Екатеринбург", MOCK_OUTPUT_ADDRESS)
            mock_add.assert_awaited_once()

    async def test_parse_output_address_no_data(self):
        await parse_output_address("Урицкого 7 Екатеринбург", {})

    async def test_parse_output_address_not_russia(self):
        not_russia = MOCK_OUTPUT_ADDRESS.copy()
        not_russia["display_name"] = "Somewhere Else"
        await parse_output_address("address", not_russia)

    @patch("Source.parsing.parse_input_coordinates", new_callable=AsyncMock)
    @patch("Source.parsing.parse_input_address", new_callable=AsyncMock)
    async def test_choose_input(self, mock_address, mock_coords):
        await choose_input("1")
        mock_coords.assert_awaited_once()

        await choose_input("2")
        mock_address.assert_awaited_once()

    async def test_choose_input_invalid(self):
        await choose_input("3")

if __name__ == "__main__":
    unittest.main()
