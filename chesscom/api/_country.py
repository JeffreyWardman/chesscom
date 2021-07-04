from pydantic import BaseModel


class CountryDetails(BaseModel):
    """
    id: the location of this profile (always self-referencing)
    name: the human-readable name of this country
    code: the ISO-3166-1 2-character code
    """

    id: str
    name: str
    code: str
