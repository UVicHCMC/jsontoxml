from src.roles import Role


class TestRole:
    def test_role(self):
        test_role = Role(
            id=1,
            name="test role",
            category="test category",
            female=True,
            play_id=4,
        )

        assert test_role.id == 1
        assert test_role.name == "test role"
        assert test_role.category == "test category"
        assert test_role.female is True
        assert test_role.play_id == 4
