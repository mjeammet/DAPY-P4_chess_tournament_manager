class Match(tuple):
    def __init__(self, duet):
        self = duet
    
    def serialize(self):
        print_duet = print(self)
        return print_duet

    # def __str__(self):
    #     """Prints opponents """
    #     player1 = get_player_object(self[0][0])
    #     player2 = get_player_object(self[1][0])
    #     # TODO add "round_number x index" pour avoir Match numéro X opposant player1 et player2
    #     return f'    Match opposant {player1} (cl. {player1.ranking}) et {player2} (cl. {player2.ranking}).'