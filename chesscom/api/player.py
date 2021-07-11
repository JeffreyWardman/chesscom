import io
from typing import List, Union

import chess.pgn
import requests

from ._player import (
    ChessModeRatings,
    ChessModeStats,
    ClubDetails,
    CurrentDailyChess,
    MonthlyArchive,
    PlayerMatches,
    PlayerProfile,
    PlayerTournaments,
    ToMoveDailyChess,
)

BASE_PLAYER_URL = "https://api.chess.com/pub/player"


class Player:
    """Player API wrapper."""

    @staticmethod
    def profile(username: str) -> PlayerProfile:
        """Get player profile.

        Args:
            username (str): Username.

        Returns:
            PlayerProfile: Player profile class.
        """
        api_url = f"{BASE_PLAYER_URL}/{username}"
        response = requests.get(api_url).json()
        response["id"] = response.pop("@id")
        return PlayerProfile(**response)

    @staticmethod
    def clubs(username: str) -> List[ClubDetails]:
        """Get list of clubs player is in.

        Args:
            username (str): Username.

        Returns:
            List[ClubDetails]: List of club details class.
        """
        api_url = f"{BASE_PLAYER_URL}/{username}/clubs"
        response = requests.get(api_url).json()

        clubs = []
        for club in response["clubs"]:
            club["id"] = club.pop("@id")
            clubs.append(ClubDetails(**club))
        return clubs

    @staticmethod
    def tournaments(username: str) -> PlayerTournaments:
        """Get list of tournaments player is in.

        Args:
            username (str): Username.

        Returns:
            PlayerTournaments: Player tournaments class.
        """
        api_url = f"{BASE_PLAYER_URL}/{username}/tournaments"
        response = requests.get(api_url).json()
        return PlayerTournaments(**response)

    @staticmethod
    def matches(username: str) -> PlayerMatches:
        """Get list of matches player is in.

        Args:
            username (str): Username.

        Returns:
            PlayerMatches: Player matches class.
        """
        api_url = f"{BASE_PLAYER_URL}/{username}/matches"
        response = requests.get(api_url).json()
        return PlayerMatches(**response)

    @staticmethod
    def online_status(username: str) -> bool:
        """Get online status of player (if they have been online in the last five minutes).

        Args:
            username (str): Username

        Returns:
            bool: Whether player is online.
        """
        api_url = f"{BASE_PLAYER_URL}/{username}/is-online"
        response = requests.get(api_url).json()
        return response["online"]

    @staticmethod
    def stats(username: str) -> List[Union[ChessModeStats, ChessModeRatings]]:
        """Get player stats for game modes.

        Args:
            username (str): Username.

        Returns:
            List[Union[ChessModeStats, ChessModeRatings]]: List of player stats for game modes.
        """
        api_url = f"{BASE_PLAYER_URL}/{username}/stats"
        response = requests.get(api_url).json()
        for mode in response:
            if "chess" in mode:
                response[mode] = ChessModeStats(**response[mode])
            elif mode in ("tactics", "lessons", "puzzle_rush"):
                response[mode] = ChessModeRatings(**response[mode])
        return response

    @staticmethod
    def current_daily_chess_games(username: str) -> List[CurrentDailyChess]:
        """Get current daily chess games of player.

        Args:
            username (str): Username.

        Returns:
            List[CurrentDailyChess]: List of current daily chess class.
        """
        api_url = f"{BASE_PLAYER_URL}/{username}/games"
        response = requests.get(api_url).json()
        return [CurrentDailyChess(**x) for x in response["games"]]

    @staticmethod
    def to_move_daily_chess_games(username: str) -> List[CurrentDailyChess]:
        """Get list of daily chess games where it is the player's turn to move.

        Args:
            username (str): Username.

        Returns:
            List[CurrentDailyChess]: List of current daily chess class (one per game).
        """
        api_url = f"{BASE_PLAYER_URL}/{username}/games/to-move"
        response = requests.get(api_url).json()
        return [ToMoveDailyChess(**x) for x in response["games"]]

    @staticmethod
    def monthly_archive_urls(username: str) -> List[str]:
        """Get list of URLs of monthly archives for player games.

        Args:
            username (str): Username.

        Returns:
            List[str]: List of URLs of monthly archives for player games.
        """
        api_url = f"{BASE_PLAYER_URL}/{username}/games/archives"
        response = requests.get(api_url).json()
        return response["archives"]

    @staticmethod
    def monthly_archive(
        username: str, year: Union[int, str], month: Union[int, str]
    ) -> List[MonthlyArchive]:
        """Get list of games from monthly archive URL of player.

        Args:
            username (str): Username.
            year (Union[int, str]): Year.
            month (Union[int, str]): Month.

        Returns:
            List[MonthlyArchive]: List of games.
        """
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
        """List of player games loaded from PGN format for a given month.

        Args:
            username (str): Username.
            year (Union[int, str]): Year.
            month (Union[int, str]): Month.

        Returns:
            List[chess.pgn.Game]: List of loaded PGN games.
        """
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
