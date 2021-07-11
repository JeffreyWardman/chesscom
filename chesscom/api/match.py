import requests

from ._match import LiveMatchDetails, MatchBoardDetails, MatchDetails, MatchResults

BASE_MATCH_URL = "https://api.chess.com/pub/match"


class Match:
    """Match API wrapper."""

    @staticmethod
    def daily_team_matches(match_id: str) -> MatchDetails:
        """Get daily team matches.

        Args:
            match_id (str): Match ID.

        Returns:
            MatchDetails: Match details class.
        """
        api_url = f"{BASE_MATCH_URL}/{match_id}"
        response = requests.get(api_url).json()
        return MatchDetails(**response)

    @staticmethod
    def team_match_board(match_id: str, board: int) -> MatchBoardDetails:
        """Get team match board.

        Args:
            match_id (str): Match ID.
            board (int): Board number.

        Returns:
            MatchBoardDetails: Match board details class.
        """
        api_url = f"{BASE_MATCH_URL}/{match_id}/{board}"
        response = requests.get(api_url).json()
        return MatchBoardDetails(**response)

    @staticmethod
    def live_match(live_match_id: str) -> LiveMatchDetails:
        """Get live match details.

        Args:
            live_match_id (str): Live match ID.

        Returns:
            LiveMatchDetails: Live match details class.
        """
        api_url = f"{BASE_MATCH_URL}/live/{live_match_id}"
        response = requests.get(api_url).json()
        response["id"] = response.pop("@id")
        return LiveMatchDetails(**response)

    @staticmethod
    def live_match_board(live_match_id: str, board: int) -> MatchBoardDetails:
        """Get live match board.

        Args:
            live_match_id (str): Live match ID.
            board (int): Board number.

        Returns:
            MatchBoardDetails: Match board details.
        """
        api_url = f"{BASE_MATCH_URL}/live/{live_match_id}/{board}"
        response = requests.get(api_url).json()
        return MatchBoardDetails(**response)
