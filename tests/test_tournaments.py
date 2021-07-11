from chesscom.api.tournaments import Tournament


class TestTournament:
    @staticmethod
    def test_get(tournament_id):
        Tournament.get(tournament_id)

    @staticmethod
    def test_get_round(tournament_id, tournament_round):
        Tournament.get_round(tournament_id, tournament_round)

    @staticmethod
    def test_get_round_group(tournament_id, tournament_round, tournament_group):
        Tournament.get_round_group(tournament_id, tournament_round, tournament_group)
