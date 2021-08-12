from chess.database import get_database_table
from chess.constants import DATABASE_PATH
from . import database
from tinydb import TinyDB

VERBOSE = False

def get_player_object(id):
    try: 
        player = Query()
        return players_table.search(player.id == id)
    except Exception as error:
        print("Unexpected error occurred.")
        raise error 

def add_to_database(object, type):
        players_table = get_database_table(type)
        # players_database.append(object) # relique de quand la db était une simple liste 
        players_table = TinyDB(DATABASE_PATH).table(type).insert(vars(object))
        if VERBOSE:           
            print(f'    {object.full_name} ajouté.e à la base de données.')

# recup les scores de cette manière si les un-tupler dans la méthode "sort_players" ne me satisfait pas
# then again, cette solution ne me satisfait pas non plus
# def get_scores(players_list, tournament):
