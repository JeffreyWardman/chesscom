from typing import Any, Dict, List

from pydantic import BaseModel

AVAILABLE_LEADERBOARDS = [
    "daily",
    "daily960",
    "live_rapid",
    "live_blitz",
    "live_bullet",
    "live_bughouse",
    "live_blitz960",
    "live_threecheck",
    "live_crazyhouse",
    "live_kingofthehill",
    # "lessons",
    "tactics",
]


class Trend(BaseModel):
    """Amount changed in ranking and direction.

    Args:
        direction (int): Direction (0 or 1, where 1 is up and 0 is down).
        delta (int): Amount changed.
    """

    direction: int
    delta: int


class LeaderboardPlayerDetails(BaseModel):
    """
    Args:
        player_id (str): Player ID.
        id (str): Player URL ID.
        username (str): Username.
        score (int): Score.
        rank (int): Leaderboard rank.
        url (url): Player URL.
        country (str): Player country URL.
        status (str): Membership status.
        avatar (str): URL of image.
        trend_score (Dict[str, int], optional): Direction of player score and amount changed.
        trend_rank (Dict[str, int], optional): Direction of player rank and amount changed.
        flair_code (str): Flair icon code.
    """

    player_id: str
    id: str
    username: str
    score: int
    rank: int
    url: str
    country: str
    status: str
    avatar: str
    trend_score: Dict[str, int] = None
    trend_rank: Dict[str, int] = None
    flair_code: str

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        if self.trend_score is not None:
            self.trend_score = Trend(**self.trend_score)
        if self.trend_rank is not None:
            self.trend_rank = Trend(**self.trend_rank)


class LeaderboardDetails(BaseModel):
    f"""Leaderboard for {AVAILABLE_LEADERBOARDS}.\n
    Note: the endpoint refreshes when one of the leaderboards is updated.

    Args:
        daily (List[Dict[str, Any]]): Leaderboard for the daily game mode.
        daily960 (List[Dict[str, Any]]): Leaderboard for the daily960 game mode.
        live_rapid (List[Dict[str, Any]]): Leaderboard for the live rapid game mode.
        live_blitz (List[Dict[str, Any]]): Leaderboard for the live blitz game mode.
        live_bullet (List[Dict[str, Any]]): Leaderboard for the live bullet game mode.
        live_bughouse (List[Dict[str, Any]]): Leaderboard for the live bughouse game mode.
        live_blitz960 (List[Dict[str, Any]]): Leaderboard for the live blitz960 game mode.
        live_threecheck (List[Dict[str, Any]]): Leaderboard for the live three check game mode.
        live_crazyhouse (List[Dict[str, Any]]): Leaderboard for the live crazyhouse game mode.
        live_kingofthehill (List[Dict[str, Any]]): Leaderboard for the live king of the hill game mode.
        tactics (List[Dict[str, Any]]): Leaderboard for the tactics game mode.
    """
    daily: List[Dict[str, Any]]
    daily960: List[Dict[str, Any]]
    live_rapid: List[Dict[str, Any]]
    live_blitz: List[Dict[str, Any]]
    live_bullet: List[Dict[str, Any]]
    live_bughouse: List[Dict[str, Any]]
    live_blitz960: List[Dict[str, Any]]
    live_threecheck: List[Dict[str, Any]]
    live_crazyhouse: List[Dict[str, Any]]
    live_kingofthehill: List[Dict[str, Any]]
    # lessons: List[Dict[str, Any]]
    tactics: List[Dict[str, Any]]

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        for board in AVAILABLE_LEADERBOARDS:
            leaderboard = []
            for x in getattr(self, board):
                x["id"] = x.pop("@id")
                leaderboard.append(LeaderboardPlayerDetails(**x))
            setattr(self, board, leaderboard)
