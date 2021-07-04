import requests

from ._puzzles import PuzzleDetails

BASE_PUZZLE_URL = "https://api.chess.com/pub/puzzle"


class Puzzles:
    @staticmethod
    def daily() -> PuzzleDetails:
        response = requests.get(BASE_PUZZLE_URL).json()
        return PuzzleDetails(**response)

    @staticmethod
    def random() -> PuzzleDetails:
        api_url = f"{BASE_PUZZLE_URL}/random"
        response = requests.get(api_url).json()
        return PuzzleDetails(**response)
