from chess.controllers.controllers import ApplicationController
from chess.models import Player, Tournament, Match, Round
from chess.models import Database
from settings import TEST


def main():
    if TEST:
        # empty_database_table("players", force=True)
        # empty_database_table("tournaments", force=True)

        # Player(1, "Marie", "Pupo", "1990", "F", 0).save()
        # Player(2, "Amandine", "Gay", "1984", "F", 5).save()
        # Player(3, 'Rosa', 'Parks', "1913", "F", 6).save()
        # Player(4, "Rokhaya", "Diallo", "1978", "F", 3).save()
        # Player(5, "Christiane", "Taubira", "1952", "F", 1).save()
        # Player(6, 'Maryse', 'Condé', "1937", "F", 0).save()
        # Player(7, 'Danièle', 'Obono', "1980", "F", 0).save()
        # Player(8, 'Aïssa', 'Maïga', "1975", "F", 0).save()

        # Fruit = Query()
        # players_table.remove(Fruit.first_name == "Marie")

        # print(f'--- Database now has {len(players_table)} players.')

        from chess.controllers.controllers import get_db_object
        tournoi = Tournament(name = 'Test tournament 2021', location = "Paris, France")
        print(tournoi)
        # tournoi.add_players([1, 2, 3, 4, 5, 6, 7, 84, 8])
        # tournoi.save()

        round1 = tournoi.new_round()
        print('    before :', tournoi.rounds[0])
        round1.mark_as_finished()
        print('    after :', tournoi.rounds[0])
        # print(tournoi.rounds[0].matchs[1])

        tournoi.new_round()
        round = 1
        print('    before :', tournoi.rounds[round])
        tournoi.rounds[round].matchs[0].update_results(0.5, 0.5)
        tournoi.rounds[round].matchs[1].update_results(1, 0)
        tournoi.rounds[round].matchs[2].update_results(1, 0)
        tournoi.rounds[round].matchs[3].update_results(0, 1)
        print('    after :', tournoi.rounds[round])

        tournoi.new_round()
        round = 2
        print('    avant :', tournoi.rounds[round])
        tournoi.rounds[round].matchs[0].update_results(1, 0)
        tournoi.rounds[round].matchs[1].update_results(1, 0)
        tournoi.rounds[round].matchs[2].update_results(0, 1)
        tournoi.rounds[round].matchs[3].update_results(1, 0)
        print('    après :', tournoi.rounds[round])

        tournoi.new_round()
        round = 3
        print('    avant :', tournoi.rounds[round])
        tournoi.rounds[round].matchs[0].update_results(1, 0)
        tournoi.rounds[round].matchs[1].update_results(0.5, 0.5)
        tournoi.rounds[round].matchs[2].update_results(0, 1)
        tournoi.rounds[round].matchs[3].update_results(1, 0)
        print('    après :', tournoi.rounds[round])

        print('\nFinal order is: \t')
        print(tournoi.sort_players(by = 'score'))

        ## REPORTS !
        # print_tournament_players(tournoi, sort_by='rating')
        # print_tournament_turn(tournoi)
    else:
        app = ApplicationController()
        app.start()


if __name__ == '__main__':
    main()
