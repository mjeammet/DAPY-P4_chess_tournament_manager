class Player():
    """Un joueur pour le tournoi."""
    # TODO faire un dictionnaire pour le genre

    def __init__(self, first_name, last_name, birth_date, gender, ranking = 0):
        self.first_name = first_name
        self.last_name = last_name        
        self.birth_date = birth_date
        self.gender = gender
        self.ranking = ranking

    def __str__(self):
        return f'{self.full_name}'

    def __repr__(self):
        pass

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'