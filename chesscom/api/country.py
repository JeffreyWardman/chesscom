from typing import List

import pycountry
import requests

from ._country import CountryDetails

BASE_COUNTRY_URL = "https://api.chess.com/pub/country"

AVAILABLE_COUNTRIES = [
    {"name": x.name, "code": x.alpha_2} for x in list(pycountry.countries)
] + [
    {"name": "Canary Islands", "code": "XA"},
    {"name": "Basque Country", "code": "XB"},
    {"name": "Catalonia", "code": "XC"},
    {"name": "England", "code": "XE"},
    {"name": "Galicia", "code": "XG"},
    {"name": "Kosovo", "code": "XK"},
    {"name": "Palestine", "code": "XP"},
    {"name": "Scotland", "code": "XS"},
    {"name": "Wales", "code": "XW"},
    {"name": "International", "code": "XX"},
]


class Country:
    """Country API wrapper."""

    @staticmethod
    def details(country_alpha_2: str) -> CountryDetails:
        """Get country details.

        Args:
            country_alpha_2 (str): Country alpha-2 code.

        Returns:
            CountryDetails: Country details class.
        """
        assert len(country_alpha_2) == 2
        api_url = f"{BASE_COUNTRY_URL}/{country_alpha_2}"
        response = requests.get(api_url).json()
        response["id"] = response.pop("@id")
        return CountryDetails(**response)

    @staticmethod
    def players(country_alpha_2: str) -> List[str]:
        """Get list of players from country.

        Note: Endpoint refreshes at most every 12 hours.

        Args:
            country_alpha_2 (str): Country alpha-2 code.

        Returns:
            List[str]: List of players from country.
        """
        assert len(country_alpha_2) == 2
        api_url = f"{BASE_COUNTRY_URL}/{country_alpha_2}/players"
        response = requests.get(api_url).json()
        return response["players"]

    @staticmethod
    def clubs(country_alpha_2: str) -> List[str]:
        """Get list of clubs from country.

        Note: Endpoint refreshes at most every 12 hours.

        Args:
            country_alpha_2 (str): Country alpha-2 code.

        Returns:
            List[str]: List of clubs from country.
        """
        assert len(country_alpha_2) == 2
        api_url = f"{BASE_COUNTRY_URL}/{country_alpha_2}/clubs"
        response = requests.get(api_url).json()
        return response["clubs"]
