import requests

from ._tournaments import (
    TournamentDetails,
    TournamentRoundDetails,
    TournamentRoundGroupDetails,
)

BASE_TOURNAMENT_URL = "https://api.chess.com/pub/tournament"
TOURNAMENT_STATUSES = ["winner", "eliminated", "withdrew", "removed"]
INVITATION_STATUSES = ["invited", "registered"]


class Tournament:
    """Tournament API wrapper."""

    @staticmethod
    def get(tournament_id: str) -> TournamentDetails:
        """Get tournament details.

        Args:
            tournament_id (str): Tournament ID.

        Returns:
            TournamentDetails: Tournament details class.
        """
        api_url = f"{BASE_TOURNAMENT_URL}/{tournament_id}"
        response = requests.get(api_url).json()
        return TournamentDetails(**response)

    @staticmethod
    def get_round(tournament_id: str, tournament_round: str) -> TournamentRoundDetails:
        """Get tournament round details.

        Args:
            tournament_id (str): Tournament ID.
            tournament_round (str): Tournament round.

        Returns:
            TournamentRoundDetails: Tournament round details class.
        """
        api_url = f"{BASE_TOURNAMENT_URL}/{tournament_id}/{tournament_round}"
        response = requests.get(api_url).json()
        return TournamentRoundDetails(**response)

    @staticmethod
    def get_round_group(
        tournament_id: str,
        tournament_round: str,
        tournament_group: str,
    ) -> TournamentRoundGroupDetails:
        """Get tournament round group details.

        Args:
            tournament_id (str): Tournament ID.
            tournament_round (str): Tournament round.
            tournament_group (str): Tournament group.

        Returns:
            TournamentRoundGroupDetails: [description]
        """
        api_url = f"{BASE_TOURNAMENT_URL}/{tournament_id}/{tournament_round}/{tournament_group}"
        response = requests.get(api_url).json()
        return TournamentRoundGroupDetails(**response)
