from chess.database import get_database_table
from tinydb import TinyDB
from chess.constants import DATABASE_PATH
# from chess.controllers import add_to_database

VERBOSE = False

players_table = get_database_table("players")

class Player():
    """Un joueur pour le tournoi.
    # TODO faire un dictionnaire pour le genre
    # TODO Sérialisation / Désérialisation ?
    """

    def __init__(self, first_name, last_name, birth_date, gender, ranking = 0):
        self.id = len(players_table)+1
        self.first_name = first_name
        self.last_name = last_name        
        self.birth_date = birth_date
        self.gender = gender
        self.ranking = ranking
        # add_to_database(self, 'players')

    def __str__(self):
        return f'{self.full_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def save(self):
        players_table = get_database_table("players")


    # def serialize(self):
