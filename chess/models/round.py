from datetime import datetime

class Round(list):
    """ Un tour de jeu. """

    def __init__(self, turn_name, matchs): 
        self.name = turn_name
        self.start_time = str(datetime.today())
        self.end_datetime = None
        self.matchs = matchs

    def mark_as_finished(self):
        """Mark round as finished, sets endtime and calls for an update of match results."""
        self.end_datetime = str(datetime.today())
        self.is_finished = True

        for match in self.matchs:
            match.update_results(1,0)

        return True

    def __str__(self):
        return str(self.matchs)

    def __repr__(self):
        return self.__str__()