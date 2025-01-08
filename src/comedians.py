
from typing import Optional


class Comedian:
    def __init__(self, id: Optional[int], pseudonym: Optional[str], variations: Optional[str],
                 first_name: Optional[str], last_name: Optional[str], title: Optional[str], female: Optional[bool],
                 status: Optional[str], entry: Optional[int], society: Optional[int], departure: Optional[int]) -> None:
        self.id = id
        self.pseudonym = pseudonym
        self.variations = variations
        self.first_name = first_name
        self.last_name = last_name
        self.title = title
        self.female = female
        self.status = status
        self.entry = entry
        self.society = society
        self.departure = departure

