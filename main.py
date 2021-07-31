from views import main_menu, view_tournament
from models import Player, Tournament, PLAYERS_PER_TOURNAMENT, PLAYERS_DATABASE
DEBUG = True

def development():
    player1 = Player("Pupo", "Marie", "1990", "F", 0).add_to_database()
    player2 = Player("Bet", "Gexo", "1999", "X", 5).add_to_database()
    player3 = Player('Pupo', 'José Leodan', "1947", "M", 0).add_to_database()
    player4 = Player('Pupo', 'Yina', "2001", "F", 6).add_to_database()
    player5 = Player("Pupo", "Gwendy", "1990", "F", 3).add_to_database()
    player6 = Player("Pupo", "Enzo", "1980", "F", 1).add_to_database()
    player7 = Player('King', 'Stephen', "1947", "M", 0).add_to_database()
    player8 = Player('Pupo', 'Anita', "2001", "F", 0).add_to_database()
    print(f'Database now has {len(PLAYERS_DATABASE)} players.')

    tournoi = Tournament()
    tournoi.add_players([0,1,2,3,4,5,6,7])
    
    # first tour
    # tournoi.sort_players()



    # val = input("Enter your value: ")
    # print(val)

    view_tournament(tournoi)

if __name__ == '__main__' :
    development()
    # main_menu()
