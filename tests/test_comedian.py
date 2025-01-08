from src.comedians import Comedian


class TestComedian:
    def test_comedian(self):
        test_comedian = Comedian(id=1, pseudonym='test pseudonym', variations='test variations',
                                 first_name='test first name',
                                 last_name='test last name', title='test title', female=True, status='test status',
                                 entry=2, society=3, departure=4)

        assert test_comedian.id == 1
        assert test_comedian.pseudonym == 'test pseudonym'
        assert test_comedian.variations == 'test variations'
        assert test_comedian.first_name == 'test first name'
        assert test_comedian.last_name == 'test last name'
        assert test_comedian.title == 'test title'
        assert test_comedian.female == True
        assert test_comedian.status == 'test status'
        assert test_comedian.entry == 2
        assert test_comedian.society == 3
        assert test_comedian.departure == 4


