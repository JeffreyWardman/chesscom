import requests

from ._match import LiveMatchDetails, MatchBoardDetails, MatchDetails, MatchResults

BASE_MATCH_URL = "https://api.chess.com/pub/match"


class Match:
    @staticmethod
    def daily_team_matches(match_id: str) -> MatchDetails:
        api_url = f"{BASE_MATCH_URL}/{match_id}"
        response = requests.get(api_url).json()
        return MatchDetails(**response)

    @staticmethod
    def team_match_board(match_id: str, board: int) -> MatchBoardDetails:
        api_url = f"{BASE_MATCH_URL}/{match_id}/{board}"
        response = requests.get(api_url).json()
        return MatchBoardDetails(**response)

    @staticmethod
    def live_match(live_match_id: str) -> LiveMatchDetails:
        api_url = f"{BASE_MATCH_URL}/live/{live_match_id}"
        response = requests.get(api_url).json()
        response["id"] = response.pop("@id")
        return LiveMatchDetails(**response)

    @staticmethod
    def live_match_board(live_match_id: str, board: int) -> MatchBoardDetails:
        api_url = f"{BASE_MATCH_URL}/live/{live_match_id}/{board}"
        response = requests.get(api_url).json()
        return MatchBoardDetails(**response)
