from typing import Any, Dict, List, Union

from pydantic import BaseModel


class Player(BaseModel):
    """
    username: username
    board: url of board
    rating: rating of player
    rd: Glicko RD
    timeout_percent: timeout percentage in the last 90 days
    status: status of user
    stats: url to player's stats
    played_as_white: result {win, lose, resign, etc.} of player when played as white (if game's finished)
    played_as_black: result {win, lose, resign, etc.} of player when played as black (if game's finished)
    """

    username: str
    board: str
    rating: int = None
    rd: float = None
    timeout_percent: float = None
    status: str
    stats: str = None
    played_as_white: str = None
    played_as_black: str = None


class MatchBoardPlayer(BaseModel):
    """
    username: the username
    rating: the player's rating at the start of the game
    result: game result, if game's finished
    id: URL of this player's profile
    team: url to club's profile
    """

    username: str
    rating: int
    result: str = None
    id: str
    team: str = None


class MatchSettings(BaseModel):
    """
    time_class: time class (daily)
    time_control: time control
    initial_setup: initial match setup
    rules: game variant information (e.g., "chess960")
    min_team_players: minimum number of players per team
    max_team_players: maximum number of players per team
    min_required_games: minimum number of required games
    min_rating: minimum rating of players to be admitted in this match
    max_rating: maximum rating of players to be admitted in this match
    autostart: if the match is set to automatically start
    """

    time_class: str
    time_control: str
    initial_setup: str = None
    rules: str
    min_team_players: int = 0
    max_team_players: int = 0
    min_required_games: int = 0
    min_rating: int = None
    max_rating: int = None
    autostart: bool = False


class MatchTeamDetails(BaseModel):
    """
    id: API URL for the club profile
    url: Web URL for the club profile
    name: club name
    score Team score (adjuested in case of fair play recalculations)
    """

    id: str
    url: str = None
    name: str
    score: int
    players: List[Dict[str, Union[str, int, float]]]
    fair_play_removals: List[str] = None

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        self.players = [Player(**x) for x in self.players]


class MatchTeams(BaseModel):
    team1: Dict[str, Any]
    team2: Dict[str, Any]
    fair_play_removals: List[str] = None

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        self.team1["id"] = self.team1.pop("@id")
        self.team2["id"] = self.team2.pop("@id")

        self.team1 = MatchTeamDetails(**self.team1)
        self.team2 = MatchTeamDetails(**self.team2)


class MatchDetails(BaseModel):
    """
    name: match name
    url: the URL of the match on the website
    description: match description
    start_time: manual or auto time start
    settings: match settings
    status: whether match has been registered/in progress/finished
    boards: number of boards
    teams: information about team1 and team2
    """

    name: str
    url: str
    description: str = None
    start_time: int
    settings: Dict[str, Union[str, int]]
    status: str
    boards: int
    teams: Dict[str, Dict[str, Any]]

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        self.settings = MatchSettings(**self.settings)
        self.teams = MatchTeams(**self.teams)


class MatchBoardScore(BaseModel):
    """
    player1: User score (adjusted in case of fair play recalculations)
    player2: User score (adjusted in case of fair play recalculations)
    """

    player1: float
    player2: float


class MatchResult(BaseModel):
    """
    played_as_white: Result when playing as white
    played_as_black: Result when playing as black
    """

    played_as_white: str
    played_as_black: str


class MatchBoardGame(BaseModel):
    """
    white: details of the white-piece player
    black: details of the black-piece player
    url: URL of this game
    fen: current FEN
    pgn: final PGN, if game's finished
    start_time: timestamp of the game start (Daily Chess only)
    end_time: timestamp of the game end, if game's finished
    time_control: PGN-compliant time control
    time_class: time-per-move grouping, used for ratings
    rules: game variant information (e.g., "chess960")
    eco: URL pointing to ECO opening (if available)
    match: URL pointing to team match (if available)
    rated: whether game is rated
    """

    white: Dict[str, Union[str, int]]
    black: Dict[str, Union[str, int]]
    url: str
    fen: str
    pgn: str = None
    start_time: int = None
    end_time: int = None
    time_control: str
    time_class: str
    rules: str
    eco: str = None
    match: str = None
    rated: bool = None

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        self.white["id"] = self.white.pop("@id")
        self.black["id"] = self.black.pop("@id")

        self.white = MatchBoardPlayer(**self.white)
        self.black = MatchBoardPlayer(**self.black)


class MatchBoardDetails(BaseModel):
    """
    board_scores: board scores
    games: games
    """

    board_scores: Dict[str, float]
    games: List[Dict[str, Any]]

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        self.board_scores = {
            f"player{i + 1}": val for i, val in enumerate(self.board_scores.values())
        }
        self.board_scores = MatchBoardScore(**self.board_scores)
        self.games = [MatchBoardGame(**x) for x in self.games]


class LiveMatchDetails(BaseModel):
    """
    id: live match id
    name: match name
    url: match url
    start_time: timestamp of match start
    status: match status
    boards: number of boards in match
    settings: match settings
    teams: match teams
    """

    id: str
    name: str
    url: str
    start_time: int
    end_time: int = None
    status: str
    boards: int
    settings: Dict[str, Union[str, int, bool]]
    teams: Dict[str, Dict[str, Any]]

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        self.settings = MatchSettings(**self.settings)
        self.teams = MatchTeams(**self.teams)


class MatchResults(BaseModel):
    """
    name: Name of match
    url: URL of match on web site
    id: URL of PubAPI match endpoint
    club: URL of player's club endpoint
    results: List of results of game played as white and black respectively
    board: URL of PubAPI match board endpoint
    """

    name: str
    url: str
    id: str
    club: str
    results: Dict[str, str] = None
    board: str = None

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        if self.results is not None:
            self.results = MatchResult(**self.results)
