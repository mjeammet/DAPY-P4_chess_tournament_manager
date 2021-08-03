from models import Player, PLAYERS_DATABASE


PLAYERS_PER_TOURNAMENT = 8
PLAYERS_DATABASE

class Tournament:
    """Un tournoi"""

    def __init__(self, name='', number_of_turns = 4, description=''):
        # location, date, tournees, time_control,
        self.name = name
        self.location = ''
        self.date = ''
        self.tour = 0               # "la liste de instances rondes\" ?" 
        self.players = []
        
    

    # PLAYERS HANDLING 
    def add_player(self, id):
        if len(self.players) >= PLAYERS_PER_TOURNAMENT:
            print("Le tournoi est déjà plein, vous ne pouvez pas ajouter de participant.es.")
        else:
            if id < len(PLAYERS_DATABASE):
                self.players.append(id)
                print(f'{PLAYERS_DATABASE[id]} ajouté.e au tournoi')
            else:
                print("Joueur inconnu. Veuillez l'ajouter à la base de données.")
        if len(self.players) == PLAYERS_PER_TOURNAMENT:
            print("Le tournoi est désormais plein ! ")

    def add_players(self, list_of_integers):
        for num in list_of_integers:
            self.add_player(num)
    
    def sort_players(self):
        # players_objects = [PLAYERS_DATABASE[player_id] for player_id in self.players]
        self.players = [PLAYERS_DATABASE.index(player) for player in sorted([PLAYERS_DATABASE[player_id] for player_id in self.players], key=lambda player:player.rating, reverse=True)]
        return self.players

    def generate_pairs(self):
        pairs = []
        if len(self.players) == PLAYERS_PER_TOURNAMENT:
            for player_id in self.players:
                print(player_id)
                pairs.append((self.players[int(player_id)], self.players[player_id+int(PLAYERS_PER_TOURNAMENT/2)]))
        return pairs 