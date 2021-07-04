from typing import Any, Dict, List, Union

from pydantic import BaseModel


class TournamentSettings(BaseModel):
    """
    type: tournament type
    rules: tournament rules
    time_class: tournament time class
    time_control: tournament time control
    is_rated: whether tournament is rated
    is_official: whether tournament is official
    is_invite_only: whether tournament is invite only
    initial_group_size: initial tournament group size
    user_advance_count: number of users who advance to the next round
    use_tiebreak: whether tiebreak is used
    allow_vacation: whether users can be on vacation and not forfeit
    winner_places: winner placements
    registered_user_count: number of registered users
    games:per_opponent: number of games played against each opponent
    total_rounds: number of rounds
    concurrent_games_per_opponent: Number of concurrent games allowed per opponent
    """

    type: str
    rules: str
    time_class: str
    time_control: str
    is_rated: bool
    is_official: bool
    is_invite_only: bool
    initial_group_size: int
    user_advance_count: int
    use_tiebreak: bool
    allow_vacation: bool
    winner_places: int
    registered_user_count: int
    games_per_opponent: int
    total_rounds: int
    concurrent_games_per_opponent: int


class TournamentPlayerStatus(BaseModel):
    """
    username: username
    status: status of user
    """

    username: str
    status: str


class TournamentDetails(BaseModel):
    """
    name: name
    url: url to Web tournament's URL
    description: description
    creator: username of creator
    status: status of tournament {finished, in_progress, registration}
    finish_time: timestamp of finish time, if tournament is finished
    settings: tournament settings
    players: List of tournament's players and their status
    rounds: List of tournament's rounds URL
    """

    name: str
    url: str
    description: str
    creator: str
    status: str
    finish_time: int
    settings: Dict[str, Any]
    players: List[Dict[str, str]]
    rounds: List[str]

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        self.settings = TournamentSettings(**self.settings)
        self.players = [TournamentPlayerStatus(**x) for x in self.players]


class TournamentRoundPlayerAdvancement(BaseModel):
    """
    username: username
    is_advancing: only if this tournament is completed
    """

    username: str
    is_advancing: bool = None


class TournamentRoundDetails(BaseModel):
    """
    groups: List of tournament's round groups (URLs)
    players: List of tournament's round players
    """

    groups: List[str]
    players: List[Dict[str, Union[str, bool]]]

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        self.players = [TournamentRoundPlayerAdvancement(**x) for x in self.players]


class TournamentRoundGroupPlayer(BaseModel):
    """
    rating: player rating before game
    result: game result
    id: player URL
    username: username
    """

    rating: int
    result: str
    id: str
    username: str


class TournamentRoundGroupGames(BaseModel):
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
    eco: URL pointing to ECO opening (if available)
    tournament: URL pointing to tournament (if available),
    """

    white: Dict[str, Union[str, int]]
    black: Dict[str, Union[str, int]]
    url: str
    fen: str
    pgn: str
    turn: str = None
    move_by: int = None
    draw_offer: str = None
    last_activity: int = None
    start_time: int
    time_control: str
    time_class: str
    rules: str
    eco: str = None
    tournament: str = None

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        self.white["id"] = self.white.pop("@id")
        self.black["id"] = self.black.pop("@id")

        self.white = TournamentRoundGroupPlayer(**self.white)
        self.black = TournamentRoundGroupPlayer(**self.black)


class TournamentRoundGroupPlayer(BaseModel):
    """
    username: username
    points: points earned by player in this group adjuested in case of fair play recalculations)
    tie_break: tie-break points by player earned in this group
    is_advancing: {true, false}
    """

    username: str
    points: str = "0"
    tie_break: str = "0"
    is_advancing: bool = False

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        self.points = float(self.points)
        self.tie_break = float(self.tie_break)


class TournamentRoundGroupDetails(BaseModel):
    fair_play_removals: List[str]
    games: List[Dict[str, Any]]
    players: List[Dict[str, Union[str, int, bool]]]

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        self.games = [TournamentRoundGroupGames(**x) for x in self.games]
        self.players = [TournamentRoundGroupPlayer(**x) for x in self.players]


class TournamentResults(BaseModel):
    """
    url: link to the PubAPI URL of the tournament
    id: link to the Web URL of the tournament
    wins: number of wins
    losses: number of losses
    draws: number of draws
    points_awarded: points_awarded
    placement: placement
    status: final status of the player in this tourmanent {winner, eliminated, withdrew, removed}
    """

    url: str
    id: str
    status: str
    wins: int
    losses: int
    draws: int
    points_awarded: int = None
    placement: int = None
    total_players: int


class TournamentStatus(BaseModel):
    """
    url: link to the PubAPI URL of the tournament
    id: link to the Web URL of the tournament
    status: final status of the player in this tourmanent {winner, eliminated, withdrew, removed}
    """

    url: str
    id: str
    status: str


class TournamentsSummary(BaseModel):
    """Summary of tournaments participated in.

    count: number of tournaments joined
    withdraw: number of tournaments withdrawn from
    points: total number of points earned in tournaments
    highest_finish: best tournament place
    """

    count: int
    withdraw: int
    points: int
    highest_finish: int
