import re 

from tinydb import Query

from chess import views
from ..models import Database, Player

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
            return "home"
        elif next_action == "9":
            return None
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
