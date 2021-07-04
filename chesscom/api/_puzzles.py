from pydantic.main import BaseModel


class PuzzleDetails(BaseModel):
    """
    title: the title of the daily puzzle
    url: url to daily puzzle in chess.com
    publish_time: the date of the published puzzle
    fen: the FEN of the published puzzle
    pgn: the PGN of the published puzzle
    image: the link to the image
    """

    title: str
    url: str
    publish_time: int
    fen: str
    pgn: str
    image: str
