from typing import Any, Dict, List, Union

from pydantic import BaseModel


class TournamentSettings(BaseModel):
    """Tournament settings.

    Args:
        type (str): Tournament type.
        rules (str): Tournament rules.
        time_class (str): Tournament time class.
        time_control (str): Tournament time control.
        is_rated (bool): Whether tournament is rated.
        is_official (bool): Whether tournament is official.
        is_invite_only (bool): Whether tournament is invite only.
        initial_group_size (int): Initial tournament group size.
        user_advance_count (int): Number of users who advance to the next round.
        use_tiebreak (bool): Whether tiebreak is used.
        allow_vacation (bool): Whether users can be on vacation and not forfeit.
        winner_places (int): Winner placements.
        registered_user_count (int): Number of registered users.
        games:per_opponent (int): Number of games played against each opponent.
        total_rounds (int): Number of rounds.
        concurrent_games_per_opponent (int): Number of concurrent games allowed per opponent.
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
    """Tournament player status.

    Args:
        username (str): Username.
        status (str): Status of user.
    """

    username: str
    status: str


class TournamentDetails(BaseModel):
    """Tournament details.

    Args:
        name (str): Name.
        url (str): URL to Web tournament's URL.
        description (str): Description.
        creator (str): Username of creator.
        status (str): Status of tournament {finished, in_progress, registration}.
        finish_time (int): Timestamp of finish time, if tournament is finished.
        settings (Dict[str, Any]): Tournament settings.
        players (List[Dict[str, str]]): List of tournament's players and their status.
        rounds (List[str]): List of tournament's rounds URL.
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
    """Information on whether player advances from tournament round.

    Args:
        username (str): Username.
        is_advancing (bool, optional): Only if this tournament is completed.
    """

    username: str
    is_advancing: bool = None


class TournamentRoundDetails(BaseModel):
    """Tournament round groups and players.

    Args:
        groups (List[str]): List of tournament's round groups (URLs).
        players (List[Dict[str, Union[str, bool]]]): List of tournament's round players.
    """

    groups: List[str]
    players: List[Dict[str, Union[str, bool]]]

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        self.players = [TournamentRoundPlayerAdvancement(**x) for x in self.players]


class TournamentRoundGroupPlayer(BaseModel):
    """Information on player in tournament round's group.

    Args:
        rating (int): Player rating before game.
        result (str): Game result.
        id (str): Player URL.
        username (str): Username.
    """

    rating: int
    result: str
    id: str
    username: str


class TournamentRoundGroupGames(BaseModel):
    """Information on tournament round group games.

    Args:
        white (Dict[str, Union[str, int]]): URL of the white player's profile.
        black (Dict[str, Union[str, int]]): URL of the black player's profile.
        url (str): URL of this game.
        fen (str): current FEN.
        pgn (str): Current PGN.
        turn (str, optional): Player to move.
        move_by (int, optional): Timestamp of when the next move must be made. this is "0" if the player-to-move is on vacation.
        draw_offer (str, optional): player who has made a draw offer.
        last_activity (int, optional): Timestamp of the last activity on the game.
        start_time (int): Timestamp of the game start (Daily Chess only).
        time_control (str): PGN-compliant time control.
        time_class (str): Time-per-move grouping, used for ratings.
        rules (str): Game variant information.
        eco (str, optional): URL pointing to ECO opening.
        tournament (str, optional): URL pointing to tournament.
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
    username (str): Username.
    points (str): Points earned by player in this group adjusted in case of fair play recalculations. Defaults to "0".
    tie_break (str): Tie-break points by player earned in this group. Defaults to "0".
    is_advancing (bool): Whether player advances. Defaults to False.
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
    """List of games, players and fair play removals in tournament round group.

    Args:
        fair_play_removals (List[str]): List of removals due to breach of fair play.
        games (List[Dict[str, Any]]): List of games.
        players (List[Dict[str, Union[str, int, bool]]]): List of players.
    """

    fair_play_removals: List[str]
    games: List[Dict[str, Any]]
    players: List[Dict[str, Union[str, int, bool]]]

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        self.games = [TournamentRoundGroupGames(**x) for x in self.games]
        self.players = [TournamentRoundGroupPlayer(**x) for x in self.players]


class TournamentResults(BaseModel):
    """Tournament results of player.

    Args:
        url (str): Link to the PubAPI URL of the tournament.
        id (str): Link to the Web URL of the tournament.
        status (str): Final status of the player in this tourmanent {winner, eliminated, withdrew, removed}.
        wins (int): Number of wins.
        losses (int): Number of losses.
        draws (int): Number of draws.
        points_awarded (int, optional): Points awarded.
        placement (int, optional): Player placement.
        total_players (int): Total number of players in tournament.
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
    """Tournament status.

    Args:
        url (str): Link to the PubAPI URL of the tournament.
        id (str): Link to the Web URL of the tournament.
        status (str): Final status of the player in this tourmanent {winner, eliminated, withdrew, removed}.
    """

    url: str
    id: str
    status: str


class TournamentsSummary(BaseModel):
    """Summary of tournaments participated in.

    Args:
        count (int): Number of tournaments joined.
        withdraw (int): Number of tournaments withdrawn from.
        points (int): Total number of points earned in tournaments.
        highest_finish (int): Best tournament place.
    """

    count: int
    withdraw: int
    points: int
    highest_finish: int
