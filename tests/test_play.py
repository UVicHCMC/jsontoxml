from src.plays import Play


class TestPlay:
    def test_play(self):
        test_play = Play(
            id=1,
            title="test title",
            genre="test genre",
            acts=3,
            prologue=True,
            entertainment=False,
            form="test form",
            creation_date="1700",
        )

        assert test_play.id == 1
        assert test_play.title == "test title"
        assert test_play.genre == "test genre"
        assert test_play.acts == 3
        assert test_play.prologue is True
        assert test_play.entertainment is False
        assert test_play.form == "test form"
        assert test_play.creation_date == "1700"
