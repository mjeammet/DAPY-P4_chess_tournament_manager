import re
from datetime import date, datetime
from tinydb import Query
from chess import views
from chess.models import Player, Tournament, Round, Match, Database
from chess.models import PLAYERS_PER_TOURNAMENT, ROUNDS_PER_TOURNAMENT, TIME_CONTROL_TYPE
VERBOSE = False


class ApplicationController:
    """Controller for the app itself."""

    def __init__(self):
        self.current_controller = HomeController()

    def start(self):
        """Starts the app and handle keyboard interruptions."""
        self.current_controller.view.print_welcome()

        try:
            while self.current_controller is not None:
                next_controller = self.current_controller.run()
                self.current_controller = next_controller
        except KeyboardInterrupt:
            self.view = views.EndView()
            self.view.print_alert("\nFermeture au clavier. Ciao !")


class HomeController:
    """Controller for Home menu."""
    def __init__(self):
        self.view = views.HomeView()
        self.database = Database()

    def run(self):
        """Run controller."""
        self.view.render()

        next_action = self.view.get_user_choice()
        if next_action == "1":
            # Displays all tournaments
            self.show_tournaments_details()
            self.view.press_enter()
            return self.run()
        elif next_action == "2":
            # Creation of a new tournament
            new_tournament_infos = self.get_new_tournament_info()
            new_tournament = Tournament(*new_tournament_infos)

            self.add_new_tournament_to_database(new_tournament)
            self.view.press_enter()
            return self.run()
        elif next_action == "3":
            return TournamentMenuController()
        elif next_action == '4':
            return PlayerMenuController()
        elif next_action == "9":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return self.run()

    def show_tournaments_details(self):
        tournaments_list = self.database.tournaments_table.all()
        self.view.print_tournament_details_header()
        if len(tournaments_list) == 0:
            self.view.print_alert("Aucun tournoi à afficher.")
        else:            
            for tournament in tournaments_list:
                self.view.print_tournament_details(tournament)
        return None

    def get_new_tournament_info(self):
        """Get all infos to create a new tournament object.
        Args:
            - None
        Returns:
            - A list containing collected data"""
        # TODO récupérer la liste des champs avec "signature(Tournament)" ?
        name = self.get_valid_tournament_name()
        location = self.get_valid_location()
        date = self.get_valid_date()
        time_control = self.view.get_time_control()
        description = self.view.get_description()
        return [name, location, date, [], {}, time_control, description]

    def get_valid_tournament_name(self):
        return self.view.get_name()
    
    def get_valid_location(self):
        return self.view.get_location()

    def get_valid_date(self):
        return self.view.get_date()
    
    def get_valid_time_control(self):
        time_control = self.view.get_time_control()
        if time_control in TIME_CONTROL_TYPE:
            return time_control
        else:
            self.view.print_alert("Time control doit être \"bullet\" ou \"blitz\" ou \"rapide\"")

    def add_new_tournament_to_database(self, tournament):
        """Add a new tournament to the database.
        Args:
            - Informations of new tournament
        Returns:
            - database id of the new tournament"""
        table_name = "tournaments"
        tournament_id = self.database.add_to_database(table_name, tournament)
        alert = f'---\n{tournament.name} ajouté.e à la base de données avec l\'id {tournament_id}.'
        self.view.print_alert(alert)
        return None


class PlayerMenuController:
    """Controller for Player menu."""
    def __init__(self):
        self.view = views.PlayerHomeView()
        self.database = Database()

    def run(self):
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == '1':
            # Lists all players in database
            all_players = self.database.players_table.all()
            self.list_players(all_players)
            self.view.press_enter()
            return self.run()
        elif next_action == '2':
            # Create new player and add them to the database
            new_player = self.create_new_player()
            new_player_id = self.database.add_to_database("players", new_player)
            self.view.print_alert(f'---\n{new_player.first_name} {new_player.last_name} succesfully added with id {new_player_id}.')
            self.view.press_enter
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
            return self.run()

    def list_players(self, players_list):
        """Lists players."""
        sorting_parameter = self.view.get_sorting_parameter()
        if sorting_parameter == "1":
            sorted_list = sorted(players_list, key = lambda x:x['last_name'])
            self.view.print_player_details(sorted_list)
        elif sorting_parameter == "2":
            sorted_list = sorted(players_list, key = lambda x:x['ranking'], reverse=True)
            self.view.print_player_details(sorted_list)
        else:
            self.view.notify_invalid_choice()        
        return None

    def get_new_player_info(self):
        """Collects player info from the user."""
        self.view.print_alert("Ajout d'un nouveau participant.")
        # Collecting player info
        first_name = self.get_valid_first_name()
        last_name = self.get_valid_last_name()
        if first_name is None or last_name is None:
            self.view.cancelled()
            return None
        birth_date = self.get_valid_birth_date()
        gender = self.get_valid_gender()
        ranking = self.get_valid_ranking()
        return [first_name, last_name, birth_date, gender, ranking]

    def get_valid_first_name(self):
        """Get valid first_name from user.
        Args:
            - None
        Returns:
            - a validated string."""
        inputted_name = self.view.get_first_name()
        if inputted_name == "":
            return None
        elif re.fullmatch("[A-Za-z\-]*", inputted_name): 
            return inputted_name
        else:
            self.view.print_alert("Le prénom ne peut pas être vide et doit être uniquement constitué de lettres.")
            return self.get_valid_first_name()
    
    def get_valid_last_name(self):
        """Get valid last_name from user.
        Args:
            - None
        Returns:
            - a validated string."""
        inputted_name = self.view.get_last_name()
        if inputted_name == "":
            return None
        elif re.fullmatch("[A-Za-z\s]*", inputted_name): 
            return inputted_name
        else:
            self.view.print_alert("Le nom de famille doit être uniquement constitué de lettres (ou de \"-\").")
            return self.get_valid_last_name()

    def get_valid_gender(self):
        inputted_gender = self.view.get_gender()
        if inputted_gender.upper() in ['F', 'M', 'X']:
            self.view.print_alert("Le genre doit être 'F', 'M' or 'X'.")
            return inputted_gender
        else:
            return self.get_valid_gender()
    
    def get_valid_birth_date(self):
        inputted_date = self.view.get_birth_date()
        listed_input = inputted_date.split("-")
        try: 
            date(int(listed_input[2]), int(listed_input[1]), int(listed_input[0]))
            return 
        except IndexError: 
            self.view.print_alert("La date de nasisance doit être au format DD-MM-YYYY.")
            return self.get_valid_birth_date()
        except ValueError:
            self.view.print_alert("La date de nasisance doit être au format DD-MM-YYYY.")
            return self.get_valid_birth_date()

    def get_valid_ranking(self):
        """Prompt user for player ranking and validate data.        
        Returns:
            - An integer, for player ranking."""
        inputted_ranking = self.view.get_ranking()
        try:
            return int(inputted_ranking)
        except ValueError:
            self.view.type_error("integer")
            return self.get_valid_ranking()

    def get_valid_player_id(self):
        inputted_id = self.view.get_player_id()
        try:
            return int(inputted_id)
        except ValueError:
            self.view.type_error("integer")
            return self.get_valid_player_id()

    def check_existing_duplicate(self, new_player_info):
        """From inputted player info, check for duplicate in the database."""
        first_name = new_player_info[0]
        last_name = new_player_info[1]
        return self.database.players_table.search(
            (Query().first_name == first_name) & (Query().last_name == last_name))
    
    def create_new_player(self):
        """Add a player to the database.
        Returns:
            - A new instance of Player class
        """
        new_player_data = self.get_new_player_info()            
        existing_duplicate = self.check_existing_duplicate(new_player_data)
        # TODO transformer en une fonction search_player() qui servira aussi à aller update les infos du player
        if existing_duplicate != []:
            self.view.print_duplicate_alert(new_player_data, existing_duplicate)
            next_action = self.view.get_user_choice()
            if next_action == '1':
                self.update_player_infos()
            elif next_action == "2":
                self.add_player_to_database(new_player_data)
            elif next_action == "3":
                self.view.cancelled()
            else:
                self.view.notify_invalid_choice()
        else:
            new_player = Player(*new_player_data)
        return new_player

    def update_player_infos(self, player_id="", first_name="", last_name="", gender="", birth_date="", ranking=""):
        """Update a player in the database."""
        player_id = self.get_valid_player_id()
        existing_player = self.database.get_db_object(player_id, "players")

        self.view.print_player_details([existing_player])
        

        next_action = self.view.get_player_field_to_modify()
        # TODO convert to dictionary, please 
        if next_action == "1":
            updated_field = "first_name"
        elif next_action == "2":
            updated_field = "last_name"
        elif next_action == "3": 
            updated_field = "birth_date"
        elif next_action == "4":
            updated_field = "gender"
        elif next_action == "5":
            updated_field = "ranking"                
        else:
            self.view.notify_invalid_choice()
            self.view.press_enter()
            return self.run()
        updated_info = self.view.get_updated_info()
        self.database.players_table.update({updated_field: updated_info}, doc_ids = [player_id])


class TournamentMenuController:
    """Controller for Tournament menu."""
    def __init__(self):
        self.view = views.TournamentHomeView()
        self.current_tournament = None
        self.database = Database()

    def run(self):
        self.view.render(self.current_tournament)
        next_action = self.view.get_user_choice()
        if next_action in ["2","3","4","5","6","7"]:
            if self.current_tournament == None:
                self.current_tournament = self.select_current_tournament()
        if next_action == "1":
            # Change selected tournament
            self.current_tournament = self.select_current_tournament()
            return self.run()
        if next_action == "2":
            # Selected add players to tournament        
            if len(self.current_tournament.players) >= PLAYERS_PER_TOURNAMENT:
                alert = "Le tournoi est déjà plein, vous ne pouvez pas ajouter de participant.es."
                self.view.print_alert(alert)
            else:
                while len(self.current_tournament.players) != 8:
                    self.add_player_to_tournament()

                # notifies if it was the last player
                self.view.print_alert("8ème participant.e ajouté.e au tournoi. Le tournoi est désormais plein ! ")

            self.view.press_enter()
            return self.run()
        elif next_action == "3":
            # Selected "New round"

            if self.check_ready_for_new_round():
                new_round = self.create_new_round()
                self.current_tournament.rounds.append(new_round)

                # Creating round in database
                serialized_rounds = [round.serialize() for round in self.current_tournament.rounds]
                self.database.tournaments_table.update({"rounds": serialized_rounds}, Query().name == self.current_tournament.name)
            else:
                self.view.print_alert("Le tour précédent attend encore des résultats.")
            
            self.view.press_enter()
            return self.run()        
        elif next_action == "4":
            # Updatting round

            # TODO check if last round is finished. 
            round_to_update = self.current_tournament.rounds[-1]
            for match_to_update in round_to_update.matchs:
                # print(match_to_update)
                self.view.print_alert(f"Updating match {match_to_update[0][0]} contre {match_to_update[1][0]}")
                match_index = round_to_update.matchs.index(match_to_update)

                new_match = self.get_updated_match(match_to_update)
                self.current_tournament.rounds[-1].matchs[match_index] = new_match
                self.current_tournament.rounds[-1].end_datetime = str(datetime.today())

                # Updating players scores
                self.current_tournament.players[str(new_match[0][0])] += new_match[0][1]
                self.current_tournament.players[str(new_match[1][0])] += new_match[1][1]

            
            self.view.print_round_ended(self.current_tournament.rounds[-1])
            # Updating database
            self.update_rounds_in_database()
            self.update_players_in_database()

            self.view.press_enter()
            return self.run()
        elif next_action == "5":
            # Browse and print entrants infos
            entrants_infos = [] 
            for player_id in self.current_tournament.players.keys():
                entrants_infos.append(self.database.players_table.get(doc_id = int(player_id)))

            self.list_players(entrants_infos)
            self.view.press_enter()
            return self.run()
        elif next_action == "6":
            # Selected "prints rounds"

            # Prints header and round infos
            self.show_rounds_details()            

            self.view.press_enter()
            return self.run()
        elif next_action == "7":
            # List matches
            for round in self.current_tournament.rounds:
                self.view.print_alert(round.matchs)
            
            self.view.press_enter()
            return self.run()
        elif next_action == "0":
            return HomeController()
        elif next_action == "9":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return self.run()

    def show_rounds_details(self):
        if len(self.current_tournament.rounds) > 0:
                self.view.print_round_header()
                for round in self.current_tournament.rounds:
                    self.view.print_round_details(round)
        else: 
            self.view.print_alert("Aucun round à afficher.")

    # TODO 
    def list_players(self, entrants_infos):
        return PlayerMenuController.list_players(self, entrants_infos)

    def get_valid_player_id(self):
        return PlayerMenuController.get_valid_player_id(self)

    def update_players_in_database(self):
        """Update players dictionary in the database"""
        # self.view.print_alert(self.current_tournament.players)
        self.database.tournaments_table.update({"players": self.current_tournament.players}, Query().name == self.current_tournament.name)

    def update_rounds_in_database(self):
        serialized_rounds = [round.serialize() for round in self.current_tournament.rounds]
        self.database.tournaments_table.update({"rounds": serialized_rounds}, Query().name == self.current_tournament.name)

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
            self.view.id_not_found(inputted_id, "tournaments")
            return None
        
        #unserialize_tournament()
        tournament = self.unserialize_object(serialized_tournament, type="tournaments")
        name = tournament.name
        self.view.print_alert(f"Tournoi {name} sélectionné comme tournoi en cours.")
        return tournament

    def get_current_tournament_object(self):
        pass 
        
    def add_player_to_tournament(self):
        """ Add a player to tournament, using their id. """
     
        player_id = self.get_valid_player_id()
        
        # Check if player is not already registered in tournament
        if len(self.current_tournament.players) > 0:
            if str(player_id) in self.current_tournament.players.keys():
                self.view.print_alert("Player already in tournament.")
                return None

        # Making sure que le player est bien dans la DB
        db_match = self.database.players_table.get(doc_id = player_id)
        if db_match is not None:
            self.current_tournament.players[str(player_id)] = 0
            self.database.tournaments_table.update({"players": self.current_tournament.players}, Query().name == self.current_tournament.name)  
            self.view.print_alert("Joueur ajouté.")
        else:
            self.view.id_not_found(player_id, "players")

    def create_new_round(self):   
        """Creates a new round for current tournament. """
        round_number = int(len(self.current_tournament.rounds))+1

        if round_number == 1:
            # first round, players order is based on ranking 
            # and 1 meets 4, 2 meets 5, etc
            players_order = self.sort_players(self.current_tournament.players, by = 'ranking')
        else:
            players_order = self.sort_players(self.current_tournament.players, by = 'score')
    
        paired_players = self.pair_players(players_order, round_number)
   
        new_round_matchs = []
        for pair in paired_players:
            new_match = Match(([pair[0], 0], [pair[1], 0]))
            new_round_matchs.append(new_match)

        # New round infos
        round_name = f'Round {round_number}'
        round_starttime = str(datetime.today())
        round_endtime = None
        
        new_round = Round(round_name, round_starttime, round_endtime, new_round_matchs)
        self.view.print_alert(f'{new_round.name} créé le {new_round.start_datetime}.')
        return new_round 

    def check_ready_for_new_round(self):

        if len(self.current_tournament.rounds) > 0:
            for match in self.current_tournament.rounds[-1].matchs:
                if match[0][1] == 0 and match[1][1] == 0:
                    return False

        if len(self.current_tournament.players) != PLAYERS_PER_TOURNAMENT:
            error_message = (
                "Le round ne peut pas commencer car le nombre de joueurs est incorrect."
                f"Actuellement {len(self.current_tournament.players)} joueurs au lieu de {PLAYERS_PER_TOURNAMENT}.")
            self.view.print_alert(error_message)
            return False
        elif len(self.current_tournament.rounds) >= ROUNDS_PER_TOURNAMENT:
            error_message = f"Le nombre de tour par tournoi ne peut pas excéder {ROUNDS_PER_TOURNAMENT} (voir \"settings.py\")."
            self.view.print_alert(error_message)
            return False
        else:
            return True

    def sort_players(self, entrants_list, by = 'score'):
        """ Sorts player to generate pairs according to the swiss tournament pattern.         
        Args:
            - a list of players
            - by -- the parameter by which players will be sorted. Can be 'score' or 'ranking'
        Returns:
        - a sorted list of players' ids
        """
        
        # filters the database to only get this tournament's entrants
        entrants_infos = []
        for entrants_id in entrants_list.keys():
            # extract player infos from the database and add score
            players_infos = self.database.players_table.get(doc_id = int(entrants_id))
            players_infos["score"] = int(self.current_tournament.players[str(entrants_id)])
            entrants_infos.append(players_infos)

        if by == "ranking":
            return [player.doc_id for player in sorted(entrants_infos, key = lambda x:x['ranking'], reverse=True)]
        elif by == 'name':
            return [player.doc_id for player in sorted(entrants_infos, key = lambda x:x['last_name'])]
        elif by == 'score':
            return [player.doc_id for player in sorted(entrants_infos, key = lambda x: (x['score'], x['ranking']), reverse=True)]
        else:
            message = (f'Cannot sort by {by}. Please sort by \'score\', \'ranking\' or \'name\' instead.')
            self.view.print_alert(message)

    def pair_players(self, players_ordered_list, round_number):
        """Pairs players together from player list.
        
        Args: 
            - An ordered list of players_ids

        Returns:
            - A list of this round's pairs """
        pair_list = []

        if round_number == 1:
            # Pairs weirdly : 1 with 5, 2 with 6, etc
            half = int(PLAYERS_PER_TOURNAMENT/2)
            # Making special pairs for first round
            highest_half = players_ordered_list[:half]
            lowest_half = players_ordered_list[half:]
            
            for position in range(len(highest_half)):
                duo = ([highest_half[position], lowest_half[position]])
                pair_list.append(duo)
        elif round_number > 1:
            # Pairs from top to bottom, avoiding matching players who already played together
            players_left_to_match = players_ordered_list 
            while players_left_to_match != []:
                p1_id = players_left_to_match[0]
                p2_id = self.first_unmet_partner(p1_id, players_left_to_match[1:])
                duo = (p1_id, p2_id)
                pair_list.append(duo)
                players_left_to_match.remove(p1_id)
                players_left_to_match.remove(p2_id)

        return pair_list

    def first_unmet_partner(self, player_to_match, list_of_candidates):        
        met_players = self.get_previously_met_players(player_to_match)
        # print(f"    Matching for {player_to_match}, who already met {met_players}")
        for candidate in list_of_candidates:
            if candidate not in met_players:
                return candidate
        
        # if we run out of candidates AKA player_to_match already met everyone
        return list_of_candidates[0]

    def get_previously_met_players(self, player_id):
        """Browse previous rounds to find past opponents.
        Arguments:
            - A player's id
        Returns:
            - A list of past opponents ids"""
        met_players = []
        for past_round in self.current_tournament.rounds:
            for past_match in past_round.matchs:
                if player_id == past_match[0][0]:
                    met_players.append(past_match[1][0])
                elif player_id == past_match[1][0]:
                    met_players.append(past_match[0][0])
                else:
                    pass 
        return met_players

    def get_updated_match(self, match):
        p1_id = match[0][0]
        p2_id = match[1][0]
        score1 = self.view.get_match_score(p1_id)
        score2 = self.view.get_match_score(p2_id)
        if score1 + score2 == 1:
            new_match = Match(([p1_id, score1], [p2_id, score2]))
            return new_match
        else:
            return None

    def unserialize_object(self, serialized_object, type):
        try:
            if type.lower() == "players":
                object = Player(*serialized_object.values())
            elif type.lower() == "tournaments":
                object = Tournament(*serialized_object.values())
            else:
                error = f"Provided type '{type}'' is not a valid database table."
                raise error
            return object
        except AttributeError:
            error_message = "Object provided is not valid."
            self.view.print_alert(error_message)
            return None


class EndController:
    """Controller handling app closure."""

    def __init__(self):
        self.view = views.EndView()

    def run(self):
        self.view.render()
        choice = self.view.confirm_exit()
        if choice.upper() == "Y":
            return None
        elif choice.upper() == "N":
            return HomeController()
        else:
            self.view.notify_invalid_choice()
            return self.run()
