from core.repositories.interfaces import PlayerRepositoryInterface


class DepositUseCase:

    def __init__(self, player_repo: PlayerRepositoryInterface):
        self.player_repo = player_repo

    def execute(self, user, amount):
        if amount <= 0:
            raise ValueError("Некорректная сумма")

        player = self.player_repo.get_by_user(user)
        player.balance += amount
        self.player_repo.save(user, player)

        return player