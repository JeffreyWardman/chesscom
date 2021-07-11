from enum import Enum
from typing import Any, Dict, List

from pydantic import BaseModel

from ._match import MatchResults
from ._tournaments import TournamentResults, TournamentsSummary


class PlayerAccountStatus(Enum):
    closed = "closed"
    fair_play_violations = "closed:fair_play_violations"
    basic = "basic"
    premium = "premium"
    mod = "mod"
    staff = "staff"


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


class ClubDetails(BaseModel):
    """Details about club and user's club activity.

    Args:
        id (str): URL of Club endpoint.
        name (str): Club's name.
        last_activity (int): timestamp of last activity.
        icon (str): Club's icon URL.
        url (str): Club's URL.
        joined (int): Timestamp of when player has joined the club.
    """

    id: str
    name: str
    last_activity: int
    icon: str
    url: str
    joined: int


class PlayerProfile(BaseModel):
    """Player profile.

    Args:
        id (str): Location of this profile (always self-referencing).
        url (str): Chess.com user's profile page (the username is displayed with the original letter case).
        username (str): The username of this player.
        player_id (int): The non-changing Chess.com ID of this player.
        title (str, optional): Abbreviation of chess title.
        status (str): Account status.
        name (str, optional): The personal first and last name.
        avatar (str, optional): URL of a 200x200 image.
        location (str, optional): The city or location of player.
        country (str, optional): API location of this player's country's profile.
        joined (int): Timestamp of registration on Chess.com.
        last_online (int): Timestamp of the most recent login.
        followers (int): Number of players tracking this player's activity.
        is_streamer (bool): If the member is a Chess.com streamer.
        twitch_url (str, optional): Twitch.tv URL.
        fide (int, optional): FIDE rating.
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


class CurrentDailyChess(BaseModel):
    """Current daily chess game details.

    Args:
        white (str): URL of the white player's profile.
        black (str): URL of the black player's profile.
        url (str): URL of this game.
        fen (str): Current FEN.
        pgn (str): Current PGN.
        turn (str): Player to move.
        move_by (int): Timestamp of when the next move must be made. this is "0" if the player-to-move is on vacation.
        draw_offer (str, optional): Player who has made a draw offer.
        last_activity (int): Timestamp of the last activity on the game.
        start_time (int): Timestamp of the game start (Daily Chess only).
        time_control (str): PGN-compliant time control.
        time_class (str): Time-per-move grouping, used for ratings.
        rules (str): Game variant information.
        tournament (str, optional): URL pointing to tournament.
        match (str, optional): URL pointing to team match.
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
    """Daily chess game details for game where it's user's turn to move.

    Args:
        url (str): URL of this game.
        move_by (int): Timestamp of the when the move must be made by. this is "0" if it is not this player's turn.
        draw_offer (bool, optional): This player has received a draw offer.
        last_activity (int): Timestamp of the last activity on the game.
    """

    url: str
    move_by: int
    draw_offer: bool = None
    last_activity: int


class Player(BaseModel):
    """Player information for a game.

    Args:
        username (str): Username.
        rating (int): Player's rating at the start of the game.
        result (str): Game result.
        id (str): URL of this player's profile.
    """

    username: str
    rating: int
    result: str
    id: str


class MonthlyArchive(BaseModel):
    """Monthly archived game details.

    Args:
        white (Dict[str, Any]): Details of the white-piece player.
        black (Dict[str, Any]): Details of the black-piece player.
        url (str): URL of this game.
        fen (str): Final FEN.
        pgn (str): Final PGN.
        start_time (int, optional): Timestamp of the game start (Daily Chess only).
        end_time (int): Timestamp of the game end.
        time_control (str): PGN-compliant time control.
        rules (str): Game variant information.
        eco (str, optional): URL pointing to ECO opening.
        tournament (str, optional): URL pointing to tournament.
        match (str, optional): URL pointing to team match.
        time_class (str): Time class.
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
    """Rating log for amount and date first achieved.

    Args:
        rating (int): Rating.
        date (int): Timestamp rating was (first) achieved.
    """

    rating: int
    date: int


class LastRating(BaseModel):
    """Current player rating, date achieved and Glicko RD value.

    Args:
        date (int): Timestamp of the last rated game finished.
        rating (int): Most-recent rating.
        rd (int): Glicko "RD" value used to calculate ratings changes.
    """

    date: int
    rating: int
    rd: int


class BestRating(BaseModel):
    """Best player rating, URL to game and date achieved.

    Args:
        date (int): Timestamp of the best-win game.
        rating (int): Highest rating achieved.
        game (str): URL of the best-win game.
    """

    date: int
    rating: int
    game: str


class GamesRecord(BaseModel):
    """Summary of all games played.

    Args:
        win (int): Number of games won.
        loss (int): Number of games lost.
        draw (int): Number of games drawn.
        time_per_move (int, optional): Integer number of seconds per average move.
        timeout_percent (float, optional): Timeout percentage in the last 90 days.
    """

    win: int
    loss: int
    draw: int
    time_per_move: int = None
    timeout_percent: float = None


class PlayerMatches(BaseModel):
    """Player matches separated by status (registered, in progress, finished).

    Args:
        finished (List[Dict[str, Any]]): Details on finished matches.
        in_progress (List[Dict[str, Any]]): Details on matches in progress.
        registered (List[Dict[str, Any]]): Details on registered matches.
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
                matches.append(MatchResults(**match))
            setattr(self, match_type, matches)


class ChessModeStats(BaseModel):
    """Basic statistics for player for a chess mode.

    Args:
        last (Dict[str, int]): Current stats.
        best (Dict[str, Any]): Best rating achieved by a win.
        record (Dict[str, int]): Summary of all games played.
        tournament (Dict[str, Any], optional): Summary of tournaments participated in.
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


class ChessModeRatings(BaseModel):
    """Player rating information for a chess mode.

    Args:
        highest (Dict[str, int], optional): Highest rating and date for game mode.
        lowest (Dict[str, int], optional): Lowest rating and date for game mode.
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
    """List of matches in tournaments for player based on progress status.

    Args:
        finished (List[Dict[str, Any]]): List of finished matches in tournaments.
        in_progress (List[Dict[str, Any]]): List of in progress matches in tournaments.
        registered (List[Dict[str, Any]]): List of registered matches in tournaments.
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
