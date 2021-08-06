from chess.models.match import Match
PLAYERS_PER_TOURNAMENT = 8

class Round(list):
    """ Un tour de jeu. """

    def __init__(self, turn_name, players_list): 
        # self = list(self.generate_pairs(players_list))
        self.name = turn_name
        self.start_datetime = 0
        self.end_datetime = 0
        self.matchs = self.generate_pairs(players_list)

    def generate_pairs(self, players_list):
        """Generates pairs of players for the next round"""
        list_of_matchs = []
        half = int(PLAYERS_PER_TOURNAMENT/2)
        if len(players_list) == PLAYERS_PER_TOURNAMENT:
            # Dividing players in two halves
            highest_half = players_list[:half]
            lowest_half = players_list[half:]
            
            for position in range(len(highest_half)):
                # match = ([highest_half[position], 0], [lowest_half[position], 0])
                match = Match(([highest_half[position], 0] , [lowest_half[position], 0]))
                list_of_matchs.append(match)

        return(list_of_matchs)

            