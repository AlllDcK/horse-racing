from django.test import TestCase

from core.entities.player import Player
from core.entities.horse import Horse
from core.entities.bet import Bet

from core.use_cases.deposit import DepositUseCase
from core.use_cases.withdraw import WithdrawUseCase
from core.use_cases.place_bet import PlaceBetUseCase
from core.use_cases.run_race import RunRaceUseCase
from core.use_cases.bet_history import BetHistoryUseCase
from core.repositories.interfaces import (
    PlayerRepositoryInterface,
    BetRepositoryInterface
)


# ---------------------------------------------------------------------------
# Mock-репозитории — никакой БД, просто объекты в памяти
# ---------------------------------------------------------------------------

class MockPlayerRepository(PlayerRepositoryInterface):

    def __init__(self, player):
        self._player = player
        self.saved = False

    def get_by_user(self, user):
        return self._player

    def save(self, user, player):
        self._player = player
        self.saved = True


class MockBetRepository(BetRepositoryInterface):

    def __init__(self):
        self.bets = []

    def create(self, user, bet):
        self.bets.append(bet)

    def get_user_bets(self, user):
        return self.bets


# ---------------------------------------------------------------------------
# Deposit
# ---------------------------------------------------------------------------

class DepositUseCaseTest(TestCase):

    def _make_use_case(self, player):
        self.player_repo = MockPlayerRepository(player)
        return DepositUseCase(player_repo=self.player_repo)

    def test_deposit_money(self):
        player = Player(1, "max", 1000)
        result = self._make_use_case(player).execute(user=None, amount=500)
        self.assertEqual(result.balance, 1500)
        self.assertTrue(self.player_repo.saved)

    def test_negative_deposit(self):
        player = Player(1, "max", 1000)
        with self.assertRaises(Exception):
            self._make_use_case(player).execute(user=None, amount=-100)


# ---------------------------------------------------------------------------
# Withdraw
# ---------------------------------------------------------------------------

class WithdrawUseCaseTest(TestCase):

    def _make_use_case(self, player):
        self.player_repo = MockPlayerRepository(player)
        return WithdrawUseCase(player_repo=self.player_repo)

    def test_withdraw_money(self):
        player = Player(1, "max", 1000)
        result = self._make_use_case(player).execute(user=None, amount=300)
        self.assertEqual(result.balance, 700)

    def test_withdraw_more_than_balance(self):
        player = Player(1, "max", 1000)
        with self.assertRaises(Exception):
            self._make_use_case(player).execute(user=None, amount=5000)

    def test_negative_withdraw(self):
        player = Player(1, "max", 1000)
        with self.assertRaises(Exception):
            self._make_use_case(player).execute(user=None, amount=-100)


# ---------------------------------------------------------------------------
# RunRace
# ---------------------------------------------------------------------------

class RunRaceUseCaseTest(TestCase):

    def test_race_returns_winner(self):
        horses = [
            Horse(1, "Thunder", 90),
            Horse(2, "Rocket", 80),
            Horse(3, "Storm", 85),
        ]
        winner = RunRaceUseCase().execute(horses)
        self.assertIn(winner, horses)


# ---------------------------------------------------------------------------
# PlaceBet
# ---------------------------------------------------------------------------

class PlaceBetUseCaseTest(TestCase):

    def _make_use_case(self, player):
        self.player_repo = MockPlayerRepository(player)
        self.bet_repo = MockBetRepository()
        return PlaceBetUseCase(
            player_repo=self.player_repo,
            bet_repo=self.bet_repo
        )

    def test_win_bet(self):
        player = Player(1, "max", 1000)
        horse = Horse(1, "Thunder", 90)

        result = self._make_use_case(player).execute(
            user=None,
            selected_horse=horse,
            winner=horse,
            amount=100,
            odds=2.5
        )

        self.assertTrue(result["bet"].is_win)
        self.assertEqual(result["bet"].win_amount, 250)
        self.assertEqual(result["player"].balance, 1150)  # 1000 - 100 + 250

        # Проверяем что репозитории были вызваны
        self.assertTrue(self.player_repo.saved)
        self.assertEqual(len(self.bet_repo.bets), 1)

    def test_lose_bet(self):
        player = Player(1, "max", 1000)
        selected_horse = Horse(1, "Thunder", 90)
        winner = Horse(2, "Rocket", 80)

        result = self._make_use_case(player).execute(
            user=None,
            selected_horse=selected_horse,
            winner=winner,
            amount=100,
            odds=2.5
        )

        self.assertFalse(result["bet"].is_win)
        self.assertEqual(result["bet"].win_amount, 0)
        self.assertEqual(result["player"].balance, 900)

    def test_invalid_bet_amount(self):
        player = Player(1, "max", 1000)
        horse = Horse(1, "Thunder", 90)

        with self.assertRaises(Exception):
            self._make_use_case(player).execute(
                user=None,
                selected_horse=horse,
                winner=horse,
                amount=-100,
                odds=2
            )

    def test_not_enough_money(self):
        player = Player(1, "max", 100)
        horse = Horse(1, "Thunder", 90)

        with self.assertRaises(Exception):
            self._make_use_case(player).execute(
                user=None,
                selected_horse=horse,
                winner=horse,
                amount=1000,
                odds=2
            )


# ---------------------------------------------------------------------------
# BetHistory
# ---------------------------------------------------------------------------

class BetHistoryUseCaseTest(TestCase):

    def test_sort_bets_by_date(self):
        player = Player(1, "max", 1000)
        horse = Horse(1, "Thunder", 90)

        bets = [
            Bet(player=player, horse=horse, amount=100, created_at=1),
            Bet(player=player, horse=horse, amount=200, created_at=3),
            Bet(player=player, horse=horse, amount=150, created_at=2),
        ]

        result = BetHistoryUseCase().execute(bets)

        self.assertEqual(result[0].amount, 200)
        self.assertEqual(result[1].amount, 150)
        self.assertEqual(result[2].amount, 100)