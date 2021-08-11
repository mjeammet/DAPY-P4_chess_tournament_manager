from chess.models import players_database, VERBOSE
from chess.models.round import Round
from chess.database import get_database_table
from tinydb import Query

PLAYERS_PER_TOURNAMENT = 8
tournament_database = []

class Tournament:
    """Un tournoi
    TODO Gestion du temps"""

    def __init__(self, name='', number_of_turns = 4, description=''):
        # location, date, tournees, time_control,
        # self.id = int             # auto-increment ? 
        self.name = name
        self.location = ''
        self.date = ''
        self.rounds = []
        self.players = []
        self.time_control = []
        self.description = ''
        tournament_database.append(self)

    def add_player_to_tournament(self, id):
        """ Add a player to tournament, using their id. """
        # checks if tournament isn't already full
        if len(self.players) >= PLAYERS_PER_TOURNAMENT:
            print("Le tournoi est déjà plein, vous ne pouvez pas ajouter de participant.es.")
        else:
            players_table = get_database_table("players")
            
            try:
                player = Query()
                # players_table.search(player.id == id)
                print(players_table.search(player.id == id))
                self.players.append(id)
                if VERBOSE:
                    print(f'    {players_database[id]} ajouté.e au tournoi')
            except IndexError:
                print(f"Joueur #{id} inconnu. Veuillez l'ajouter à la base de données.")

        # notifies if it was the eighth player
        if len(self.players) == PLAYERS_PER_TOURNAMENT:
            print("8 participant.es ajouté.es au tournoi. Le tournoi est désormais plein ! ")


    def add_players(self, list_of_integers):
        for num in list_of_integers:
            self.add_player_to_tournament(num)

    def sort_players(self, by = 'score'):
        """ Sorts player to generate pairs according to the swiss tournament pattern. 
        
        Args:
        - by -- the parameter by which players will be sorted. Can be 'score' or 'ranking'.

        Returns:
        - a sorted list of players
        """
        if len(self.rounds) == 0:
            # Add "0" score for everyone
            players_score = [[player, 0] for player in self.players]
        else:
            # "un-tuple" players list
            players_score = [[item1, item2] for tup in self.rounds[-1].matchs for item1, item2 in tup]


        if by == 'ranking':
            # get players objects instead of simply the indice in db
            players_as_objects = [players_database[player_id] for player_id in self.players]
            sorted_players_as_objects = sorted(players_as_objects, key=lambda player:player.ranking, reverse=True)
            # reverting back to indices 
            self.players = [players_database.index(player) for player in sorted_players_as_objects]
        elif by == 'score':
            # Sorts player by score of previous round
            sorted_players = sorted(players_score, key = lambda x: x[1], reverse=True)
            # print("sorted score = ", sorted_players)

            self.players = [item[0] for item in sorted_players]
            return sorted_players
        elif by == 'name':
            # get players objects instead of simply the indice in db
            players_as_objects = [players_database[player_id] for player_id in self.players]
            sorted_players_as_objects = sorted(players_as_objects, key=lambda player:player.last_name)
            # reverting back to indices 
            self.players = [players_database.index(player) for player in sorted_players_as_objects]
        else:
            message = (f'Cannot sort by {by}. Please sort by \'score\', \'ranking\' or \'name\' instead.')
            raise Exception(message)

        # TODO change order of players in self.players

        return players_score

    def new_round(self):
        """ Initiate a new round."""
        # TODO add a test if tournament is not full.

        # Get the new turn's number
        round_number = int(len(self.rounds)+1)
        round_name = f'Round_{round_number}'
        print(f'Start round number {round_number}')

        # Define sorting type depending on the turn's number
        if round_number == 1:
            sorted_players_list = self.sort_players(by = 'ranking')
        else :
            sorted_players_list = self.sort_players(by = 'score')

        # Add a new round with rank players and their associated scores
        this_round = Round(turn_name = round_name, players_list = sorted_players_list)
        self.rounds.append(this_round)

        return self.rounds

