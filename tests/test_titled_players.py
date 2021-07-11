from chesscom.api.titled_players import VALID_TITLES, TitledPlayers


class TestTitledPlayers:
    @staticmethod
    def test_usernames():
        TitledPlayers.usernames(VALID_TITLES)
