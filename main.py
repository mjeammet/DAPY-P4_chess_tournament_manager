from tournament.models import Player, players_database 
from tournament.models.tournament import Tournament, PLAYERS_PER_TOURNAMENT
from tournament.views import main_menu, view_tournament

DEBUG = True

def development():
    player1 = Player("Marie", "Pupo", "1990", "F", 0).add_to_database()
    player2 = Player("Gexo", "Bet", "1999", "X", 5).add_to_database()
    player3 = Player('Yina', 'Pupo', "2001", "F", 6).add_to_database()
    player4 = Player("Gwendy", "Pupo", "2003", "F", 3).add_to_database()
    player5 = Player("Enzo", "Pupo", "2010", "F", 1).add_to_database()
    player6 = Player('José Leodan', 'Pupo', "2000", "M", 0).add_to_database()
    player7 = Player('Devon', 'White', "1997", "M", 0).add_to_database()
    player8 = Player('Shanna-Kay', 'Samuels', "1988", "F", 0).add_to_database()
    print(f'   --- Database now has {len(players_database)} players.')

    tournoi = Tournament()
    tournoi.add_players([0,1,2,3,4,5,6,7])
    
    # first tour
    # print(tournoi.sort_players())
    # print(tournoi.generate_pairs())
    print(tournoi.new_round())
    
    # val = input("Enter your value: ")
    # print(val)

    view_tournament(tournoi)

if __name__ == '__main__' :
    development()
    # main_menu()
