import requests

from chesscom.api.match import BASE_MATCH_URL

from ._leaderboards import LeaderboardDetails

BASE_LEADERBOARD_URL = "https://api.chess.com/pub/leaderboards"


class Leaderboards:
    @staticmethod
    def get_all() -> LeaderboardDetails:
        response = requests.get(BASE_LEADERBOARD_URL).json()
        return LeaderboardDetails(**response)
