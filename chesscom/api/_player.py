from enum import Enum
from typing import Any, Dict, List

from pydantic import BaseModel

from ._match import MatchResults
from ._tournaments import TournamentResults, TournamentsSummary


class ClubDetails(BaseModel):
    """
    id: URL of Club endpoint
    name: Club's name
    last_activity: timestamp of last activity
    icon: Club's icon url
    url: Club's url
    joined: Timestamp of when player has joined the Club
    """

    id: str
    name: str
    last_activity: int
    icon: str
    url: str
    joined: int


class PlayerProfile(BaseModel):
    """
    id: the location of this profile (always self-referencing)
    url: the chess.com user's profile page (the username is displayed with the original letter case)
    username: the username of this player
    player_id: the non-changing Chess.com ID of this player
    title: (optional) abbreviation of chess title, if any
    status: account status: closed, closed:fair_play_violations, basic, premium, mod, staff
    name: (optional) the personal first and last name
    avatar: (optional) URL of a 200x200 image
    location: (optional) the city or location
    country: API location of this player's country's profile
    joined: timestamp of registration on Chess.com
    last_online: timestamp of the most recent login
    followers: the number of players tracking this player's activity
    is_streamer: if the member is a Chess.com streamer
    twitch_url: Twitch.tv URL
    fide: FIDE rating
    """

    id: str
    url: str
    username: str
    player_id: int
    title: str = None
    status: str
    name: str = None
    avatar: str = None
    location: str = None
    country: str = None
    joined: int
    last_online: int
    followers: int
    is_streamer: bool
    twitch_url: str = None
    fide: int = None


class GameResults(Enum):
    win = "Win"
    checkmated = "Checkmated"
    agreed = "Draw agreed"
    repetition = "Draw by repetition"
    timeout = "Timeout"
    resigned = "Resigned"
    stalemate = "Stalemate"
    lose = "Lose"
    insufficient = "Insufficient material"
    fifty_move = "Draw by 50-move rule"
    abandoned = "Abandoned"
    kingofthehill = "Opponent king reached the hill"
    threecheck = "Checked for the 3rd time"
    timevsinsufficient = "Draw by timeout vs insufficient material"
    bughousepartnerlose = "Bughouse partner lost"


class CurrentDailyChess(BaseModel):
    """
    white: URL of the white player's profile
    black: URL of the black player's profile
    url: URL of this game
    fen: current FEN
    pgn: current PGN
    turn: player to move
    move_by: timestamp of when the next move must be made. this is "0" if the player-to-move is on vacation
    draw_offer: (optional) player who has made a draw offer
    last_activity: timestamp of the last activity on the game
    start_time: timestamp of the game start (Daily Chess only)
    time_control: PGN-compliant time control
    time_class: time-per-move grouping, used for ratings
    rules: game variant information (e.g., "chess960")
    tournament: URL pointing to tournament (if available),
    match: URL pointing to team match (if available)
    """

    white: str
    black: str
    url: str
    fen: str
    pgn: str
    turn: str
    move_by: int
    draw_offer: str = None
    last_activity: int
    start_time: int
    time_control: str
    time_class: str
    rules: str
    tournament: str = None
    match: str = None


class ToMoveDailyChess(BaseModel):
    """
    url: URL of this game
    move_by: timestamp of the when the move must be made by. this is "0" if it is not this player's turn
    draw_offer: (optional) this player has received a draw offer
    last_activity: timestamp of the last activity on the game
    """

    url: str
    move_by: int
    draw_offer: bool = None
    last_activity: int


class Player(BaseModel):
    """
    username: the username
    rating: the player's rating at the start of the game
    result: game result
    id:  URL of this player's profile
    """

    username: str
    rating: int
    result: str
    id: str


class MonthlyArchive(BaseModel):
    """
    white: details of the white-piece player
    black: details of the black-piece player
    url: URL of this game
    fen: final FEN
    pgn: final PGN
    start_time: timestamp of the game start (Daily Chess only)
    end_time: timestamp of the game end
    time_control: PGN-compliant time control
    rules: game variant information (e.g., "chess960")
    eco: URL pointing to ECO opening (if available),
    tournament: URL pointing to tournament (if available),
    match: URL pointing to team match (if available)
    """

    white: Dict[str, Any]
    black: Dict[str, Any]
    url: str
    fen: str
    pgn: str
    start_time: int = None
    end_time: int
    time_control: str
    rules: str
    eco: str = None
    tournament: str = None
    match: str = None
    time_class: str

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        self.white["id"] = self.white.pop("@id")
        self.black["id"] = self.black.pop("@id")

        self.white = Player(**self.white)
        self.black = Player(**self.black)


class RatingLog(BaseModel):
    """
    rating: rating
    date: timestamp rating was (first) achieved
    """

    rating: int
    date: int


class LastRating(BaseModel):
    """The current stats.

    date: timestamp of the last rated game finished
    rating: most-recent rating
    rd: the Glicko "RD" value used to calculate ratings changes
    """

    date: int
    rating: int
    rd: int


class BestRating(BaseModel):
    """The best rating achieved by a win.

    date: timestamp of the best-win game
    rating: highest rating achieved
    game: URL of the best-win game
    """

    date: int
    rating: int
    game: str


class GamesRecord(BaseModel):
    """Summary of all games played.

    win: number of games won
    loss: number of games lost
    draw: number of games drawn
    time_per_move: integer number of seconds per average move
    timeout_percent: timeout percentage in the last 90 days
    """

    win: int
    loss: int
    draw: int
    time_per_move: int = None
    timeout_percent: float = None


class PlayerMatches(BaseModel):
    finished: List[Dict[str, Any]]
    in_progress: List[Dict[str, Any]]
    registered: List[Dict[str, Any]]

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        for match_type in ("finished", "in_progress", "registered"):
            matches = []
            for match in getattr(self, match_type):
                match["id"] = match.pop("@id")
                matches.append(MatchResults(**match))
            setattr(self, match_type, matches)


class ChessMode(BaseModel):
    """
    last: the current stats
    best: the best rating achieved by a win
    record: summary of all games played
    tournament: summary of tournaments participated in
    """

    last: Dict[str, int]
    best: Dict[str, Any]
    record: Dict[str, int]
    tournament: Dict[str, Any] = None

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        self.last = LastRating(**self.last)
        self.best = BestRating(**self.best)
        self.record = GamesRecord(**self.record)
        if self.tournament is not None:
            self.tournament = TournamentsSummary(**self.tournament)


class GameMode(BaseModel):
    """
    highest: highest rating and date for game mode
    lowest: lowest rating and date for game mode
    """

    highest: Dict[str, int] = None
    lowest: Dict[str, int] = None

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        if self.highest is not None:
            self.highest = RatingLog(**self.highest)
        if self.lowest is not None:
            self.lowest = RatingLog(**self.lowest)


class PlayerTournaments(BaseModel):
    """
    finished: List of finished matches in tournaments
    in_progress: List of in progress matches in tournaments
    registered: List of registered matches in tournaments
    """

    finished: List[Dict[str, Any]]
    in_progress: List[Dict[str, Any]]
    registered: List[Dict[str, Any]]

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        for match_type in ("finished", "in_progress", "registered"):
            matches = []
            for match in getattr(self, match_type):
                match["id"] = match.pop("@id")
                matches.append(TournamentResults(**match))
            setattr(self, match_type, matches)
