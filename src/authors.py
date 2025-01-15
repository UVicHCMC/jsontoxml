from typing import Optional


class Author:
    def __init__(self, id: Optional[int], pseudonym: Optional[str], female: Optional[bool]) -> None:
        self.id = id
        self.pseudonym = pseudonym
        self.female = female
