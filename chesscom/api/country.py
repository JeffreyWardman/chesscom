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
    @staticmethod
    def details(country_alpha_2: str) -> CountryDetails:
        assert len(country_alpha_2) == 2
        api_url = f"{BASE_COUNTRY_URL}/{country_alpha_2}"
        response = requests.get(api_url).json()
        response["id"] = response.pop("@id")
        return CountryDetails(**response)

    @staticmethod
    def players(country_alpha_2: str) -> List[str]:
        """Note: Endpoint refreshes at most every 12 hours"""
        assert len(country_alpha_2) == 2
        api_url = f"{BASE_COUNTRY_URL}/{country_alpha_2}/players"
        response = requests.get(api_url).json()
        return response["players"]

    @staticmethod
    def clubs(country_alpha_2: str) -> List[str]:
        """Note: Endpoint refreshes at most every 12 hours"""
        assert len(country_alpha_2) == 2
        api_url = f"{BASE_COUNTRY_URL}/{country_alpha_2}/clubs"
        response = requests.get(api_url).json()
        return response["clubs"]
