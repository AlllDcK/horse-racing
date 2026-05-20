class OddsService:

    @staticmethod
    def calculate(horses):
        total = sum(h.speed for h in horses)
        odds = {}
        for horse in horses:
            probability = horse.speed / total
            odds[horse.id] = round(1 / probability, 2)
        return odds