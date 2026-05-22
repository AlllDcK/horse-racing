from core.entities.bet import Bet
from core.repositories.interfaces import (
    PlayerRepositoryInterface,
    BetRepositoryInterface
)


class PlaceBetUseCase:

    def __init__(
        self,
        player_repo: PlayerRepositoryInterface,
        bet_repo: BetRepositoryInterface
    ):
        self.player_repo = player_repo
        self.bet_repo = bet_repo

    def execute(
        self,
        user,
        selected_horse,
        winner,
        amount,
        odds
    ):
        player = self.player_repo.get_by_user(user)

        # 2. Валидация
        if amount <= 0:
            raise ValueError("Некорректная ставка")

        if player.balance < amount:
            raise ValueError("Недостаточно средств")

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

        self.player_repo.save(user, player)
        self.bet_repo.create(user, bet)

        return {
            "player": player,
            "bet": bet
        }