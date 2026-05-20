class Bet:

    def __init__(
        self,
        player,
        horse,
        amount,
        is_win=False,
        win_amount=0,
        created_at=None
    ):

        self.player = player
        self.horse = horse
        self.amount = amount
        self.is_win = is_win
        self.win_amount = win_amount
        self.created_at = created_at
