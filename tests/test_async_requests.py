import unittest
from unittest.mock import AsyncMock, Mock, patch

from utils.requests.async_tools import fetch_first


class AsyncRequestTests(unittest.IsolatedAsyncioTestCase):
    async def test_retry_failure_preserves_root_cause_in_message(self):
        session = Mock()
        session.get.side_effect = TimeoutError("TLS handshake timed out")

        with patch("utils.requests.async_tools.asyncio.sleep", new=AsyncMock()):
            with self.assertRaises(Exception) as raised:
                await fetch_first(
                    session,
                    ["https://example.com/list.m3u"],
                    name="https://example.com/list.m3u",
                )

        self.assertIn("TimeoutError", str(raised.exception))
        self.assertIn("TLS handshake timed out", str(raised.exception))
        self.assertIsInstance(raised.exception.__cause__, TimeoutError)


if __name__ == "__main__":
    unittest.main()
