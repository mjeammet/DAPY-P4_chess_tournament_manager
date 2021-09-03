from chess import views
from ..models import Tournament, Database, TIME_CONTROL_TYPE

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
            return "tournament_menu"
        elif next_action == '4':
            return "players_menu"
        elif next_action == "9":
            return None
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