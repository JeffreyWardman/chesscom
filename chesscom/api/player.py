import io
from typing import List, Union

import chess.pgn
import requests

from ._player import (
    ChessMode,
    ClubDetails,
    CurrentDailyChess,
    GameMode,
    MonthlyArchive,
    PlayerMatches,
    PlayerProfile,
    PlayerTournaments,
    ToMoveDailyChess,
)

BASE_PLAYER_URL = "https://api.chess.com/pub/player"


class Player:
    @staticmethod
    def profile(username: str) -> PlayerProfile:
        api_url = f"{BASE_PLAYER_URL}/{username}"
        response = requests.get(api_url).json()
        response["id"] = response.pop("@id")
        return PlayerProfile(**response)

    @staticmethod
    def clubs(username: str) -> List[ClubDetails]:
        api_url = f"{BASE_PLAYER_URL}/{username}/clubs"
        response = requests.get(api_url).json()

        clubs = []
        for club in response["clubs"]:
            club["id"] = club.pop("@id")
            clubs.append(ClubDetails(**club))
        return clubs

    @staticmethod
    def tournaments(username: str) -> PlayerTournaments:
        api_url = f"{BASE_PLAYER_URL}/{username}/tournaments"
        response = requests.get(api_url).json()
        return PlayerTournaments(**response)

    @staticmethod
    def matches(username: str):
        api_url = f"{BASE_PLAYER_URL}/{username}/matches"
        response = requests.get(api_url).json()
        return PlayerMatches(**response)

    @staticmethod
    def online_status(username: str) -> bool:
        api_url = f"{BASE_PLAYER_URL}/{username}/is-online"
        response = requests.get(api_url).json()
        return response["online"]

    @staticmethod
    def stats(username: str) -> List[Union[ChessMode, GameMode]]:
        api_url = f"{BASE_PLAYER_URL}/{username}/stats"
        response = requests.get(api_url).json()
        for mode in response:
            if "chess" in mode:
                response[mode] = ChessMode(**response[mode])
            elif mode in ("tactics", "lessons", "puzzle_rush"):
                response[mode] = GameMode(**response[mode])
        return response

    @staticmethod
    def current_daily_chess_games(username: str) -> List[CurrentDailyChess]:
        api_url = f"{BASE_PLAYER_URL}/{username}/games"
        response = requests.get(api_url).json()
        return [CurrentDailyChess(**x) for x in response["games"]]

    @staticmethod
    def to_move_daily_chess_games(username: str) -> List[CurrentDailyChess]:
        api_url = f"{BASE_PLAYER_URL}/{username}/games/to-move"
        response = requests.get(api_url).json()
        return [ToMoveDailyChess(**x) for x in response["games"]]

    @staticmethod
    def monthly_archive_urls(username: str) -> List[str]:
        api_url = f"{BASE_PLAYER_URL}/{username}/games/archives"
        response = requests.get(api_url).json()
        return response["archives"]

    @staticmethod
    def monthly_archive(
        username: str, year: Union[int, str], month: Union[int, str]
    ) -> List[MonthlyArchive]:
        if isinstance(year, (int, float)):
            year = str(int(year))

        assert 1 <= int(month) <= 12

        if isinstance(month, (int, float)):
            month = str(int(month))

        if len(month) == 1:
            month = "0" + month

        api_url = f"{BASE_PLAYER_URL}/{username}/games/{year}/{month}"
        response = requests.get(api_url).json()

        return [MonthlyArchive(**x) for x in response["games"]]

    @staticmethod
    def monthly_pgns(
        username: str, year: Union[int, str], month: Union[int, str]
    ) -> List[chess.pgn.Game]:
        if isinstance(year, (int, float)):
            year = str(int(year))

        assert 1 <= int(month) <= 12

        if isinstance(month, (int, float)):
            month = str(int(month))

        if len(month) == 1:
            month = "0" + month

        api_url = f"{BASE_PLAYER_URL}/{username}/games/{year}/{month}/pgn"
        response = requests.get(api_url)

        pgn_file = io.StringIO(response.content.decode())
        pgns = []
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:  # End of file
                break
            pgns.append(game)
        return pgns
