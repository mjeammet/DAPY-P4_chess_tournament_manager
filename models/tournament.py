from models.players import PLAYERS_DATABASE


PLAYERS_PER_TOURNAMENT = 8
PLAYERS_DATABASE

class Tournament:
    """Un tournoi"""

    def __init__(self, name='', number_of_turns = 4, description=''):
        # location, date, tournees, time_control,
        self.name = name
        self.players = []

    def add_player(self, id):
        if len(self.players) >= PLAYERS_PER_TOURNAMENT:
            print("Le tournoi est déjà plein, vous ne pouvez pas ajouter de participant.es.")
        else:
            if id < len(PLAYERS_DATABASE):
                player = PLAYERS_DATABASE[id]
                self.players.append(player)
                print(f'{player} ajouté.e au tournoi')
            else:
                print("Joueur inconnu. Veuillez l'ajouter à la base de données.")
        if len(self.players) == PLAYERS_PER_TOURNAMENT:
            print("Le tournoi est désormais plein ! ")

    def add_players(self, list_of_integers):
        for num in list_of_integers:
            self.add_player(num)