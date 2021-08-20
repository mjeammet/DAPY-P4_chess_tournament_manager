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

def print_header(title):
    print(
        "\n|========================================|\n"
        f"|\t\t{title}\t\t|\n"
        "|========================================|"
    )
    
class HomeViewFromExampe(BaseView):
    """View of the main menu."""

    @staticmethod
    def render():
        print_header(title = "MENU PRINCIPAL")
        print(
            "1. Gestion des joueurs.\n"
            "2. Gestion des tournois.\n"
            "3. Impression des rapports.\n"
            "4. Vider base de données\n"
            "\nQ. Quitter le programme.\n"
        )

    def print_welcome(self):
        print(
            "Tournament manager v.0.10.0.\n"
            "Read README.md."
            )

class PlayerHomeView(BaseView):

    @staticmethod
    def render():
        print_header(title = "MENU DES JOUEURS")
        print(
            "1. Ajouter un joueur à la base de données.\n"
            "2. Mettre à jour les données d'un joueur.\n"
            "0. Retour au menu principal.\n"
            "\nQ. Quitter le programme.\n"
        )

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
            f"      {inputted_data[0]} {inputted_data[1]}, né.e le {inputted_data[2]} et classé {inputted_data[3]}.\n"
            "La base de données contient déjà une ou des entrées similaires:"
        )
        for homonyme in homonymes_list:
            print(f"      {homonyme['first_name']} {homonyme['last_name']}, né.e le {homonyme['birth_date']} et classé {homonyme['ranking']}.\n")
        print(
            "Que souhaitez-vous faire ?\n"
            "1. Ecraser le joueur existant avec les nouvelles données.\n"
            "2. Ajouter quand même un nouveau joueur.\n"
            "3. Annuler l'ajout.\n"            
        )


class TournamentHomeView(BaseView):

    @staticmethod
    def render(current_tournament):
        print_header(title = "MENU DES TOURNOIS")
        print(f'Current tournament : {current_tournament}')
        print(
            "\n"
            "1. Créer un nouveau tournoi.\n"
            "2. Sélectionner un tournoi comme le tournoi actuel.\n"
            "3. Ajouter des joueurs à un tournoi.\n"
            "4. Ouvrir un round.\n"
            "5. Entrer les résultats d'un round ouvert.\n"
            "0. Retour au menu principal.\n"
            "9. Quitter le programme.\n"
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

class ReportMenu(BaseView):

    @staticmethod
    def render():
        print_header(title = "MENU DES RAPPORTS")
        print(
            "1. Liste de tous les acteurs.\n"            
            "2. Liste de tous les tournois.\n"
            "3. Liste de tous les joueurs d'un tournoi.\n"
            "4. Liste de tous les tours d'un tournoi.\n"
            "5. Liste de tous les matchs d'un tournoi.\n"
            "\n0. Retour au menu principal.\n"
            "Q. Quitter le programme.\n"
        )

    @staticmethod
    def print_players(unserialized_players_list):
        # print(unserialized_players_list)
        """Prints all current and past players in db."""
        for player in unserialized_players_list:
            print(f'- {player["first_name"]}')

    @staticmethod
    def print_tournaments(tournaments_list):
        """Prints all current and past players in db."""
        for tournament in tournaments_list:
            print(tournament)


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