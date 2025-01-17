from typing import Optional


class Play:
    def __init__(self, id: Optional[int], title: Optional[str], genre: Optional[str],
                 acts: Optional[int], prologue: Optional[bool], entertainment: Optional[bool], form: Optional[str],
                 creation_date: Optional[str]) -> None:

        self.id = id
        self.title = title
        self.genre = genre
        self.acts = acts
        self.prologue = prologue
        self.entertainment = entertainment
        self.form = form
        self.creation_date = creation_date


