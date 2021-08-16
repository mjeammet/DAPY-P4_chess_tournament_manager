# from chess.models import Player, Tournament

# classe abstraite "view" et sous-classes "main_menu", "adding player", etc ?
# class view

from chess.database import get_database_table
from tinydb import Query


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

class HomeViewFromExampe(BaseView):
    """View of the main menu."""

    @staticmethod
    def render():
        print(
            "Menu d'accueil\n"
            "==============\n"
            "1. Ajouter un.e joueuse à la base de données.\n"
            "2. Créer un tournoi dans la base de données\n"
            "3. Ajouter un participant au tournoi.\n"
            "4. Lancer le tournoi ou reprendre un tournoi en cours.\n"
            "5. Afficher rapports.\n"
            "6. Vider base de données\n"
            "\n0. Quitter le programme.\n"
        )

class NewPlayerView(BaseView):
    """ Adding a player to database """
    @staticmethod
    def render():   
        print(
            "---\n"
            "1. Ajouter une nouvelle personne.\n"
            "2. Retour au menu principal.\n"        
        )
    
    def get_new_player_info(self):
        print("Veuillez ajouter les informations du nouveau participant.")
        first_name = input('Prénom :')
        last_name = input('Nom de famille :')
        gender = input("Genre ('F','M','X'\) :")
        birth_year = input('Année de naissance (4 chiffres) :')
        ranking = input('Classement (if any, leave blank sinon) :')
        return [first_name, last_name, birth_year, gender, ranking]

class NewTournamentView(BaseView):

    @staticmethod
    def render():
        print(
            "1. Launch new tournament.\n"
            "2. Retour au menu principal.\n"
            "3. Quitter.\n"
        )

class ReportMenu(BaseView):

    @staticmethod
    def render():
        print(
            "----------\n"
            "1. Liste de tous les acteurs.\n"            
            "2. Liste de tous les tournois.\n"
            "3. Liste de tous les joueurs d'un tournoi.\n"
            "4. Liste de tous les tours d'un tournoi.\n"
            "5. Liste de tous les matchs d'un tournoi.\n"
            "\n0. Retour au menu principal.\n"
            "Q. Quitter le programme.\n"
        )

    @staticmethod
    def print_players(player_list):
        """Prints all current and past players in db."""
        for player in player_list:
            print(player)

    def prints_entrants(self, tournament_id, sort_by = "ranking"):
        """Prints players partaking in a tournament.

        Args:
        - sort_by : the method by which to sort the players. Can be 'name' or default, 'ranking'
        Returns nothing
        """
        players_db = get_database_table("players")
        
        # selected_tournament["players"].sort_players(by = sort_by)
        # print(players_db)

        # print(players_db.search(Query().id.one_of(list(selected_tournament["players"])))) # makes another list so, quite ugly       
        for entrant_id in selected_tournament["players"]:
            player = players_db.search(Query().id == int(entrant_id))
            print(player)
            print(f'    - {entrant_id}. {player["first_name"]} ')
            # print(f'cl. {player["ranking"]})')        


def print_tournament_turn(tournament):
    print(tournament.turns)



def print_tournaments(tournament):
    """ Prints all infos on a tournament. """
    print('---')

    list_tournament_players(tournament)
    
    for turn in range(1,tournament.turn+1):
        print('Tour', turn, ":")
        print('     ',tournament.generate_pairs())


