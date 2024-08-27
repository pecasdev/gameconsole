from now import now


class ReactionRecord:
    def __reset(self):
        self.reaction_stamp_start = None
        self.reaction_stamp_end = None
        self.reaction_too_early = False

    def __init__(self):
        self.__reset()

    def __determine_score(self):
        if self.reaction_too_early:
            return -1
        elif (
            self.reaction_stamp_start is not None
            and self.reaction_stamp_end is not None
        ):
            # cap score at 9999
            return min(9999, int(self.reaction_stamp_end - self.reaction_stamp_start))
        else:
            return None

    def pop_score(self):
        result = self.__determine_score()

        if result is not None:
            self.__reset()

        return result

    def record_start(self):
        self.reaction_stamp_start = now()

    def record_end(self):
        self.reaction_stamp_end = now()

    def record_too_early(self):
        self.reaction_too_early = True
