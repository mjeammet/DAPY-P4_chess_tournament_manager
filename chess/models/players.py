from chess.database import get_database_table
from tinydb import TinyDB
from chess.constants import DATABASE_PATH

VERBOSE = False

# players_database = ['0 is not a player. A régler une fois qu\'on aura la db']
players_table = get_database_table("players")

def get_player_object(id):
    try: 
        return players_table.search(Query().id == id)
    except Exception as error:
        print("Unexpected error occurred.")
        raise error 

class Player():
    """Un joueur pour le tournoi.
    # TODO faire un dictionnaire pour le genre
    # TODO Sérialisation / Désérialisation ?
    """

    def __init__(self, first_name, last_name, birth_date, gender, ranking = 0):
        self.id = len(players_table)
        self.first_name = first_name
        self.last_name = last_name        
        self.birth_date = birth_date
        self.gender = gender
        self.ranking = ranking
        self.add_to_database()

    def __str__(self):
        return f'{self.full_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def add_to_database(self):
        players_table = get_database_table("players")
        # players_database.append(self) # relique de quand la db était une simple liste 
        players_table = TinyDB(DATABASE_PATH).table("players").insert(vars(self))
        if VERBOSE:           
            print(f'    {self.full_name} ajouté.e à la base de données.')

    # def serialize(self):
