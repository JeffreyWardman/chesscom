from chesscom.api.player import Player


class TestPlayer:
    @staticmethod
    def test_profile(username):
        Player.profile(username)

    @staticmethod
    def test_clubs(username):
        Player.clubs(username)

    @staticmethod
    def test_tournaments(username):
        Player.tournaments(username)

    @staticmethod
    def test_matches(username):
        Player.matches(username)

    @staticmethod
    def test_online_status(username):
        Player.online_status(username)

    @staticmethod
    def test_stats(username):
        Player.stats(username)

    @staticmethod
    def test_current_daily_chess_games(username):
        Player.current_daily_chess_games(username)

    @staticmethod
    def test_to_move_daily_chess_games(username):
        Player.to_move_daily_chess_games(username)

    @staticmethod
    def test_monthly_archive_urls(username):
        Player.monthly_archive_urls(username)

    @staticmethod
    def test_monthly_archive(username, month, year):
        Player.monthly_archive(username, year=year, month=month)

    @staticmethod
    def test_monthly_pgns(username, month, year):
        Player.monthly_pgns(username, year=year, month=month)
