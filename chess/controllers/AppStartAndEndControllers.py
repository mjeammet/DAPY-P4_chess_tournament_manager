
from chess import views
from .PlayerController import PlayerMenuController
from .HomeController import HomeController
from .TournamentMenuController import TournamentMenuController

class ApplicationController:
    """Controller for the app itself."""

    def __init__(self):
        self.current_controller = HomeController()
        self.home = HomeController()
        self.players_menu = PlayerMenuController()
        self.tournament_handling_menu = TournamentMenuController()
        self.end_controller = EndController()

    def start(self):
        """Starts the app and handle keyboard interruptions."""
        self.current_controller.view.print_welcome()

        try:
            while self.current_controller is not None:
                next_controller = self.current_controller.run()
                if next_controller == "home":
                    self.current_controller = self.home
                elif next_controller == "players_menu":
                    self.current_controller = self.players_menu
                elif next_controller == "tournament_menu": 
                    self.current_controller = self.tournament_handling_menu
                else:
                    self.current_controller = self.end_controller
        except KeyboardInterrupt:
            self.current_controller = self.end_controller.hard_stop()


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
            return "home"
        else:
            self.view.notify_invalid_choice()
            return self.run()

    def hard_stop(self):
        self.view.print_alert("\nFermeture au clavier. Au revoir !")
        return None