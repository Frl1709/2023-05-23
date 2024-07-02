from dataclasses import dataclass


@dataclass
class Player:
    playerID: str
    nameFirst: str
    nameLast: str
    ID: int
    year: int
    teamCode: str
    teamID: int
    salary: float

    def __hash__(self):
        return hash(self.playerID)







