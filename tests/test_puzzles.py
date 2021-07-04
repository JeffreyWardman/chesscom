from chesscom.api.puzzles import Puzzles


class TestPuzzles:
    @staticmethod
    def test_daily():
        Puzzles.daily()

    @staticmethod
    def test_random():
        Puzzles.random()
