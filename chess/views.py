# from chess.models import Player, Tournament

# classe abstraite "view" et sous-classes "main_menu", "adding player", etc ?
# class view

from os import stat


class BaseView():
    @staticmethod
    def render():
        print("stuff")

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

    def print_alert(self, info_text):
        print(info_text)
        self.press_any_key()

    def press_any_key(self):
        input("Presser 'Entrée' pour retourner à la selection.")


class HomeView(BaseView):
    """View of the main menu."""

    @staticmethod
    def render():
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

    # def print_tournaments(self, tournaments_list):
    #     """Prints all current and past players in db."""
    #     for tournament in tournaments_list:
    #         print(tournament)

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

    @staticmethod
    def render():
        print(
            "1. Lister les joueurs présents dans la base de données.\n"
            "2. Ajouter un joueur à la base de données.\n"
            "3. Mettre à jour les données d'un joueur.\n"
            "0. Retour au menu principal.\n"
            "9. Quitter le programme.\n"
        )

    def print_players(self, unserialized_players_list):
        # print(unserialized_players_list)
        """Prints all current and past players in db."""
        for player in unserialized_players_list:
            print(f'- {player["first_name"]}')

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

    # def print_confirmation_added_player():
    #     return 

    def print_homonyme(self, inputted_data, homonymes_list):
        print(
            "Vous souhaitez ajouter:\n"
            f"      {inputted_data[0]} {inputted_data[1]} ({inputted_data[2]}), né.e le {inputted_data[3]} et classé {inputted_data[4]}.\n"
            "La base de données contient déjà une ou des entrées similaires:"
        )
        for homonyme in homonymes_list:
            print(f"      {homonyme['first_name']} {homonyme['last_name']} ({homonyme['gender']}), né.e le {homonyme['birth_date']} et classé {homonyme['ranking']}.\n")
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


class ReportMenu(BaseView):

    @staticmethod
    def render():
        print(         
            "2. Liste de tous les tournois.\n"

            "0. Retour au menu principal.\n"
            "9. Quitter le programme.\n"
        )

class EndView:
    """Vue responsable de l'affichage de menu de fin d'application."""

    def render(self):
        print("Voulez-vous vraiment quitter l'application ?")

    def confirm_exit(self):
        return input("Sûr (Y/N) ? ")

    def notify_invalid_choice(self):
        print("Choix non valable !\n\n")

        
# FUNCTIONS TO REWORK
def print_tournament_rounds(tournament):
    print(tournament.rounds)

def print_tournament_match(tournament):
    print(tournament.matchs)

def print_tournaments(tournament):
    """ Prints all infos on a tournament. """
    print('---')

    list_tournament_players(tournament)
    
    for turn in range(1,tournament.turn+1):
        print('Tour', turn, ":")
        print('     ',tournament.generate_pairs())