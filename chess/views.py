from chess.models import tournament


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
        
    def print_header(self, title):
        print(
            "\n|========================================|\n"
            f"|\t\t{title}\t\t|\n"
            "|========================================|"
        )

    def print_alert(self, alert_text):
        print(alert_text)

    def press_enter(self):
        input("Retour au menu de sélection.")

    def id_not_found(self, id, table_name):
        print(f"Id {id} introuvable dans la table \"{table_name}\". Opération annulée.")

    def cancelled(self):
        print("Opération annulée.")

    def print_player_details(self, players_details):
        print(players_details)

    def print_tournament_details_header(self):
        print(
            "Nom\t\t\t"
            "Lieu\t"
            "Date\t"
            "Time control\t"
            "Tour joués\t"
            "Gagnant.e.s"
        )

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

class HomeView(BaseView):
    """View of the main menu."""

    def render(self):
        self.print_header("MENU PRINCIPAL")
        print(
            "1. Lister les tournois existants.\n"
            "2. Créer un tournoi.\n"
            "3. Sélectionner et jouer un tournoi.\n"
            "4. Gestion des joueurs.\n"
            "9. Quitter le programme.\n"
        )

    def print_welcome(self):
        print(
            "Tournament manager v.0.10.0.\n"
            "Read README.md."
            )

    def get_name(self):
        return input("Nom du tournoi : ")
    
    def get_location(self):
        return input("Lieu du tournoi : ")
    
    def get_date(self):
        return input("Date du tournoi : ")

    def get_time_control(self):
        return input("Type de contrôle du temps (peut être 'bullet', 'blitz' ou 'fast') : ")

    def get_description(self):
        return input("(optional) Description : ")

class PlayerHomeView(BaseView):

    def render(self):
        self.print_header("MENU DES JOUEURS")
        print(
            "1. Lister les joueurs présents dans la base de données.\n"
            "2. Ajouter un joueur à la base de données.\n"
            "3. Mettre à jour les données d'un joueur.\n"
            "0. Retour au menu principal.\n"
            "9. Quitter le programme.\n"
        )

    def get_sorting_parameter(self):
        print(
            "1. Par nom de famille\n"
            "2. Par classement"
        )
        return self.get_user_choice()


    def print_player_details(self, unserialized_players_list):
        """Prints a list of players."""
        print(
            "Prénom\t\t",
            "Nom\t\t",
            "Sexe\t\t",
            "Date de naissance\t",
            "Classement")
        for player in unserialized_players_list:
            player_line = f'{player["first_name"]}\t'
            if len(player["first_name"]) < 8:
                player_line += '\t'
            player_line += f' {player["last_name"]}\t'
            if len(player["last_name"]) < 7:
                player_line += '\t'
            player_line += f' {player["gender"]}\t\t {player["birth_date"]}\t\t {player["ranking"]}'
            print(player_line)

    def get_first_name(self):
        return input('Prénom :')
    
    def get_last_name(self):
        return input('Nom de famille :')

    def get_gender(self):
        return input("Genre ('F','M','X'\) :")
    
    def get_birth_date(self):
        return input('Année de naissance (format DD-MM-YYYY) :')

    def get_ranking(self):
        return input('Classement (entier positif) :')

    def print_duplicate_alert(self, inputted_data, duplicate_list):
        print(
            "Vous souhaitez ajouter:\n"
            f"      {inputted_data[0]} {inputted_data[1]} ({inputted_data[2]}), né.e le {inputted_data[3]} et classé {inputted_data[4]}.\n"
            "La base de données contient déjà une ou des entrées similaires:"
        )
        for duplicate in duplicate_list:
            print(f"      {duplicate['first_name']} {duplicate['last_name']} ({duplicate['gender']}), né.e le {duplicate['birth_date']} et classé {duplicate['ranking']}.\n")
        print(
            "Que souhaitez-vous faire ?\n"
            "1. Ecraser le joueur existant avec les nouvelles données.\n"
            "2. Ajouter quand même un nouveau joueur.\n"
            "3. Annuler l'ajout.\n"            
        )

class TournamentHomeView(BaseView):

    @staticmethod
    def render(current_tournament = None):
        print(
            "1. Lister les joueurs du tournoi.\n"
            "2. Ajouter un joueur au tournoi.\n"
            "---\n"
            "3. Lister les tours du tournoi.\n"
            "4. Commencer un nouveau tour de jeu.\n"
            "5. Entrer les résultats du round non terminé.\n"
            "6. Lister les matchs du tournoi.\n"
            "---\n"
            "7. Changer de tournoi sélectionné.\n"
            "0. Retour au menu principal.\n"
            "9. Quitter le programme."
        ) 

    def print_current_tournament(self, tournament_name):
        print(f'Current tournament : {tournament_name}\n')

    def print_round_header(self):
        print("Nom\t   Date_debut\t\t\t Date_fin  Match1    Match2  Match3  Match4")

    def print_round_details(self, round):
        details = (
            f'{round.name}    '    
            f'{round.start_datetime}    '
            f'{round.end_datetime}    '
            f'{str(round.matchs[0])}    '
            f'{str(round.matchs[1])}    '
            f'{str(round.matchs[2])}    '
            f'{str(round.matchs[3])}    '
        )
        print(details)
        return None

    def print_match_details(self, match):
        # print(f'{match}')
        return match

    def get_match_score(self, player_id):
        inputted_score = float(input(f"Score du joueur {player_id} : "))
        # TODO add a try except to catch les petits malins qui mettent des 
        if inputted_score not in [0, 0.5, 1]:
            print(f'Score must be 0, 1 or 0.5. Cannot be {inputted_score}')
            return self.get_match_score()
        
        return inputted_score       

class EndView(BaseView):
    """Vue responsable de l'affichage de menu de fin d'application."""

    def render(self):
        print("Voulez-vous vraiment quitter l'application ?")

    def confirm_exit(self):
        return input("Sûr (Y/N) ? ")