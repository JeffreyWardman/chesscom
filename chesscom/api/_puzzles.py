from pydantic.main import BaseModel


class PuzzleDetails(BaseModel):
    """Puzzle details.

    Args:
        title (str): Title of the daily puzzle.
        url (str): URL to daily puzzle in Chess.com.
        publish_time (int): Date of the published puzzle.
        fen (str): FEN of the published puzzle.
        pgn (str): PGN of the published puzzle.
        image (str): link to the image.
    """

    title: str
    url: str
    publish_time: int
    fen: str
    pgn: str
    image: str
