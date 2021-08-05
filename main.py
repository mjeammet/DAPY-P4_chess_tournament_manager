from tournament.models import Player, players_database 
from tournament.models.tournament import Tournament, PLAYERS_PER_TOURNAMENT
from tournament.views import main_menu, view_tournament, list_tournament_players
from script_for_dev_purposes import development

DEBUG = True

if __name__ == '__main__' :
    development()
    # main_menu()
