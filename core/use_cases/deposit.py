class DepositUseCase:

    def execute(self, player, amount):

        if amount <= 0:
            raise Exception("Некорректная сумма")

        player.balance += amount

        return player