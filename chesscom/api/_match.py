from typing import Any, Dict, List, Union

from pydantic import BaseModel


class Player(BaseModel):
    """Player information in match.

    Args:
        username (str): Username.
        board (str): URL of board.
        rating (int, optional): Rating of player.
        rd (float, optional): Glicko RD.
        timeout_percent (float, optional): Timeout percentage in the last 90 days.
        status (str): Status of user.
        stats (str, optional): URL to player's stats.
        played_as_white (str, optional): Result {win, lose, resign, etc.} of player when played as white (if game's finished).
        played_as_black (str, optional): Result {win, lose, resign, etc.} of player when played as black (if game's finished).
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
    """Player result in club match.

    Args:
        username (str): Username.
        rating (int): The player's rating at the start of the game.
        result (str, optional): Game result, if game's finished.
        id (str): URL of this player's profile.
        team (str, optional): URL to club's profile.
    """

    username: str
    rating: int
    result: str = None
    id: str
    team: str = None


class MatchSettings(BaseModel):
    """Match settings.

    Args:
        time_class (str): time class.
        time_control (str): time control.
        initial_setup (str, optional): initial match setup.
        rules (str): game variant information (e.g., "chess960").
        min_team_players (int): minimum number of players per team. Defaults to 0.
        max_team_players (int): maximum number of players per team. Defaults to 0.
        min_required_games (int): minimum number of required games. Defaults to 0.
        min_rating (int, optional): minimum rating of players to be admitted in this match.
        max_rating (int, optional): maximum rating of players to be admitted in this match.
        autostart (bool): if the match is set to automatically start. Defaults to False.
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

    Args:
        id (str): API URL for the club profile.
        url (str, optional): Web URL for the club profile.
        name (str): club name.
        score (int): Team score (adjuested in case of fair play recalculations).
        players (List[Dict[str, Union[str, int, float]]]): List of players in team.
        fair_play_removals (List[str], optional): List of fair play removals.
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
    """Teams in match.

    Args:
        team1 (Dict[str, Any]): Team 1.
        team2 (Dict[str, Any]): Team 2.
        fair_play_removals (List[str], optional): List of fair play removals during match.

    """

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
    """Match details.

    Args:
        name (str): match name.
        url (str): the URL of the match on the website.
        description (str, optional): match description.
        start_time (int): manual or auto time start.
        settings (Dict[str, Union[str, int]]): match settings.
        status (str): whether match has been registered/in progress/finished.
        boards (int): number of boards.
        teams (Dict[str, Dict[str, Any]]): information about team1 and team2.
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
    """Match board score for players.

    Args:
        player1 (float): User score (adjusted in case of fair play recalculations).
        player2 (float): User score (adjusted in case of fair play recalculations).
    """

    player1: float
    player2: float


class MatchResult(BaseModel):
    """Match result.

    May be missing if game/s are incomplete.

    Args:
        played_as_white (str, optional): Result when playing as white.
        played_as_black (str. optional): Result when playing as black.
    """

    played_as_white: str = None
    played_as_black: str = None


class MatchBoardGame(BaseModel):
    """Game details on board in match.

    Args:
        white (Dict[str, Union[str, int]]): Details of the white-piece player.
        black (Dict[str, Union[str, int]]): Details of the black-piece player.
        url (str): URL of this game.
        fen (str): Current FEN.
        pgn (str, optional): Final PGN, if game's finished.
        start_time (int, optional): Timestamp of the game start (Daily Chess only).
        end_time (int, optional): Timestamp of the game end, if game's finished.
        time_control (str): PGN-compliant time control.
        time_class (str): Time-per-move grouping, used for ratings.
        rules (str): Game variant information (e.g., "chess960")
        eco (str, optional): URL pointing to ECO opening.
        match (str, optional): URL pointing to team match.
        rated (bool, optional): Whether game is rated.
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
    """Match board details.

    Args:
        board_scores (Dict[str, float]): Board scores.
        games (List[Dict[str, Any]]): Games.
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
    """Live match details.

    Args:
        id (str): Live match ID.
        name (str): Match name.
        url (str): Match URL.
        start_time (int): Timestamp of match start.
        end_time (int, optional): Timestamp of match end.
        status (str): Match status.
        boards (int): Number of boards in match.
        settings (Dict[str, Union[str, int, bool]]): Match settings.
        teams (Dict[str, Dict[str, Any]]): Match teams.
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
    """Match results.

    Args:
        name (str): Name of match.
        url (str): URL of match on web site.
        id (str): URL of PubAPI match endpoint.
        club (str): URL of player's club endpoint.
        results (Dict[str, str], optional): List of results of game played as white and black respectively.
        board (str, optional): URL of PubAPI match board endpoint.
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
