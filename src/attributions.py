from typing import Optional


class Attribution:
    def __init__(self, id: Optional[int], play_id: Optional[int], author_id: Optional[int]) -> None:
        self.id = id
        self.play_id = play_id
        self.author_id = author_id

