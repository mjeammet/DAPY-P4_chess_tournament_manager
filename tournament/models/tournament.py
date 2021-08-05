from tournament.models.players import Player, players_database


PLAYERS_PER_TOURNAMENT = 8
players_database

class Tournament:
    """Un tournoi
    TODO Gestion du temps"""

    def __init__(self, name='', number_of_turns = 4, description=''):
        # location, date, tournees, time_control,
        # self.id = int             # auto-increment ? 
        self.name = name
        self.location = ''
        self.date = ''
        self.turn = 0               # "la liste de instances rondes\" ?" 
        self.players = []
    

    # PLAYERS HANDLING 
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
        

    class Turn:
        """ Un tour de jeu. """

        def __init__(self, number):
            number = 0
            self.matches = generate_pairs()



    def sort_players(self, by = 'score'):
        """ Sorts player to generate pairs according to the swiss tournament pattern. 
        
        Args:
        - by -- the parameter by which players will be sorted. Can be 'score' or 'rating'.

        Returns:
        - a sorted list of players
        """

        # if players are to be sorted by rating
        players_as_objects = [players_database[player_id] for player_id in self.players]
        if by == 'rating':
            sorted_players_as_objects = sorted(players_as_objects, key=lambda player:player.rating, reverse=True)
        elif by == 'score':
            print('sorting by score plz')
        elif by == 'name':
            sorted_players_as_objects = sorted(players_as_objects, key=lambda player:player.last_name, reverse=False)
        else:
            print(f'Can sort by {by}. Please sort by \'score\', \'rating\' or \'name\' instead.')
            return False

        # reverting back to indices 
        self.players = [players_database.index(player) for player in sorted_players_as_objects]
        return self.players


    def generate_pairs():
        """ Generate pairs of players according to swiss tournament pattern"""
        # sorts player
        self.sort_players(by = 'rating')

        # attribute pairs
        pairs = []
        half = int(PLAYERS_PER_TOURNAMENT/2)
        if len(self.players) == PLAYERS_PER_TOURNAMENT:
            for player_id in range(half):
                pair = (self.players[player_id], self.players[player_id+half])
                pairs.append(pair)
        return pairs 

    def new_round(self):
        """ Initiate a new round. Call pairs """
        print(self.generate_pairs())
        self.turn += 1
        return self.turn 