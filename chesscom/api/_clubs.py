from typing import Any, Dict, List, Union

from pydantic import BaseModel


class ClubDetails(BaseModel):
    """
    id: the location of this profile (always self-referencing)
    name: the human-readable name of this club
    club_id: the non-changing Chess.com ID of this club
    icon: (optional) URL of a 200x200 image
    country: location of this club's country profile
    average_daily_rating: average daily rating
    members_count: total members count
    created: timestamp of creation on Chess.com
    last_activity: timestamp of the most recent post, match, etc
    visibility: whether the club is public or private
    join_request: location to submit a request to join this club
    admin: array of URLs to the player profiles for the admins of this club
    description: text description of the club
    """

    id: str
    name: str
    club_id: int
    icon: str = None
    country: str
    average_daily_rating: int
    members_count: int
    created: int
    last_activity: int
    visibility: str
    join_request: str
    admin: List[str]
    description: str


class UserJoinClub(BaseModel):
    """
    username: username
    joined: timestamp user joined club
    """

    username: str
    joined: int


class ClubMembers(BaseModel):
    """
    weekly: users joined in last week
    monthly: users joined in last month
    all_time: all users joined
    """

    weekly: List[Dict[str, Union[str, int]]]
    monthly: List[Dict[str, Union[str, int]]]
    all_time: List[Dict[str, Union[str, int]]]

    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        self.weekly = [UserJoinClub(**x) for x in self.weekly]
        self.monthly = [UserJoinClub(**x) for x in self.monthly]
        self.all_time = [UserJoinClub(**x) for x in self.all_time]


class ClubMatchDetails(BaseModel):
    """
    name: the team match name
    id: URL pointing to the team match endpoint
    opponent: URL pointing to the opponent club endpoint
    result: Game result
    start_time: timestamp of the match start
    time_class: daily
    """

    name: str
    id: str
    opponent: str
    result: str = None
    start_time: int = None
    time_class: str


class ClubMatches(BaseModel):
    """
    finished: List of finished matches
    in_progress: List of in progress matches
    registered: List of registered matches
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
                matches.append(ClubMatchDetails(**match))
            setattr(self, match_type, matches)
