from chess.controllers import HomeController
from chess.models import Player, Tournament, PLAYERS_PER_TOURNAMENT, Match
from tinydb import TinyDB, Query
from chess.database import get_database_table

DEBUG = False

def main():
    if DEBUG:
        players_table = get_database_table("players", empty = True)
        tournament_table = get_database_table("tournament", empty = True)

        player1 = Player("Marie", "Pupo", "1990", "F", 0)
        player2 = Player("Amandine", "Gay", "1984", "F", 5)
        player3 = Player('Rosa', 'Parks', "1913", "F", 6)
        player4 = Player("Rokhaya", "Diallo", "1978", "F", 3)
        player5 = Player("Christiane", "Taubira", "1952", "F", 1)
        player6 = Player('Maryse', 'Condé', "1937", "F", 0)
        player7 = Player('Danièle', 'Obono', "1980", "F", 0)
        player8 = Player('Aïssa', 'Maïga', "1975", "F", 0)

        # Fruit = Query()
        # players_table.remove(Fruit.first_name == "Marie")

        print(f'--- Database now has {len(players_table)} players.')

        tournoi = Tournament(name = 'Test tournament 2021', location = "Paris, France")
        tournoi.add_players([1,2,3,4,5,6,7,84, 8])
        
        round1 = tournoi.new_round()
        print('    before :', tournoi.rounds[0])
        round1.mark_as_finished()
        print('    after :', tournoi.rounds[0])
        # print(tournoi.rounds[0].matchs[1])

        tournoi.new_round()
        round = 1 
        print('    before :', tournoi.rounds[round])
        tournoi.rounds[round].matchs[0].update_results(0.5,0.5)
        tournoi.rounds[round].matchs[1].update_results(1,0)
        tournoi.rounds[round].matchs[2].update_results(1,0)
        tournoi.rounds[round].matchs[3].update_results(0,1)
        print('    after :', tournoi.rounds[round])

        tournoi.new_round()
        round = 2
        print('    avant :', tournoi.rounds[round])
        tournoi.rounds[round].matchs[0].update_results(1,0)
        tournoi.rounds[round].matchs[1].update_results(1,0)
        tournoi.rounds[round].matchs[2].update_results(0,1)
        tournoi.rounds[round].matchs[3].update_results(1,0)
        print('    après :', tournoi.rounds[round])

        tournoi.new_round()
        round = 3
        print('    avant :', tournoi.rounds[round])
        tournoi.rounds[round].matchs[0].update_results(1,0)
        tournoi.rounds[round].matchs[1].update_results(0.5,0.5)
        tournoi.rounds[round].matchs[2].update_results(0,1)
        tournoi.rounds[round].matchs[3].update_results(1,0)
        print('    après :', tournoi.rounds[round])

        print('\nFinal order is: \t')
        print(tournoi.sort_players(by = 'score')) 

        ## REPORTS ! 
        # print_tournament_players(tournoi, sort_by='rating')
        # print_tournament_turn(tournoi)
    else:
        return HomeController()


if __name__ == '__main__' :
    main()
