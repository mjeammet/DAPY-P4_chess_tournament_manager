class Round:
    """ Un tour de jeu. """

    def __init__(self, turn_name, start_datetime, end_datetime, matchs): 
        self.name = turn_name
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.matchs = matchs

    def mark_as_finished(self, end_datetime):
        """Mark round as finished, sets endtime and calls for an update of match results."""
        self.end_datetime = end_datetime
        self.is_finished = True

        for match in self.matchs:
            match.update_results(1,0)

        return True

    def serialize(self):
        composition = vars(self)
        composition['matchs'] = [match_ for match_ in self.matchs]
        return composition

    def __str__(self):
        return str(self.matchs)

    def __repr__(self):
        return self.__str__()