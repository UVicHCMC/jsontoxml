from typing import Optional


class Role:
    def __init__(self, id: Optional[int], name: Optional[str], category: Optional[str], female: Optional[bool], play_id: Optional[int]) -> None:
        self.id = id
        self.name = name
        self.category = category
        self.female = female
        self.play_id =play_id
