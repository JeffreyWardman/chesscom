from chesscom.api.leaderboards import Leaderboards


class TestLeaderboards:
    @staticmethod
    def test_get_all():
        Leaderboards.get_all()
