class BaseView():
    @staticmethod
    def render():
        print("")

    def get_user_choice(self):
        return input('\nQue souhaitez-vous faire ? ').lower()

    def notify_invalid_choice(self):
        print("Choix non valable!")

    def get_user_tournament_choice(self):
        return input('\nVeuillez entrer l\'id d\'un tournoi existant ? ')

    @staticmethod
    def print_header(title):
        bars = "|==========" + "=" * len(title) + "==========|"
        print(
            f"\n{bars}\n"
            f"|          {title}          |\n"
            f"{bars}"
        )

    def print_alert(self, alert_text):
        print(alert_text)

    def print_player_details(self, unserialized_players_list):
        """Prints a list of players."""
        print(
            "Prénom\t\t",
            "Nom\t\t",
            "Sexe\t\t",
            "Date de naissance\t",
            "Classement")
        if unserialized_players_list == []:
            print("- Aucun joueur à afficher -")
        else:
            for player in unserialized_players_list:
                player_line = f'{player["first_name"]}\t'
                if len(player["first_name"]) < 8:
                    player_line += '\t'
                player_line += f' {player["last_name"]}\t'
                if len(player["last_name"]) < 7:
                    player_line += '\t'
                player_line += f' {player["gender"]}\t\t {player["birth_date"]}\t\t {player["ranking"]}'
                print(player_line)
        return None

    def press_enter(self):
        input("Retour au menu de sélection.")

    def id_not_found(self, id, table_name):
        print(f"Id {id} introuvable dans la table \"{table_name}\". Opération annulée.")

    def cancelled(self):
        print("Opération annulée.")

    def print_tournament_details_header(self):
        print(
            "Nom\t\t\t"
            "Lieu\t"
            "Date\t"
            "Time control\t"
            "Tour joués\t"
            "Gagnant.e.s"
        )

    def get_sorting_parameter(self):
        print(
            "1. Par nom de famille\n"
            "2. Par classement"
        )
        return self.get_user_choice()

    @staticmethod
    def get_player_id():
        return input("Id du joueur : ")

    def print_tournament_details(self, tournament_details):
        # print(tournament_details)
        print(
            f"{tournament_details['name']}\t"
            f"{tournament_details['location']}\t"
            f"{tournament_details['date']}\t"
            f"{tournament_details['time_control']}\t"
            f"{len(tournament_details['rounds'])}\t"
            "-"
        )

    def type_error(self, type):
        print(f"Doit être de type {type}.")