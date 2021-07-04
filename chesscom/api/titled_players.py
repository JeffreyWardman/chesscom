from typing import Dict, List, Union

import requests

BASE_TITLED_URL = "https://api.chess.com/pub/titled"
VALID_TITLES = ["GM", "WGM", "IM", "WIM", "FM", "WFM", "NM", "WNM", "CM", "WCM"]


class TitledPlayers:
    @staticmethod
    def usernames(titles: Union[List[str], str]) -> Dict[str, List[str]]:
        usernames = {}
        for title in titles:
            api_url = f"{BASE_TITLED_URL}/{title}"
            response = requests.get(api_url).json()
            usernames[title] = response["players"]
        return usernames
