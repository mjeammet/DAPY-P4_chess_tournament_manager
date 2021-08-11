from chess.models import Player, Tournament, players_database

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
    ranking = input('Classement (if any, leave blank sinon) :')
    Player(first_name, last_name, birth_year, genre, ranking).add_to_database()

    print('1. Ajouter une nouvelle personne.')
    print('2. Retour au menu principal')
    opt = input('\nQue souhaitez-vous faire ?')


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