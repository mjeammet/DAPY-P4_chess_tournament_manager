from chess.views import EndView


class EndController:
    """Controller handling app closure."""

    def __init__(self):
        self.view = EndView()

    def run(self):
        self.view.render()
        choice = self.view.confirm_exit()
        if choice.upper() == "Y":
            exit()
        elif choice.upper() == "N":
            return "home"
        else:
            self.view.notify_invalid_choice()
            return self.run()

    def hard_stop(self):
        self.view.print_alert("\nFermeture au clavier. Au revoir !")
        return None
