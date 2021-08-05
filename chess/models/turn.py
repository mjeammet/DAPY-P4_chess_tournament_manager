from chess.models.match import Match
PLAYERS_PER_TOURNAMENT = 8

class Turn(list):
    """ Un tour de jeu. """

    def __init__(self, players_list): 
        # self = list(self.generate_pairs(players_list))

        half = int(PLAYERS_PER_TOURNAMENT/2)
        if len(players_list) == PLAYERS_PER_TOURNAMENT:
            # Dividing players in two halves
            highest_half = players_list[:half]
            lowest_half = players_list[half:]
            
            for position in range(len(highest_half)):
                # match = ([highest_half[position], 0], [lowest_half[position], 0])
                match = Match(highest_half[position], lowest_half[position])
                self.append(match)