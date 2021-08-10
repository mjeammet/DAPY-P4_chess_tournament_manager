from chess.models import players_database, VERBOSE
from chess.models.round import Round


PLAYERS_PER_TOURNAMENT = 8

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

    def add_player_to_tournament(self, id):
        """ Add a player to tournament, using their id. """
        # checks if tournament isn't already full
        if len(self.players) >= PLAYERS_PER_TOURNAMENT:
            print("Le tournoi est déjà plein, vous ne pouvez pas ajouter de participant.es.")
        else:
            if id < len(players_database):
                # [player if getattr(player, 'id') == 3 else for player in players_database]
                self.players.append(id)
                if VERBOSE:
                    print(f'    {players_database[id]} ajouté.e au tournoi')
            else:
                print("Joueur inconnu. Veuillez l'ajouter à la base de données.")

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

        if by == 'ranking':
            # get players objects instead of simply the indice in db
            players_as_objects = [players_database[player_id] for player_id in self.players]
            sorted_players_as_objects = sorted(players_as_objects, key=lambda player:player.ranking, reverse=True)
            # reverting back to indices 
            self.players = [players_database.index(player) for player in sorted_players_as_objects]
        elif by == 'score':
            # "un-tuple" players list
            players = [[item1, item2] for tup in self.rounds[-1].matchs for item1, item2 in tup]
            # sort players list by sc
            sorted_players = sorted(players, key = lambda x: x[1], reverse=True)

            self.players = [item[0] for item in sorted_players]
        elif by == 'name':
            # get players objects instead of simply the indice in db
            players_as_objects = [players_database[player_id] for player_id in self.players]
            sorted_players_as_objects = sorted(players_as_objects, key=lambda player:player.last_name)
            # reverting back to indices 
            self.players = [players_database.index(player) for player in sorted_players_as_objects]
        else:
            message = (f'Cannot sort by {by}. Please sort by \'score\', \'ranking\' or \'name\' instead.')
            raise Exception(message)

        return self.players

    def new_round(self):
        """ Initiate a new round."""
        # self.turns.append(self.generate_pairs())

        # Get the new turn's number
        round_number = int(len(self.rounds)+1)
        round_name = f'Round_{round_number}'
        print(f'Init turn number {round_number}')

        
        # Define sorting type depending on the turn's number
        if round_number == 1:
            sorted_players_list = self.sort_players(by = 'ranking')
        else :
            sorted_players_list = self.sort_players(by = 'score')

        this_round = Round(turn_name = round_name, players_list = sorted_players_list)
        self.rounds.append(this_round)

        return self.rounds

