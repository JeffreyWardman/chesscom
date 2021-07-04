import pytest


@pytest.fixture
def username() -> str:
    return "erik"


@pytest.fixture
def month() -> int:
    return 5


@pytest.fixture
def year() -> int:
    return 2020


@pytest.fixture
def club_id() -> str:
    return "chess-com-developer-community"


@pytest.fixture
def tournament_id() -> str:
    return "-33rd-chesscom-quick-knockouts-1401-1600"


@pytest.fixture
def tournament_round() -> int:
    return 1


@pytest.fixture
def tournament_group() -> int:
    return 1


@pytest.fixture
def match_id() -> int:
    return 12803


@pytest.fixture
def live_match_id() -> int:
    return 5861


@pytest.fixture
def board() -> int:
    return 1


@pytest.fixture
def country_alpha_2() -> str:
    return "AU"
