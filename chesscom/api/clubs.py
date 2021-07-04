import requests

from ._clubs import ClubDetails, ClubMatches, ClubMembers

BASE_CLUB_URL = "https://api.chess.com/pub/club"


class Club:
    @staticmethod
    def details(club_id: str) -> ClubDetails:
        api_url = f"{BASE_CLUB_URL}/{club_id}"
        response = requests.get(api_url).json()
        response["id"] = response.pop("@id")
        return ClubDetails(**response)

    @staticmethod
    def members(club_id: str) -> ClubMembers:
        api_url = f"{BASE_CLUB_URL}/{club_id}/members"
        response = requests.get(api_url).json()
        return ClubMembers(**response)

    @staticmethod
    def matches(club_id: str) -> ClubMatches:
        api_url = f"{BASE_CLUB_URL}/{club_id}/matches"
        response = requests.get(api_url).json()
        return ClubMatches(**response)
