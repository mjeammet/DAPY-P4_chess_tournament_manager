from datetime import datetime

class Round(list):
    """ Un tour de jeu. """

    def __init__(self, turn_name, players_and_scores_list): 
        self.name = turn_name
        self.start_datetime = str(datetime.today())
        self.is_finished = False
        self.end_datetime = 0
        self.matchs = self.generate_pairs(players_and_scores_list)

    def mark_as_finished(self):
        """Mark round as finished, sets endtime and calls for an update of match results."""
        self.end_datetime = str(datetime.today())
        self.is_finished = True

        for match in self.matchs:
            match.update_results(1,0)

        return True

    def __repr__(self):
        return str(self.matchs)