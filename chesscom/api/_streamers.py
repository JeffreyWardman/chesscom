from pydantic import BaseModel


class StreamerDetails(BaseModel):
    """Streamer details.

    Args:
        username (str): Username.
        avatar (str): URL of avatar.
        twitch_url (str, optional): Twitch.tv URL.
        url (str): Member's Chess.com profile URL.
    """

    username: str
    avatar: str
    twitch_url: str = None
    url: str
