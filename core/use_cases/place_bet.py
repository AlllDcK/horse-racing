from core.entities.bet import Bet


class PlaceBetUseCase:

    def execute(
        self,
        player,
        selected_horse,
        winner,
        amount,
        odds
    ):

        if amount <= 0:
            raise Exception("Некорректная ставка")

        if player.balance < amount:
            raise Exception("Недостаточно средств")

        player.balance -= amount

        is_win = selected_horse.id == winner.id

        win_amount = 0

        if is_win:
            win_amount = int(amount * odds)
            player.balance += win_amount

        bet = Bet(
            player=player,
            horse=selected_horse,
            amount=amount,
            is_win=is_win,
            win_amount=win_amount
        )

        return {
            "player": player,
            "bet": bet
        }
