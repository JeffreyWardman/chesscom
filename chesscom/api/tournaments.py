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
    @staticmethod
    def get(tournament_id: str) -> TournamentDetails:
        api_url = f"{BASE_TOURNAMENT_URL}/{tournament_id}"
        response = requests.get(api_url).json()
        return TournamentDetails(**response)

    @staticmethod
    def get_round(tournament_id: str, tournament_round: str) -> TournamentRoundDetails:
        api_url = f"{BASE_TOURNAMENT_URL}/{tournament_id}/{tournament_round}"
        response = requests.get(api_url).json()
        return TournamentRoundDetails(**response)

    @staticmethod
    def get_round_group(
        tournament_id: str,
        tournament_round: str,
        tournament_group: str,
    ) -> TournamentRoundGroupDetails:
        api_url = f"{BASE_TOURNAMENT_URL}/{tournament_id}/{tournament_round}/{tournament_group}"
        response = requests.get(api_url).json()
        return TournamentRoundGroupDetails(**response)
