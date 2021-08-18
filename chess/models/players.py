from chess.database import get_database_table
from settings import DATABASE_PATH, VERBOSE
# from chess.controllers import add_to_database


class Player():
    """Un joueur pour le tournoi.
    # TODO faire un dictionnaire pour le genre
    # TODO Sérialisation / Désérialisation ?
    """

    def __init__(self, first_name, last_name, birth_date, gender, ranking = 0):
        self.first_name = first_name
        self.last_name = last_name        
        self.birth_date = birth_date
        self.gender = gender
        self.ranking = ranking

    def __str__(self):
        return f'{self.full_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def save(self):
        table_name = "players"
        players_table = get_database_table(table_name)
        # players_database.append(object) # relique de quand la db était une simple liste 
        # print(vars(self))
        players_table.insert(vars(self))
        if VERBOSE:           
            print(f'    {self.full_name} ajouté.e à la base de données.')


    # def serialize(self):
