from chess.models import Tournament
from chess.database import get_database_table
from settings import DATABASE_PATH, VERBOSE, PLAYERS_PER_TOURNAMENT
from chess.models import Player, Tournament
from chess import database
from chess import views
from tinydb import Query

# recup les scores de cette manière si les un-tupler dans la méthode "sort_players" ne me satisfait pas
# then again, cette solution ne me satisfait pas non plus
# def get_scores(players_list, tournament):

class ApplicationController:
    """The app itself. Prints welcome."""

    def __init__(self):
        """Initialise la classe principale de l'application."""
        self.current_controller = HomeController()

    def start(self):
        """Démarre l'application."""
        print("HEEEEY WELCOME !\nNaviguez avec le clavier en renseignant le numéro / le chiffre correpondant à l'option qui vous intéresse.\n")

        while self.current_controller is not None:
            next_controller = self.current_controller.run()
            self.current_controller = next_controller

class HomeController:
    
    def __init__(self):
        self.view = views.HomeViewFromExampe()

    def run(self):
        # self.view.print_header("MENU PRINCIPAL")
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == '1':
            return PlayerHomeController()
        elif next_action == "2":
            return TournamentHubController()
        elif next_action == "3":
            return ReportMenuController()
        elif next_action == "Q":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return HomeController()


class PlayerHomeController:

    def __init__(self):
        self.view = views.PlayerHomeView()

    def run(self):
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == '1':
            return self.add_player()
        elif next_action == "0":
            return HomeController()
        elif next_action == "Q":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return PlayerHomeController()

    def add_player(self):
        print("Ajout d'un nouveau participant.")
        first_name = input('Prénom :')
        last_name = input('Nom de famille :')
        gender = input("Genre ('F','M','X'\) :")
        birth_year = input('Année de naissance (4 chiffres) :')
        ranking = input('Classement (if any, leave blank sinon) :')
        new_player_info = [first_name, last_name, birth_year, gender, ranking]

        # new_player_id = get_database_table("players").all()[-1]["id"] or 0
        # new_player_info.append(new_player_id)

        # inputted_info = self.view.get_new_player_info()
        # new_player_info.extend(inputted_info)
        # print(new_player_info)
        Player(*new_player_info).save()
        new_player_id = get_database_table("players").all()[-1].doc_id
        print(f'---\n{new_player_info[0]} {new_player_info[1]} succesfully added with id {new_player_id}.')
        return PlayerHomeController()


class NewPlayerController:
    """Controller for the new player menu."""

    def __init__(self):
        self.view = views.NewPlayerView()
    
    def run(self):
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == "1":
            return NewPlayerController()
        elif next_action == "2":
            return HomeController()
        elif next_action == "Q":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return NewPlayerController()      

class TournamentHubController:

    def __init__(self):
        self.view = views.TournamentHomeView()

    def run(self):
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == "1":
            return NewTournamentController()
        elif next_action == "2":
            return AddPlayerToTournamentController()
        elif next_action == "3":
            pass
        elif next_action == "4":
            pass
        elif next_action == "0":
            return HomeController()
        elif next_action == "Q":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return PlayerHomeController()


class NewTournamentController:

    def __init__(self):
        self.view = views.NewTournamentView()
    
    def run(self):
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == "Q":
            return EndController()

class AddPlayerToTournamentController:

    def __init__(self):
        self.view = ""
    
    def run(self):
        """ Add a player to tournament, using their id. """

        tournament_id = int(self.view.get_user_tournament_choice())
        tournament = get_object_by_id("tournaments", tournament_id, serizalized=False)
        
        # checks if tournament isn't already full
        #     if len(self.players) >= PLAYERS_PER_TOURNAMENT:
        #         print("Le tournoi est déjà plein, vous ne pouvez pas ajouter de participant.es.")
        #     else:
        
        while len(tournament.players) < 8:
            player_id = input("Which player id ?")    

            players_table = get_database_table("players")
            try:
                player = get_object_by_id(player_id)
            except IndexError:
                print(f"Unknown player #{id}. Please select a valid player id.")


            if players_table.search(Query().id == player_id) != []:
                tournament.add_player_to_tournament(player_id)
                if VERBOSE:
                    print(f'    {player["first_name"]} ajouté.e au tournoi')
            

        # notifies if it was the eighth player
        if len(tournament.players) == PLAYERS_PER_TOURNAMENT:
            print("8 participant.es ajouté.es au tournoi. Le tournoi est désormais plein ! ")


class ReportMenuController:
    
    def __init__(self):
        self.view = views.ReportMenu()  

    def run(self):
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == "1":
            # lists all players in database
            player_list = get_database_table("players").all()
            self.view.print_players(player_list)
        elif next_action == "2":
            tournaments_list = get_database_table("tournaments").all()
            self.view.print_tournaments(tournaments_list)
        elif next_action == "3":
            # gets desired tournament and its players, deserialized
            tournament_id = int(self.view.get_user_tournament_choice())
            tournament = get_object_by_id("tournaments", tournament_id)
            tournament_players_list = list(tournament["players"])

            # Done by list comprehension instead of query logic https://github.com/msiemens/tinydb/issues/293
            players_list = [ player for player in get_database_table("players").all() if player.doc_id in tournament_players_list ]

            self.view.print_players(players_list)
            # self.view.print_players()            
        elif next_action == "4":
            tournament_id = int(self.view.get_user_tournament_choice())
            tournament = get_object_by_id("tournaments", tournament_id, serialized=False)
            print(tournament.rounds)
        elif next_action == "0":
            return HomeController()
        elif next_action == "Q":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return ReportMenuController()


class EndController:
    """Controller handling app closure."""

    def __init__(self):
        self.view = views.EndView()

    def run(self):
        self.view.render()
        choice = self.view.confirm_exit()
        if choice == "Y":
            return None
        elif choice == "N":
            return HomeController()
        else:
            self.view.notify_invalid_choice()
            return EndController()


# FUNCTIONS TO REWORK
def get_object_by_id(table, object_id, serialized = True):
    """Selects a tournament, using its id """        
    serialized_object = get_database_table(table).get(doc_id = object_id)

    if serialized: 
        return serialized_object
    else: 
        object = unserialize_tournament(serialized_object)
        return object

def unserialize_tournament(serialized_tournament):        
    tournament = Tournament(*serialized_tournament.values())
    return tournament

def get_player_object(id):
    try: 
        player = Query()
        return players_table.search(player.id == id)
    except Exception as error:
        print("Unexpected error occurred.")
        raise error 