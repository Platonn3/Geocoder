import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from Source.database.requests import return_address_if_exist, add_new_address
from Source.database.models import Address


class TestDatabaseFunctions(unittest.IsolatedAsyncioTestCase):

    @patch("Source.database.requests.async_session")
    async def test_return_address_if_exist_found(self, mock_async_session):
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none = MagicMock(return_value="address_obj")

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_async_session.return_value.__aenter__.return_value = mock_session

        result = await return_address_if_exist("test query")
        self.assertEqual(result, "address_obj")
        mock_session.execute.assert_awaited()

    @patch("Source.database.requests.async_session")
    async def test_return_address_if_exist_not_found(self, mock_async_session):
        # Setup mock
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none = MagicMock(return_value=None)

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_async_session.return_value.__aenter__.return_value = mock_session

        result = await return_address_if_exist("missing query")

        self.assertIsNone(result)

    # @patch("Source.database.requests.async_session")
    # async def test_add_new_address_success(self, mock_async_session):
    #     mock_session = AsyncMock()
    #     mock_async_session.return_value.__aenter__.return_value = mock_session
    #
    #     # Test data
    #     test_data = {
    #         "input_query": "test query",
    #         "full_address": "full test address",
    #         "lat": 12.34,
    #         "lon": 56.78
    #     }
    #
    #     # Test
    #     result = await add_new_address(
    #         input_query=test_data["input_query"],
    #         full_address=test_data["full_address"],
    #         lat=test_data["lat"],
    #         lon=test_data["lon"]
    #     )
    #
    #     # Assertions
    #     mock_session.begin.assert_called_once()
    #
    #     # Check that session.add was called with an Address object
    #     mock_session.add.assert_called_once()
    #     added_address = mock_session.add.call_args[0][0]
    #     self.assertIsInstance(added_address, Address)
    #     self.assertEqual(added_address.input_query, test_data["input_query"])
    #     self.assertEqual(added_address.full_address, test_data["full_address"])
    #     self.assertEqual(added_address.latitude, test_data["lat"])
    #     self.assertEqual(added_address.longitude, test_data["lon"])

    @patch("Source.database.requests.async_session")
    async def test_add_new_address_exception(self, mock_async_session):
        # Setup mock with exception
        mock_session = AsyncMock()
        mock_session.begin.return_value.__aenter__.side_effect = Exception("DB error")
        mock_async_session.return_value.__aenter__.return_value = mock_session

        # Test
        with self.assertRaises(Exception):
            await add_new_address(
                input_query="failing query",
                full_address="fail address",
                lat=0.0,
                lon=0.0
            )


if __name__ == "__main__":
    unittest.main()