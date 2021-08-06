from chess.models import players_database
from chess.models.turn import Round


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
    
    def add_player_to_tournament(self, id):
        """ Add a player to tournament, using their id. """
        # checks if tournament isn't already full
        if len(self.players) >= PLAYERS_PER_TOURNAMENT:
            print("Le tournoi est déjà plein, vous ne pouvez pas ajouter de participant.es.")
        else:
            if id < len(players_database):
                # [player if getattr(player, 'id') == 3 else for player in players_database]
                self.players.append(id)
                print(f'{players_database[id]} ajouté.e au tournoi')
            else:
                print("Joueur inconnu. Veuillez l'ajouter à la base de données.")

        # notifies if it was the eighth player
        if len(self.players) == PLAYERS_PER_TOURNAMENT:
            print("Le tournoi est désormais plein ! ")


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

        # if players are to be sorted by rating
        players_as_objects = [players_database[player_id] for player_id in self.players]
        if by == 'ranking':
            sorted_players_as_objects = sorted(players_as_objects, key=lambda player:player.ranking, reverse=True)
        elif by == 'score':
            print(self.rounds)
            sorted_players_as_objects = players_as_objects
            pass
        elif by == 'name':
            sorted_players_as_objects = sorted(players_as_objects, key=lambda player:player.last_name)
        else:
            message = (f'Cannot sort by {by}. Please sort by \'score\', \'ranking\' or \'name\' instead.')
            raise Exception(message)

        # reverting back to indices 
        self.players = [players_database.index(player) for player in sorted_players_as_objects]
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


        self.rounds.append(Round(turn_name = round_name, players_list = sorted_players_list))

        return self.rounds

