from chesscom.api.country import Country


class TestCountry:
    @staticmethod
    def test_details(country_alpha_2):
        Country.details(country_alpha_2)

    @staticmethod
    def test_players(country_alpha_2):
        Country.players(country_alpha_2)

    @staticmethod
    def test_clubs(country_alpha_2):
        Country.clubs(country_alpha_2)
