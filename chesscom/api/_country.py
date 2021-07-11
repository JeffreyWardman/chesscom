from pydantic import BaseModel


class CountryDetails(BaseModel):
    """Country details.

    Args:
        id (str): The location of this profile (always self-referencing).
        name (str): The human-readable name of this country.
        code (str): The ISO-3166-1 2-character code.
    """

    id: str
    name: str
    code: str
