from pydantic import BaseModel


class StreamerDetails(BaseModel):
    """
    username: username
    avatar: URL,
    twitch_url: Twitch.tv URL
    url: member url's
    """

    username: str
    avatar: str
    twitch_url: str = None
    url: str
