from tournament.models.players import Player, players_database
from tournament.models.tournament import Tournament


def main_menu():
    """Main menu, displayed upon launching the script. 
    Called by main.py. 
    """
    print('|=================|\n| ~ BIENVENUE ! ~ |\n|=================|')
    print('Vous êtes au menu principal. Voici vos options:')
    print('1. Ajouter un.e joueuse à la base de données.')
    print('2. Créer un tournoi dans la base de données')
    print('3. Ajouter un participant au tournoi.')
    # print('4. Lancer le tournoi ou reprendre un tournoi en cours.')    
    print('10. Quitter')
    opt = input('\nQue souhaitez-vous faire ?')

    def browse(answer):
        switcher = {
            # TODO : add a default which does nothing
            1: create_player(),
            # 2: create_tournament(),
            # 3: tournament.add_player(),
            10: exit()
        }
        return switcher.get([answer], '')

    browse(opt)


def create_player():
    """ Adding a player to database """
    print('---')
    print('Ajout d\'un nouveau joueur !')

    first_name = input('Prénom :')
    last_name = input('Nom de famille :')
    genre = input("Genre ('F','M','X'\) :")
    birth_year = input('Année de naissance (4 chiffres) :')
    rating = input('Classement (if any, leave blank sinon) :')
    Player(first_name, last_name, birth_year, genre, rating).add_to_database()

    print('1. Ajouter une nouvelle personne.')
    print('2. Retour au menu principal')
    opt = input('\nQue souhaitez-vous faire ?')


def list_tournament_players(tournament, sort_by = 'rating'):
    """Lists players partaking in a tournament.

    Args:
    - sort_by : the method by which to sort the players. Can be 'name' or default, 'rating'
    Returns :
    - a list of players, sorted by alphabetical order or rating. 
    """
    tournament.sort_players(by = sort_by)

    print(f'\nLes participant.es à {tournament.name} sont :')
    for player_id in tournament.players:
        player = players_database[player_id]
        print(f'    - {player_id}. {player} (cl. {player.rating})')


def view_tournament(tournament):
    """ Prints all infos on a tournament. """
    print('---')

    list_tournament_players(tournament)
    
    for turn in range(1,tournament.turn+1):
        print('Tour', turn, ":")
        print('     ',tournament.generate_pairs())