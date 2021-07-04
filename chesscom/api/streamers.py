from typing import List

import requests

from ._streamers import StreamerDetails

BASE_STREAMERS_URL = f"https://api.chess.com/pub/streamers"


class Streamers:
    @staticmethod
    def list_all() -> List[StreamerDetails]:
        """Note: the endpoint refreshes every 5 minutes."""
        response = requests.get(BASE_STREAMERS_URL).json()
        streamers = response["streamers"]
        return [StreamerDetails(**x) for x in streamers]
