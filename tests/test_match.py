from chesscom.api.match import Match


class TestMatch:
    @staticmethod
    def test_daily_team_matches(match_id):
        Match.daily_team_matches(match_id)

    @staticmethod
    def test_team_match_board(match_id, board):
        Match.team_match_board(match_id, board)

    @staticmethod
    def test_get_live_match(live_match_id):
        Match.live_match(live_match_id)

    @staticmethod
    def test_live_match_board(live_match_id, board):
        Match.live_match_board(live_match_id, board)
