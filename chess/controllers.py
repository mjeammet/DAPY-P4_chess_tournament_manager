from chess.models.tournament import Tournament
from chess.database import get_database_table
from settings import DATABASE_PATH, VERBOSE
from chess.models import Player
from . import database
from . import views
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
        while self.current_controller is not None:
            next_controller = self.current_controller.run()
            self.current_controller = next_controller

class HomeController:
    
    def __init__(self):
        self.view = views.HomeViewFromExampe()

    def run(self):
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == '1':
            return NewPlayerController()
        elif next_action == "2":
            return NewTournamentController()
        elif next_action == "3":
            tournament_id = int(self.view.get_user_tournament_choice())
            tournament = get_tournament_by_id(tournament_id)
            return NewTournamentController()
        elif next_action == "5":
            return ReportMenuController()
        else:
            self.view.notify_invalid_choice()
            return HomeController()


class NewPlayerController:
    """Controller for the new player menu."""

    def __init__(self):
        self.view = views.NewPlayerView()

    def run(self):
        new_player_info = []
        new_player_id = get_database_table("players").all()[-1]["id"]
        new_player_info.append(new_player_id)
        inputted_info = self.view.get_new_player_info()
        new_player_info.extend(inputted_info)
        # print(new_player_info)
        Player(*new_player_info).save()
        print(f'---\n{new_player_info[1]} {new_player_info[2]} succesfully added with id {new_player_id}.')

        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == "1":
            return NewPlayerController()
        elif next_action == "2":
            return HomeController()
        else:
            self.view.notify_invalid_choice()
            return HomeController()      


class NewTournamentController:

    def __init__(self):
        self.view = views.NewTournamentView()
    
    def run(self):
        self.view.render()
        next_action = self.view.get_user_choice()


class ReportMenuController:
    
    def __init__(self):
        self.view = views.ReportMenu()                
        while True : 
            self.view.render()
            next_action = self.view.get_user_choice()
            if next_action == "1":
                # lists all player
                player_list = get_database_table("players").all()
                self.view.print_players(player_list)
            elif next_action == "2":
                # gets desired tournament and its players, deserialized
                tournament_id = int(self.view.get_user_tournament_choice())
                tournament = get_tournament_by_id(tournament_id)                                
                players_list = get_database_table("players").search(Query().id.one_of(list(tournament["players"])))

                self.view.print_players(players_list)
                # self.view.print_players()
            elif next_action == "3":
                tournaments_list = get_database_table("tournaments").all()
                self.view.print_players(tournaments_list)
            elif next_action == "4":
                tournament_id = int(self.view.get_user_tournament_choice())
                tournament = get_tournament_by_id(tournament_id, serialized=False)
                print(tournament.rounds)
            elif next_action == "0":
                return HomeController()
            else:
                self.view.notify_invalid_choice()

def get_tournament_by_id(tournament_id, serialized = True):
    """Selects a tournament, using its id """        
    serialized_tournament = get_database_table("tournaments").all()[tournament_id]

    if serialized: 
        return serialized_tournament
    else: 
        tournament = unserialize_tournament(serialized_tournament)
        return tournament

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