from chess.models import get_player_object

class Match(tuple):
    def __init__(self, duet):
        pass    
    
    def update_results(self, result_player1, result_player2):
        """ Updates results of a match. """
        self[0][1] += result_player1
        self[1][1] += result_player2
    
    def __str__(self):
        """Prints opponents """
        player1 = get_player_object(self[0][0])
        player2 = get_player_object(self[1][0])
        return f'    Match opposant {player1} (cl. {player1.ranking}) et {player2} (cl. {player2.ranking}).'