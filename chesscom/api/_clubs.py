from typing import Any, Dict, List, Union

from pydantic import BaseModel


class ClubDetails(BaseModel):
    """Details about a club.

    Args:
        id (str): The location of this profile (always self-referencing).
        name (str): The human-readable name of this club.
        club_id (int): The non-changing Chess.com ID of this club.
        icon (str, optional): URL of a 200x200 image.
        country (str): Location of this club's country profile.
        average_daily_rating (int): Average daily rating.
        members_count (int): Total members count.
        created (int): Timestamp of creation on Chess.com.
        last_activity (int): Timestamp of the most recent post, match, etc.
        visibility (str): Whether the club is public or private.
        join_request (str): Location to submit a request to join this club.
        admin (List[str]): Array of URLs to the player profiles for the admins of this club.
        description (str): Text description of the club.
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
    """Join date of user.

    Args:
        BaseModel (str): Username.
        joined (int): Timestamp user joined club.
    """

    username: str
    joined: int


class ClubMembers(BaseModel):
    """List of club members and their join date as per timeframe.

    Args:
        weekly (List[Dict[str, Union[str, int]]]): Users joined in last week.
        monthly (List[Dict[str, Union[str, int]]]): Users joined in last month.
        all_time (List[Dict[str, Union[str, int]]]): All users joined.
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
    """Details about the match.

    Args:
        name (str): The team match name.
        id (str): URL pointing to the team match endpoint.
        opponent (str): URL pointing to the opponent club endpoint.
        result (str, optional): Game result.
        start_time (str, optional): Timestamp of the match start.
        time_class (str): Time class.
    """

    name: str
    id: str
    opponent: str
    result: str = None
    start_time: int = None
    time_class: str


class ClubMatches(BaseModel):
    """Lists of club matches that are registered, in progress or finished.

    Args:
        finished (List[Dict[str, Any]]): List of finished matches.
        in_progress (List[Dict[str, Any]]): List of in progress matches.
        registered (List[Dict[str, Any]]): List of registered matches.
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
