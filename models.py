
PLAYERS_PER_TOURNAMENT = 8

# database doit être une base de données de joueurs
PLAYERS_DATABASE = []

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

class Player:
    """Un joueur pour le tournoi.
    # faire un dictionnaire pour le genre
    # Sérialisation / Désérialisation ?
    """

    def __init__(self, last_name, first_name, birth_date, gender):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.gender = gender
        self.rating = 0

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def add_to_database(self):
        PLAYERS_DATABASE.append(self)
        print(f'{self.first_name} {self.last_name} ajouté.e à la base de données.')
