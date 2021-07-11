from chesscom.api.clubs import Club


class TestClub:
    @staticmethod
    def test_details(club_id):
        Club.details(club_id)

    @staticmethod
    def test_members(club_id):
        Club.members(club_id)

    @staticmethod
    def test_matches(club_id):
        Club.matches(club_id)
