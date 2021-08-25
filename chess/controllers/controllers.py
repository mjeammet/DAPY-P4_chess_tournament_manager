from datetime import datetime
from tinydb import Query 
from chess.models import Tournament
from chess.models import Database
from chess.models import Player, Tournament, Round, Match
from chess import views
from settings import VERBOSE, PLAYERS_PER_TOURNAMENT, ROUNDS_PER_TOURNAMENT

# recup les scores de cette manière si les un-tupler dans la méthode "sort_players" ne me satisfait pas
# then again, cette solution ne me satisfait pas non plus
# def get_scores(players_list, tournament):

# TODO TournamentMenuController > turn self.current_controller_id into the object tournament

class ApplicationController:
    """The app itself. Prints welcome."""

    def __init__(self):
        """Initialise la classe principale de l'application."""
        self.current_controller = HomeController()

    def start(self):
        """Démarre l'application."""
        self.current_controller.view.print_welcome()

        try: 
            while self.current_controller is not None:
                next_controller = self.current_controller.run()
                self.current_controller = next_controller
        except KeyboardInterrupt:
            print("\nBISOUUUUUS !")

class HomeController:
    
    def __init__(self):
        self.title = "MENU PRINCIPAL"
        self.view = views.HomeView()
        self.database = Database()

    def run(self):
        self.view.print_header(self.title)
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == "1":
            # Displays all tournaments
            tournaments_list = self.database.tournaments_table.all()
            for tournament in tournaments_list:
                print(tournament)
            self.view.press_any_key()
            return HomeController()
        elif next_action == "2":
            # Creation of a new tournament
            new_tournament_infos = self.get_new_tournament_info()
            new_tournament = self.add_new_tournament_to_database(new_tournament_infos)
            return self.run()
        elif next_action == "3":
            return TournamentMenuController(current_tournament=None)
        elif next_action == '4':
            return PlayerMenuController()
        elif next_action == "9":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return self.run()

    def get_new_tournament_info(self) -> int:
        """Get all infos for new tournament.
        
        Args:
            (none)
            
        Returns a list containing the collected datas"""
        # TODO for argument in signature(Tournament): ? 
        name = self.view.get_name()
        location = self.view.get_location()
        date = self.view.get_date()
        time_control = self.view.get_time_control()
        description = self.view.get_description()
        return [name, location, date, [], [], time_control, description]        

    def add_new_tournament_to_database(self, new_tournament_info):
        """Add a new tournament to the database.
        Probably to move in database model.
        
        Args:
            - Informations of new tournament
    
        Returns:
            - database id of the new tournament"""
        new_tournament = Tournament(*new_tournament_info)
        new_tournament_id = self.database.add_to_database("tournaments", new_tournament)
        # new_player_id = self.database.players_table.all()[-1].doc_id
        print(f'---\n{new_tournament_info[0]} succesfully added with id {new_tournament_id}.')
        self.view.press_any_key()
        self.current_tournament = new_tournament
        # TODO faire en sorte que le current_tournament change après l'ajout d'un tournoi
        return new_tournament

class PlayerMenuController:

    def __init__(self):
        self.title = "MENU DES JOUEURS"
        self.view = views.PlayerHomeView()
        self.database = Database()

    def run(self):
        self.view.print_header(self.title)
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == '1':
            self.list_database_players()
            return self.run()
        elif next_action == '2':
            self.get_new_player_info()
            return self.run()
        elif next_action == "3":
            self.update_player_infos()
            return self.run()
        elif next_action == "0":
            return HomeController()
        elif next_action == "9":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return PlayerMenuController()

    def list_database_players(self):
        # lists all players in database
        player_list = self.database.players_table.all()
        self.view.print_players(player_list)
        return None

    def get_new_player_info(self):
        print("Ajout d'un nouveau participant.")
        # TODO faire ça en plus class ou on valide avec une fonction dédiée ? Un wrapper ?
        
        first_name = self.view.get_first_name()
        last_name = self.view.get_last_name()        
        birth_date = self.view.get_birth_date()
        gender = self.view.get_gender()
        ranking = self.view.get_ranking()
        new_player_info = [first_name, last_name, birth_date, gender, ranking]

        # TODO check if player is already in the database
        # TODO transformer en une une fonction search_player() qui servira aussi à aller update les infos du player
        
        existing_duplicate = self.check_existing_homonyme(new_player_info)
        if existing_duplicate != []:
            self.view.print_homonyme(new_player_info, existing_duplicate)
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
            return None            
            
    def check_existing_homonyme(self, new_player_info):
        """From inputted player info, check for duplicate in the database."""
        first_name = new_player_info[0]
        last_name = new_player_info[1]
        return self.database.players_table.search((Query().first_name == first_name) & (Query().last_name == last_name))
    
    def add_player_to_database(self, new_player_info):
        """Add a player to the database.
        
        Args:
            - new player informations (see Player model).

        Returns:
            - new player id
        """
        new_player = Player(*new_player_info)
        new_player_id = self.database.add_to_database("players", new_player)
        # new_player_id = self.database.players_table.all()[-1].doc_id
        print(f'---\n{new_player_info[0]} {new_player_info[1]} succesfully added with id {new_player_id}.')
        return new_player_id

    def update_player_infos(self, player_id="", first_name="", last_name="", gender="", birth_date="", ranking=""):
        """Update a player in the database."""

        if type(player_id) != int:
            player_id = int(input("Id du joueur que vous souhaitez modifier ? "))
            existing_player = self.database.get_db_object("players", player_id)

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
            if next_action == 1:
                updated_field = "first_name"
                print(f"L'entrée actuelle est : {existing_player[updated_field]}")
                updated_info = input("Veuillez entrer le nouveau prénom : ")
            elif next_action == 2:
                updated_field = "last_name"
                print(f"L'entrée actuelle est : {existing_player[updated_field]}")
                updated_info = input("Veuillez entrer le nouveau nom : ")
            elif next_action == 3: 
                updated_field = "birth_date"
                print(f"L'entrée actuelle est : {existing_player[updated_field]}")
                updated_info = input("Veuillez entrer la nouvelle date de naissance : ")
            elif next_action == 4:
                updated_field = "gender"
                print(f"L'entrée actuelle est : {existing_player[updated_field]}")
                updated_info = input("Veuillez entrer le nouveau genre : ")            
            elif next_action == 5:
                updated_field = "ranking"
                print(f"L'entrée actuelle est : {existing_player[updated_field]}")
                updated_info = input("Veuillez entrer le nouveau classement : ")
            else:
                print("Stop trolling please.")
                return PlayerMenuController()
            self.database.players_table.update({updated_field: updated_info}, doc_ids = [player_id])

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

class TournamentMenuController:

    def __init__(self, current_tournament):
        self.title = "MENU DES TOURNOIS"
        self.view = views.TournamentHomeView()
        self.current_tournament = current_tournament
        self.database = Database()

    def run(self):
        self.view.print_header(self.title)
        if self.current_tournament != None:
            current_tournament_name = self.current_tournament.name
            self.view.print_current_tournament(current_tournament_name)
        else:
            self.view.print_current_tournament("None")
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == "1":
            # Selected "prints entrants"
            if self.current_tournament == None:
                self.current_tournament = self.select_current_tournament()

            # Done by list comprehension instead of query logic https://github.com/msiemens/tinydb/issues/293
            for player_id in self.current_tournament.players:
                player = self.database.players_table.get(doc_id = player_id)
                print(player)

            self.view.press_any_key()
            return self.run()
        if next_action == "2":
            # Adds a player to the selected tournament
            
            if self.current_tournament == None:
                self.current_tournament = self.select_current_tournament()
            
            if len(self.current_tournament.players) >= PLAYERS_PER_TOURNAMENT:
                alert = "Le tournoi est déjà plein, vous ne pouvez pas ajouter de participant.es."
                self.view.print_alert(alert)
            else:        
                self.add_player_to_tournament()
            return self.run()
        elif next_action == "3":
            # Selected "prints rounds"

            if self.current_tournament == None:
                self.current_tournament = self.select_current_tournament()


            self.view.print_round_header()
            for round in self.current_tournament.rounds:
                self.view.print_round_details(round)
            self.view.press_any_key()
            return self.run()
        elif next_action == "4":
            # Selected "New round"
            if self.current_tournament == None:
                self.current_tournament = self.select_current_tournament()
            new_round = self.launch_new_round()

            # if new_round != None:
            #     serialized_round = [round.serialize() for round in self.current_tournament.rounds]
            #     print(f"Updating DB with round {serialized_round}")
            #     # update database to include new round 
            #     self.database.tournaments_table.update({"rounds": serialized_round}, Query().name == self.current_tournament.name)
            
            return self.run()
        elif next_action == "5":
            # Selected "update round"

            if self.current_tournament == None:
                self.current_tournament = self.select_current_tournament()

            round_to_update = self.current_tournament.rounds[-1]
            updated_results = self.update_round_results(round_to_update)
            round_to_update.matchs = updated_results

            # self.database.update_round_results(round_to_update)
            serialized_round = [round.serialize() for round in self.current_tournament.rounds]
            self.database.tournaments_table.update({"rounds": serialized_round}, Query().name == self.current_tournament.name)     
            return self.run()
        elif next_action == "6":
            # List matches
            for round in self.current_tournament.rounds:
                print(round.matchs)
            return self.run()
        elif next_action == "7":
            # Change selected tournament
            selected_tournament = self.select_current_tournament()
            self.current_tournament = selected_tournament
            return self.run()
        elif next_action == "0":
            return HomeController()
        elif next_action == "9":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return self.run()

    def select_current_tournament(self):
        """Prompts user to select a tournament as current tournament.
        
        Returns : 
            - an tournament object (unserialized) or None if """        
        try:
            inputted_id = int(self.view.get_user_tournament_choice())
            serialized_tournament = self.database.tournaments_table.get(doc_id = inputted_id)
        except ValueError:
            error_message = 'L\'id doit être un entier positif. Tournoi actuel inchangé.'
            self.view.print_alert(error_message)
            return None
        except AttributeError:
            error_message = f"Aucun tournoi trouvé sous l'id n°{inputted_id}. Tournoi actuel inchangé."
            self.view.print_alert(error_message)
            return None
        
        #unserialize_tournament()
        tournament = unserialize_object(serialized_tournament, type="tournaments")
        name = tournament.name
        print(f"Tournoi {name} sélectionné comme tournoi en cours.")
        return tournament
        
    def add_player_to_tournament(self):
        """ Add a player to tournament, using their id. """

        # checks if tournament isn't already full        
        player_id = int(input("Id du joueur que vous souhaiter ajouter : "))
        if player_id in self.current_tournament.players:
            print("Player already in tournament.")
            return self.view.press_any_key()

        # Making sure que le player est bien dans la DB
        try: 
            self.database.players_table.get(doc_id = player_id)
        # Add except
        finally: 
            self.current_tournament.append(player_id)
            # if VERBOSE: 
            #     print(f'    {player["first_name"]} ajouté.e au tournoi')
            self.database.tournaments_table.update({"players": self.current_tournament.players}, Query().name == self.current_tournament.name)
            
        # notifies if it was the eighth player
        if len(self.current_tournament.players) == PLAYERS_PER_TOURNAMENT:
            print("8 participant.es ajouté.es au tournoi. Le tournoi est désormais plein ! ")

    def launch_new_round(self):
        # Get the new turn's number
        round_number = int(len(self.current_tournament.rounds))+1

        if round_number >= ROUNDS_PER_TOURNAMENT:
            error_message = f"Le nombre de tour par tournoi ne peut pas excéder {ROUNDS_PER_TOURNAMENT} (voir \"settings.py\")."
            self.view.print_alert(error_message)
            return None
        else:
            print(f'Starting round number {round_number}')

            # # sort players
            if round_number == 1:
                players_order = self.sort_players(self.current_tournament.players, by = 'ranking')
            else :
                players_order = self.sort_players(self.current_tournament.players, by = 'score')

            print(players_order)
            exit()
            # print(players_order)
            round_matchs = self.pair_players(players_order)
            # TODO find a way to store matches as dictionaries too
            # upsert a temporary 
            # checking if we have a duo we already previously had
            # if it's the case, try and mickmack with someone else

            round_name = f'Round_{round_number}'
            round_starttime = str(datetime.today())
            round_endtime = None
            # # Add a new round with rank players and their associated scores
            
            this_round = Round(round_name, round_starttime, round_endtime, round_matchs)
            print(f'{this_round.name} créé le {this_round.start_datetime}.')
            self.current_tournament.rounds.append(this_round)

            if self.current_tournament != None:
                return self.current_tournament
            else:
                return None
            
    def sort_players(self, players_list, by = 'score', tournament_id=None):
        """ Sorts player to generate pairs according to the swiss tournament pattern. 
        
        Args:
            - a list of players
            - by -- the parameter by which players will be sorted. Can be 'score' or 'ranking'.
            - optional, a tournament_id to gather players' score in the database

        Returns:
        - a sorted list of players' ids
        """
        # if by == 'score':            
        #     #        
        #     # Sorts player by score of previous round
        #     sorted_players = sorted(players_score, key = lambda x: x[1], reverse=True)
        #     # print("sorted score = ", sorted_players)
            
        #     self.players = [item[0] for item in sorted_players]
        #     return sorted_players
        
        # filters the database to only get this tournament's entrants
        entrants = []
        for entrants_id in players_list:
            entrants.append(self.database.players_table.get(doc_id = entrants_id))    

        try:
            if by == 'ranking':
                return [player.doc_id for player in sorted(entrants, key = lambda x:x['ranking'], reverse=True)]
            elif by == 'name':
                return [player.doc_id for player in sorted(entrants, key = lambda x:x['last_name'])]
            elif by == 'score':
                print(self.current_tournament.serialize())                
                previous_round = self.current_tournament.rounds[-1]
                print(previous_round)
                print(list(previous_round))
                # TODO when scores are changed, upsert a score
                # TODO When tournament is closed, remove field score_tournament{id} 
                score_field = f'score_tournament_{tournament_id}'
                return [player.doc_id for player in sorted(entrants, key = lambda x: (x[score_field], x['ranking']))]
            else:
                message = (f'Cannot sort by {by}. Please sort by \'score\', \'ranking\' or \'name\' instead.')
                self.view.print_alert(message)
        except TypeError: 
            self.view.print_alert("Le classement doit être un entier positif. Veuillez vérifier les données des joueurs.")
            return TournamentMenuController(self.current_tournament)

    def pair_players(self, players_and_scores_list):
        """Generates pairs of players for the next round
        
        Args:
            - score_list : A list of lists containing players and scores """
        
        list_of_matchs = []

        if self.current_tournament.rounds == []:
            players_and_scores_list = [[player,0] for player in players_and_scores_list]            
            half = int(PLAYERS_PER_TOURNAMENT/2)
            # Making special pairs for first round
            highest_half = players_and_scores_list[:half]
            lowest_half = players_and_scores_list[half:]
            
            for position in range(len(highest_half)):
                match = Match(([highest_half[position], lowest_half[position]]))
                list_of_matchs.append(match)

        else:
            pass
            # 'normal' pairing : 
            # 1 with 2, 3 with 4
            # EXCEPT if 1 as already met 2            
                
        return list_of_matchs
    
    def update_round_results(self, round):
        # self.view.print_alert(f"Updating {round.name}")
        # TODO ajouter un except si le round est le premier
        match_list = []
        for match in round.matchs:
            match_list.append(Match(self.update_match_results(match)))
        return match_list

    def update_match_results(self, match):
        print(match)
        p1_id = match[0][0]
        p2_id = match[1][0]
        score1 = float(input(f"Score du joueur {p1_id} : "))
        score2 = float(input(f"Score du joueur {p2_id} : "))
        if score1 + score2 == 1:
            new_match = ([p1_id, score1], [p2_id, score2])
            return new_match
        else:
            return None

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

def unserialize_object(serialized_object, type):
    try:
        if type.lower() == "players":
            object = Player(*serialized_object.values())
        elif type.lower() == "tournaments":
            object = Tournament(*serialized_object.values())
            # print(object.rounds)
            for round_number in range(len(object.rounds)):
                # print(round_number)
                round_as_dict = object.rounds[round_number]
                # print(round_as_dict)
                object.rounds[round_number] = Round(*round_as_dict.values())
                # print(object.rounds)
            # print(object.rounds)
        else:
            error = f"Provided type '{type}'' is not a valid database table."
            raise error
        return object
    except AttributeError:
        error_message = "Object provided is not valid."
        return None