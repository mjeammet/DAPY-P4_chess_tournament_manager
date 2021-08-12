from chess.models.match import Match

PLAYERS_PER_TOURNAMENT = 8

class Round(list):
    """ Un tour de jeu. """

    def __init__(self, turn_name, players_and_scores_list): 
        self.name = turn_name
        self.start_datetime = 0
        self.end_datetime = 0
        self.matchs = self.generate_pairs(players_and_scores_list)

    def generate_pairs(self, players_and_scores_list):
        """Generates pairs of players for the next round
        
        Args:
            - score_list : A list of lists containing players and scores """
        list_of_matchs = []
        half = int(PLAYERS_PER_TOURNAMENT/2)
        
        if len(players_and_scores_list) == PLAYERS_PER_TOURNAMENT:
            # Dividing players in two halves
            highest_half = players_and_scores_list[:half]
            lowest_half = players_and_scores_list[half:]
            
            for position in range(len(highest_half)):
                match = Match(([highest_half[position], lowest_half[position]]))
                list_of_matchs.append(match)
                
        return list_of_matchs

    def __repr__(self):
        return str(self.matchs)