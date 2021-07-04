from chesscom.api.streamers import Streamers


class TestStreamers:
    @staticmethod
    def test_list_all():
        Streamers.list_all()
