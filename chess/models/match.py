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