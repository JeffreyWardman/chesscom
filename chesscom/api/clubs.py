import requests

from ._clubs import ClubDetails, ClubMatches, ClubMembers

BASE_CLUB_URL = "https://api.chess.com/pub/club"


class Club:
    """Club API wrapper."""

    @staticmethod
    def details(club_id: str) -> ClubDetails:
        """Get club details.

        Args:
            club_id (str): Club ID.

        Returns:
            ClubDetails: Club details class.
        """
        api_url = f"{BASE_CLUB_URL}/{club_id}"
        response = requests.get(api_url).json()
        response["id"] = response.pop("@id")
        return ClubDetails(**response)

    @staticmethod
    def members(club_id: str) -> ClubMembers:
        """Get club members.

        Note: Endpoint refreshes at most every 12 hours.

        Args:
            club_id (str): Club ID.

        Returns:
            ClubMembers: Club members class.
        """
        api_url = f"{BASE_CLUB_URL}/{club_id}/members"
        response = requests.get(api_url).json()
        return ClubMembers(**response)

    @staticmethod
    def matches(club_id: str) -> ClubMatches:
        """Get club matches.

        Args:
            club_id (str): Club ID.

        Returns:
            ClubMatches: Club matches class.
        """
        api_url = f"{BASE_CLUB_URL}/{club_id}/matches"
        response = requests.get(api_url).json()
        return ClubMatches(**response)
