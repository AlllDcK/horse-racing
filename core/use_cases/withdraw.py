class WithdrawUseCase:

    def execute(self, player, amount):

        if amount <= 0:
            raise Exception("Некорректная сумма")

        if amount > player.balance:
            raise Exception("Недостаточно средств")

        player.balance -= amount

        return player