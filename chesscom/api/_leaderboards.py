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
    """
    direction: direction (0 or 1, where 1 is up and 0 is down)
    delta: amount changed
    """

    direction: int
    delta: int


class LeaderboardPlayerDetails(BaseModel):
    """
    player_id: player id
    id: player URL id
    username: username
    score: score
    rank: leaderboard rank
    url: player URL
    country: player country URL
    status: membership status
    avatar: URL of image
    trend_score: direction of player score and amount changed
    trend_rank: direction of player rank and amount changed
    flair_code: flair icon code
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
    f"""
    Leaderboard for {AVAILABLE_LEADERBOARDS}

    Note: the endpoint refreshes when one of the leaderboards is updated.

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
