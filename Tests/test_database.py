import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from Source.database.requests import return_address_if_exist, add_new_address

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
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none = MagicMock(return_value=None)

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_async_session.return_value.__aenter__.return_value = mock_session

        result = await return_address_if_exist("missing query")
        self.assertIsNone(result)




if __name__ == "__main__":
    unittest.main()
