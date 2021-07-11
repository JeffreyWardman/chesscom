from typing import List

import requests

from ._streamers import StreamerDetails

BASE_STREAMERS_URL = f"https://api.chess.com/pub/streamers"


class Streamers:
    """Streamers API wrapper."""

    @staticmethod
    def list_all() -> List[StreamerDetails]:
        """List all streamers.

        Note: Endpoint refreshes at most every 5 minutes.

        Returns:
            List[StreamerDetails]: List of all streamers.
        """
        response = requests.get(BASE_STREAMERS_URL).json()
        streamers = response["streamers"]
        return [StreamerDetails(**x) for x in streamers]
