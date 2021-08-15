from chess.models import Player, Tournament

# classe abstraite "view" et sous-classes "main_menu", "adding player", etc ?
# class view

class BaseView():
    @staticmethod
    def render():
        print("stuff")

    def get_user_choice(self):
        return input('\nQue souhaitez-vous faire ?').lower()

    def notify_invalid_choice(self):
        print("Choix non valable!")

class HomeViewFromExampe(BaseView):
    """View of the main menu."""

    @staticmethod
    def render():
        print(
            "Menu d'accueil\n"
            "==============\n"
            "1. Ajouter un.e joueuse à la base de données.\n"
            "2. Créer un tournoi dans la base de données\n"
            "3. Lancer le tournoi ou reprendre un tournoi en cours.\n"
            "4. Ajouter un participant au tournoi.\n"
            "5. Quitter le programme."
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
        print('Ajout d\'un nouveau joueur !')


def print_tournament_players(tournament, sort_by = 'ranking'):
    """Prints players partaking in a tournament.

    Args:
    - sort_by : the method by which to sort the players. Can be 'name' or default, 'ranking'
    Returns nothing
    """
    tournament.sort_players(by = sort_by)

    print(f'\nLes participant.es à {tournament.name} sont :')
    for player_id in tournament.players:
        player = players_database[player_id]
        print(f'    - {player_id}. {player} (cl. {player.ranking})')


def print_tournament_turn(tournament):
    print(tournament.turns)



def view_tournament(tournament):
    """ Prints all infos on a tournament. """
    print('---')

    list_tournament_players(tournament)
    
    for turn in range(1,tournament.turn+1):
        print('Tour', turn, ":")
        print('     ',tournament.generate_pairs())

def print_all_players():
    """Prints all current and past players in db."""
    for player in db:
        print(player)