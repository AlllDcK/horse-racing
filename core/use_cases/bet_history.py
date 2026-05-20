class BetHistoryUseCase:

    def execute(self, bets):

        return sorted(
            bets,
            key=lambda bet: bet.created_at,
            reverse=True
        )