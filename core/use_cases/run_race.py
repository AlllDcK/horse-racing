import random


class RunRaceUseCase:

    def execute(self, horses):

        scores = {}

        for horse in horses:
            score = horse.base_speed + random.randint(1, 10)
            scores[horse] = score

        winner = max(scores, key=scores.get)

        return winner