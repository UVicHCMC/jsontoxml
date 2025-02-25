from src.attributions import Attribution


class TestAttribution:
    def test_attribution(self):
        test_attribution = Attribution(id=1, play_id=2, author_id=3)

        assert test_attribution.id == 1
        assert test_attribution.play_id == 2
        assert test_attribution.author_id == 3
