from datetime import datetime
from tinydb import Query
from .database import get_database_table
from settings import VERBOSE, PLAYERS_PER_TOURNAMENT, ROUNDS_PER_TOURNAMENT


TIME_CONTROL_TYPE = (
    "bullet"
    "blitz"
    "fast"
)

class Tournament:
    """Un tournoi
    TODO Gestion du temps"""

    def __init__(self, name, location, date='', rounds = [], players = [], time_control = '', description=''):
        self.name = name
        self.location = location
        self.date = date
        self.rounds = rounds
        self.players = players
        self.time_control = time_control
        self.description = description

    # @property # TODO Upon uncommenting I get TypeError: 'bool' object is not callable
    def is_full(self):
        """A simple property to check if tournament is full (ie. contains 8 players)"""
        return True if len(self.players) == 8 else False

    def add_player_to_tournament(self, id):
        """ Add a player to tournament, using their id. """
        # checks if tournament isn't already full
        if len(self.players) >= PLAYERS_PER_TOURNAMENT:
            print("Le tournoi est déjà plein, vous ne pouvez pas ajouter de participant.es.")
        else:
            players_table = get_database_table("players")            
            player = Query()
            if players_table.search(player.id == id) != []:                 
                # players_table.search(player.id == id)                
                self.players.append(id)
                if VERBOSE:
                    print(f'    {players_database[id]} ajouté.e au tournoi')
            else: 
                print(f"Unknown player #{id}. Please select a valid player id.")

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

        players_table = get_database_table("players")
        if by == 'ranking':
            # filter the database to only get this tournament's entrants
            entrants = players_table.search(Query().id.one_of(self.players))

            # sorts players by ranking and then get their ids
            self.players = [player['id'] for player in sorted(entrants, key = lambda x:x['ranking'], reverse=True)]
        elif by == 'score':
            # "un-tuple" players list
            players_score = [[item1, item2] for tup in self.rounds[-1].matchs for item1, item2 in tup]
            
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

        if round_number >= ROUNDS_PER_TOURNAMENT:
            print(f"Le nombre de tour par tournoi ne peut pas excéder {ROUNDS_PER_TOURNAMENT} (voir \"settings.py\").")

        else:
            round_name = f'Round_{round_number}'
            print(f'Start round number {round_number}')

            # Define sorting type depending on the turn's number
            if round_number == 1:
                sorted_players_list = self.sort_players(by = 'ranking')
            else :
                sorted_players_list = self.sort_players(by = 'score')

            # Add a new round with rank players and their associated scores
            this_round = Round(turn_name = round_name, players_and_scores_list = sorted_players_list)
            self.rounds.append(this_round)

            return self.rounds[-1]

class Match(tuple):
    def __init__(self, duet):
        pass    
    
    def update_results(self, result_player1, result_player2):
        """ Updates results of a match. """

        if (result_player1,result_player2) == (None, None):
            print('Please input results')
        else:
            self[0][1] += result_player1
            self[1][1] += result_player2
    
    # def __str__(self):
    #     """Prints opponents """
    #     player1 = get_player_object(self[0][0])
    #     player2 = get_player_object(self[1][0])
    #     # TODO add "round_number x index" pour avoir Match numéro X opposant player1 et player2
    #     return f'    Match opposant {player1} (cl. {player1.ranking}) et {player2} (cl. {player2.ranking}).'


class Round(list):
    """ Un tour de jeu. """

    def __init__(self, turn_name, players_and_scores_list): 
        self.name = turn_name
        self.start_datetime = str(datetime.today())
        self.is_finished = False
        self.end_datetime = 0
        self.matchs = self.generate_pairs(players_and_scores_list)

    def mark_as_finished(self):
        """Mark round as finished, sets endtime and calls for an update of match results."""
        self.end_datetime = str(datetime.today())
        self.is_finished = True

        for match in self.matchs:
            match.update_results(1,0)

        return True

    def generate_pairs(self, players_and_scores_list):
        """Generates pairs of players for the next round
        
        Args:
            - score_list : A list of lists containing players and scores """
        list_of_matchs = []
        half = int(PLAYERS_PER_TOURNAMENT/2)
        
        if len(players_and_scores_list) == PLAYERS_PER_TOURNAMENT:
            # Dividing players in two halves
            highest_half = players_and_scores_list[:half]
            lowest_half = players_and_scores_list[half:]
            
            for position in range(len(highest_half)):
                match = Match(([highest_half[position], lowest_half[position]]))
                list_of_matchs.append(match)
                
        return list_of_matchs

    def __repr__(self):
        return str(self.matchs)