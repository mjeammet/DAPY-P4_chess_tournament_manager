players_database = ['feinte pour ne pas partir de 0, à régler une fois qu\'on aura la db']

def get_player_object(id):
    try: 
        return players_database[id]
    except Exception as error:
        print("Unexpected error occurred.")
        raise error 

class Player:
    """Un joueur pour le tournoi.
    # TODO faire un dictionnaire pour le genre
    # TODO Sérialisation / Désérialisation ?
    """

    def __init__(self, first_name, last_name, birth_date, gender, ranking = 0):
        self.id = len(players_database)+1
        self.first_name = first_name
        self.last_name = last_name        
        self.birth_date = birth_date
        self.gender = gender
        self.ranking = ranking

    def __str__(self):
        return f'{self.full_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


    def add_to_database(self):
        players_database.append(self)
        # print(f'{self.full_name} ajouté.e à la base de données.')
