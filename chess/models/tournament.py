TIME_CONTROL_TYPE = (
    "bullet"
    "blitz"
    "fast"
)

class Tournament:
    """Un tournoi
    TODO Gestion du temps"""

    def __init__(self, name, location, date='', rounds = '', players = [], time_control = '', description=''):
        self.name = name
        self.location = location
        self.date = date        
        self.players = players
        self.time_control = time_control
        self.description = description

        if rounds == '' or rounds == []:
            self.rounds = []
        else:
            self.rounds = rounds

    def __str__(self):
        print(
            f"{self.name} (Tournament object)\n"
            f"{self.location}\n")

    def serialize(self):
        composition = vars(self)
        composition['round'] = [round for round in self.rounds]
        # composition['matchs'] = [str(match_) for match_ in self.matchs]
        return composition