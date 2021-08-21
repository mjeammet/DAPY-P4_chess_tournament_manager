from tinydb import Query 
from chess.models import Tournament
from chess.models import get_database_table, empty_database_table
from chess.models import Player, Tournament
from chess import views
from settings import DATABASE_PATH, VERBOSE, PLAYERS_PER_TOURNAMENT

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
        self.current_controller.view.print_welcome()

        while self.current_controller is not None:
            next_controller = self.current_controller.run()
            self.current_controller = next_controller

class HomeController:
    
    def __init__(self):
        self.view = views.HomeViewFromExampe()

    def run(self):
        self.view.print_header("MENU PRINCIPAL")
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == '1':
            return PlayerHomeController()
        elif next_action == "2":
            return TournamentHubController()
        elif next_action == "3":
            return ReportMenuController()
        elif next_action == "9":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return HomeController()


class PlayerHomeController:

    def __init__(self):
        self.view = views.PlayerHomeView()

    def run(self):
        self.view.print_header(title = "MENU DES JOUEURS")
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == '1':
            self.get_new_player_info()
            return PlayerHomeController()
        elif next_action == "2":
            self.update_player_infos()
            return PlayerHomeController()
        elif next_action == "0":
            return HomeController()
        elif next_action == "9":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return PlayerHomeController()

    def get_new_player_info(self):
        print("Ajout d'un nouveau participant.")
        # TODO faire ça en plus class ou on valide avec une fonction dédiée ? Un wrapper ?
        
        first_name = self.view.get_first_name()
        last_name = self.view.get_last_name()
        gender = self.view.get_gender()
        birth_date = self.view.get_birth_date()
        try:
            ranking = int(self.view.get_ranking())
        except: 
            print("Veuillez entrer un entier positif.\n")
            ranking = self.view.get_ranking()
        new_player_info = [first_name, last_name, gender, birth_date, ranking]

        # TODO check if player is already in the database
        # TODO transformer en une une fonction search_player() qui servira aussi à aller update les infos du player
        existing_homonyme = get_database_table("players").search((Query().first_name == first_name) & (Query().last_name == last_name))
        if existing_homonyme != []:
            self.view.print_homonyme(new_player_info, existing_homonyme)
            next_action = self.view.get_user_choice()
            if next_action == '1':
                self.update_player_infos()
            elif next_action == "2":
                self.add_player_to_database(new_player_info)
            elif next_action == "3":
                print("Ajout annulé.\n")
            else:
                self.view.notify_invalid_choice()                
        else:
            self.add_player_to_database(new_player_info)
            PlayerHomeController()            
            

    def add_player_to_database(self, new_player_info):
        """Add a player to the database.
        
        Args:
            - new player informations (see Player model).

        Returns:
            - new player id
        """
        new_player = Player(*new_player_info)
        new_player_id = add_object_to_database("players", new_player)
        # new_player_id = get_database_table("players").all()[-1].doc_id
        print(f'---\n{new_player_info[0]} {new_player_info[1]} succesfully added with id {new_player_id}.')
        return new_player_id

    def update_player_infos(player_id="", first_name="", last_name="", gender="", birth_date="", ranking=""):
        """Update a player in the database."""

        if type(player_id) != int:
            player_id = int(input("Id du joueur que vous souhaitez modifier ? "))
            existing_player = get_db_object("players", player_id)

        print(f"Updating player {player_id}:\n")
        # TODO peu-être remplacer les != "" par des is.valid()
        if first_name != "":
            print(f"changement du first_name {existing_player['first_name']} pour {first_name}")
        else:
            print(
                'Veuillez entrer sélectionner le champ à modifier:\n'
                "1. Prénom\n"
                "2. Nom de famille.\n"
                "3. Genre\n"
                "4. Date de naissance\n"
                "5. Classement.\n"
                "0 pour annuler la modification.\n"        
            ) 
            next_action = int(input("Quel champ souhaitez-vous modifier ? "))
            print(f"L'entrée actuelle est : {existing_player['first_name']}")            
            if next_action == 1:
                updated_field = "first_name"
                updated_info = input("Veuillez entrer le nouveau prénom : ")
            elif next_action == 2:
                updated_field = "last_name"
                updated_info = input("Veuillez entrer le nouveau nom : ")
            elif next_action == 3:
                updated_info = input("Veuillez entrer le nouveau genre : ")
                existing_player["gender"] = updated_info
            elif next_action == 4: 
                updated_info = input("Veuillez entrer la nouvelle date de naissance : ")
                existing_player["birth_date"] = updated_info
            elif next_action == 5:
                updated_info = input("Veuillez entrer le nouveau classement : ")
                existing_player["ranking"] = updated_info
            else:
                print("Stop trolling please.")
                return PlayerHomeController()
            get_database_table("players").update({updated_field: updated_info}, doc_ids = [player_id])

    # @wrap()
    # def validate_data(self):
        # print(function)

        # def wrapper(*args, **kwargs):
        #     return function (*args, **kwargs)
            # print(user_input)
            # while user_input == None or user_input == "": 
            #     print("oh come on !")
            #     user_input = function (*args, **kwargs)            
            # return user_input


        # if wanted_data == "first_name":
        #     wanted_data = self.view.get_first_name()
        #     while len(wanted_data) < 2 or wanted_data=="":
        #         print("Le prénom ne peut pas être un champ vide ou un chiffre.\n")
        #         wanted_data = self.view.get_first_name()

class TournamentHubController:

    def __init__(self):
        self.view = views.TournamentHomeView()

    def run(self):
        # TODO utiliser une fonction header de baseview en passant le titre ? 
        # TODO pour ce contrôleur seulement, passer par une fonction dédiée pour afficher le "current_controller"
        self.view.print_header("MENU DES TOURNOIS")
        try:
            tournament_id = int(self.current_tournament_id)
            current_tournament_name = get_db_object("tournaments", tournament_id, serialized=True)["name"]
            self.view.print_current_tournament(current_tournament_name)
            print('did it work ?')
        except AttributeError: 
            # print(self.current_tournament_id)
            self.view.print_current_tournament("None")

        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == "1":
            self.get_new_tournament_info()
            return TournamentHubController()
        elif next_action == "2":
            self.current_tournament_id = int(self.view.get_user_tournament_choice())
            print(self.current_tournament_id)
            return TournamentHubController()
        elif next_action == "3":
            player_id = self.get_player_by_id()
            self.add_player_to_tournament()
            return TournamentHubController()
        elif next_action == "4":
            pass
        elif next_action == "5":
            pass
        elif next_action == "0":
            return HomeController()
        elif next_action == "9":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return PlayerHomeController()

    def get_new_tournament_info(self):
        # TODO for argument in signature(Tournament): ? 
        name = self.view.get_name()
        location = self.view.get_location()
        date = self.view.get_date()
        time_control = self.view.get_time_control()
        description = self.view.get_description()
        new_tournament_info = [name, location, date, [], [], time_control, description]
        self.add_new_tournament_to_database(new_tournament_info)

    def add_new_tournament_to_database(self, new_tournament_info):
        new_tournament = Tournament(*new_tournament_info)
        new_tournament_id = add_object_to_database("tournaments", new_tournament)
        # new_player_id = get_database_table("players").all()[-1].doc_id
        print(f'---\n{new_tournament_info[0]} succesfully added with id {new_tournament_id}.')
        self.current_tournament_id = new_tournament_id
        # TODO faire en sorte que le current_tournament change après l'ajout d'un tournoi
        return new_tournament_id

    def select_current_tournament(self):
        self.current_tournament_id = "Juste un autre tournoi."

    def add_player_to_tournament():
        """ Add a player to tournament, using their id. """

        tournament_id = int(self.view.get_user_tournament_choice())
        tournament = get_db_object("tournaments", tournament_id, serizalized=False)
        
        # checks if tournament isn't already full
        #     if len(self.players) >= PLAYERS_PER_TOURNAMENT:
        #         print("Le tournoi est déjà plein, vous ne pouvez pas ajouter de participant.es.")
        #     else:
        
        while len(tournament.players) < 8:
            player_id = input("Which player id ?")    

            players_table = get_database_table("players")
            try:
                player = get_db_object(player_id)
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
        self.view.print_header(title = "MENU DES RAPPORTS")
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == "1":
            # lists all players in database
            player_list = get_database_table("players").all()
            self.view.print_players(player_list)
            return ReportMenuController()
        elif next_action == "2":
            tournaments_list = get_database_table("tournaments").all()
            self.view.print_tournaments(tournaments_list)
            return ReportMenuController()
        elif next_action == "3":
            # gets desired tournament and its players, deserialized
            tournament_id = int(self.view.get_user_tournament_choice())
            tournament = get_db_object("tournaments", tournament_id)
            tournament_players_list = list(tournament["players"])

            # Done by list comprehension instead of query logic https://github.com/msiemens/tinydb/issues/293
            players_list = [ player for player in get_database_table("players").all() if player.doc_id in tournament_players_list ]

            self.view.print_players(players_list)
            # self.view.print_players()
            return ReportMenuController()    
        elif next_action == "4":
            tournament_id = int(self.view.get_user_tournament_choice())
            tournament = get_db_object("tournaments", tournament_id, serialized=False)
            print(tournament.rounds)
            return ReportMenuController()
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


def add_object_to_database(table_name, serialized_object):
    """Add an new object to the database.
    
    return id of the newly added element."""
    table = get_database_table(table_name)
    # players_database.append(object) # relique de quand la db était une simple liste 
    # print(vars(self))
    table.insert(vars(serialized_object))
    if VERBOSE:           
        print(f'    {serialized_object} ajouté.e à la base de données.')
    return table.all()[-1].doc_id

# FUNCTIONS TO REWORK
def get_db_object(table, object_id, serialized = True):
    """Selects a tournament, using its id """        
    serialized_object = get_database_table(table).get(doc_id = object_id)

    if serialized: 
        return serialized_object
    else: 
        object = unserialize_object(serialized_object, table)
        return object

def unserialize_object(serialized_object, type):
    if type.lower() == "players":
        object = Player(*serialized_object.values())
    elif type.lower() == "tournaments":
        object = Tournament(*serialized_object.values())
    else:
        error = f"Provided type '{type}'' is not a valid database table."
        raise error
    return object