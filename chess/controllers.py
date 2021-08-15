from chess.database import get_database_table
from chess.constants import DATABASE_PATH
from chess.models import Player
from . import database
from tinydb import TinyDB
from . import views

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

class HomeController:
    
    def __init__(self):
        self.view = views.HomeViewFromExampe()
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == '1':
            return NewPlayerController()
        else:
            self.view.notify_invalid_choice()
            return HomeController()

class NewPlayerController:

    def __init__(self):
        self.view = views.NewPlayerView()
        self.get_player_info()
        self.view.render()
        next_action = self.view.get_user_choice()
        

    def get_player_info(self):
        print("Veuillez ajouter les informations du nouveau participant.")
        first_name = input('Prénom :')
        last_name = input('Nom de famille :')
        genre = input("Genre ('F','M','X'\) :")
        birth_year = input('Année de naissance (4 chiffres) :')
        ranking = input('Classement (if any, leave blank sinon) :')
        Player(first_name, last_name, birth_year, genre, ranking).add_to_database()