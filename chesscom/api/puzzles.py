import requests

from ._puzzles import PuzzleDetails

BASE_PUZZLE_URL = "https://api.chess.com/pub/puzzle"


class Puzzles:
    """Puzzles API wrapper."""

    @staticmethod
    def daily() -> PuzzleDetails:
        """Get daily puzzle.

        Returns:
            PuzzleDetails: Puzzle details class.
        """
        response = requests.get(BASE_PUZZLE_URL).json()
        return PuzzleDetails(**response)

    @staticmethod
    def random() -> PuzzleDetails:
        """Get random puzzle.

        Returns:
            PuzzleDetails: Puzzle details class.
        """
        api_url = f"{BASE_PUZZLE_URL}/random"
        response = requests.get(api_url).json()
        return PuzzleDetails(**response)
