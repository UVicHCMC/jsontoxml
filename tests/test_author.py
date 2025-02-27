from src.authors import Author


class TestAuthor:
    def test_author(self):
        test_author = Author(id=1, pseudonym='test pseudonym', female=True)

        assert test_author.id == 1
        assert test_author.pseudonym == 'test pseudonym'
        assert test_author.female == True
