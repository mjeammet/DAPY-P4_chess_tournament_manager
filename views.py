from models import Player, Tournament, PLAYERS_DATABASE


def main_menu():
    print('|=================|\n| ~ BIENVENUE ! ~ |\n|=================|')
    print('Vous êtes au menu principal. Voici vos options:')
    print('1. Ajouter un.e joueuse à la base de données.')
    print('2. Créer un tournoi dans la base de données')
    print('3. Lancer le tournoi ou reprendre un tournoi en cours.')
    print('4. Ajouter un participant au tournoi.')
    print('10. Quitter')
    opt = input('\nQue souhaitez-vous faire ?')

    switcher = {
        # TODO : add a default which does nothing
        1: create_player(),
        # 2: create_tournament(),
        # 3: tournament.add_player(),
        10: exit()
    }

def create_player():
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


def view_tournament(tournoi):
    print('---')

    print(f'Les participant.es sont :')
    for id in tournoi.players:
        player = PLAYERS_DATABASE[id]
        print(f'    - {player} ({player.rating}), avec (score) points')