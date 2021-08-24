class Match(tuple):
    def __init__(self, duet):
        self = duet
        self[0][0] = duet[0][0]
        self[0][1] = duet[0][1]
        self[1][0] = duet[1][0]
        self[1][1] = duet[1][1]
        # self.p1_id = duet[0][0]
        # self.p1_score = duet[0][1]
        # self.p2_id = duet[1][0]
        # self.p2_score = duet[1][1]
        
    # def update_results(self, result_player1, result_player2):
    #     """ Updates results of a match. """

    #     if (result_player1,result_player2) == (None, None):
    #         print('Please input results')
    #     else:
    #         self[0][1] += result_player1
    #         self[1][1] += result_player2
    
    def serialize(self):
        print_duet = print(self)
        return print_duet

    # def __str__(self):
    #     """Prints opponents """
    #     player1 = get_player_object(self[0][0])
    #     player2 = get_player_object(self[1][0])
    #     # TODO add "round_number x index" pour avoir Match numéro X opposant player1 et player2
    #     return f'    Match opposant {player1} (cl. {player1.ranking}) et {player2} (cl. {player2.ranking}).'