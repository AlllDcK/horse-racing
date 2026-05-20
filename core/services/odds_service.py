class OddsService:

    @staticmethod
    def calculate(horses):
        total = sum(h.base_speed for h in horses)
        odds = {}
        for horse in horses:
            probability = horse.base_speed / total
            odds[horse.id] = round(1 / probability, 2)
        return odds