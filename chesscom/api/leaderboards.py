import requests

from ._leaderboards import LeaderboardDetails

BASE_LEADERBOARD_URL = "https://api.chess.com/pub/leaderboards"


class Leaderboards:
    """Leaderboards API wrapper."""

    @staticmethod
    def get_all() -> LeaderboardDetails:
        """Get leaderboards information for all game modes.

        Note: Endpoint refreshes when one of the leaderboards is updated.

        Returns:
            LeaderboardDetails: Leaderboard details class.
        """
        response = requests.get(BASE_LEADERBOARD_URL).json()
        return LeaderboardDetails(**response)
