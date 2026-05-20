from django.test import TestCase

from core.entities.player import Player
from core.entities.horse import Horse
from core.entities.bet import Bet

from core.use_cases.deposit import DepositUseCase
from core.use_cases.withdraw import WithdrawUseCase
from core.use_cases.place_bet import PlaceBetUseCase
from core.use_cases.run_race import RunRaceUseCase
from core.use_cases.bet_history import BetHistoryUseCase


class DepositUseCaseTest(TestCase):

    def test_deposit_money(self):
        player = Player(1, "max", 1000)

        use_case = DepositUseCase()

        result = use_case.execute(player, 500)

        self.assertEqual(result.balance, 1500)

    def test_negative_deposit(self):
        player = Player(1, "max", 1000)

        use_case = DepositUseCase()

        with self.assertRaises(Exception):
            use_case.execute(player, -100)


class WithdrawUseCaseTest(TestCase):

    def test_withdraw_money(self):
        player = Player(1, "max", 1000)

        use_case = WithdrawUseCase()

        result = use_case.execute(player, 300)

        self.assertEqual(result.balance, 700)

    def test_withdraw_more_than_balance(self):
        player = Player(1, "max", 1000)

        use_case = WithdrawUseCase()

        with self.assertRaises(Exception):
            use_case.execute(player, 5000)

    def test_negative_withdraw(self):
        player = Player(1, "max", 1000)

        use_case = WithdrawUseCase()

        with self.assertRaises(Exception):
            use_case.execute(player, -100)


class RunRaceUseCaseTest(TestCase):

    def test_race_returns_winner(self):
        horses = [
            Horse(1, "Thunder", 90),
            Horse(2, "Rocket", 80),
            Horse(3, "Storm", 85),
        ]

        use_case = RunRaceUseCase()

        winner = use_case.execute(horses)

        self.assertIn(winner, horses)


class PlaceBetUseCaseTest(TestCase):

    def test_win_bet(self):
        player = Player(1, "max", 1000)

        horse = Horse(1, "Thunder", 90)

        use_case = PlaceBetUseCase()

        result = use_case.execute(
            player=player,
            selected_horse=horse,
            winner=horse,
            amount=100,
            odds=2.5
        )

        updated_player = result["player"]
        bet = result["bet"]

        self.assertTrue(bet.is_win)
        self.assertEqual(bet.win_amount, 250)

        # 1000 - 100 + 250
        self.assertEqual(updated_player.balance, 1150)

    def test_lose_bet(self):
        player = Player(1, "max", 1000)

        selected_horse = Horse(1, "Thunder", 90)
        winner = Horse(2, "Rocket", 80)

        use_case = PlaceBetUseCase()

        result = use_case.execute(
            player=player,
            selected_horse=selected_horse,
            winner=winner,
            amount=100,
            odds=2.5
        )

        updated_player = result["player"]
        bet = result["bet"]

        self.assertFalse(bet.is_win)
        self.assertEqual(bet.win_amount, 0)

        self.assertEqual(updated_player.balance, 900)

    def test_invalid_bet_amount(self):
        player = Player(1, "max", 1000)

        horse = Horse(1, "Thunder", 90)

        use_case = PlaceBetUseCase()

        with self.assertRaises(Exception):
            use_case.execute(
                player=player,
                selected_horse=horse,
                winner=horse,
                amount=-100,
                odds=2
            )

    def test_not_enough_money(self):
        player = Player(1, "max", 100)

        horse = Horse(1, "Thunder", 90)

        use_case = PlaceBetUseCase()

        with self.assertRaises(Exception):
            use_case.execute(
                player=player,
                selected_horse=horse,
                winner=horse,
                amount=1000,
                odds=2
            )


class BetHistoryUseCaseTest(TestCase):

    def test_sort_bets_by_date(self):

        player = Player(1, "max", 1000)

        horse = Horse(1, "Thunder", 90)

        bet1 = Bet(
            player=player,
            horse=horse,
            amount=100,
            created_at=1
        )

        bet2 = Bet(
            player=player,
            horse=horse,
            amount=200,
            created_at=3
        )

        bet3 = Bet(
            player=player,
            horse=horse,
            amount=150,
            created_at=2
        )

        bets = [bet1, bet2, bet3]

        use_case = BetHistoryUseCase()

        result = use_case.execute(bets)

        self.assertEqual(result[0].amount, 200)
        self.assertEqual(result[1].amount, 150)
        self.assertEqual(result[2].amount, 100)