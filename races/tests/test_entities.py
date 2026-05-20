from django.test import TestCase

from core.entities.bet import Bet
from core.entities.horse import Horse
from core.entities.player import Player


class HorseEntityTest(TestCase):

    def test_create_horse(self):
        horse = Horse(
            id=1,
            name="Thunder",
            base_speed=95
        )

        self.assertEqual(horse.id, 1)
        self.assertEqual(horse.name, "Thunder")
        self.assertEqual(horse.base_speed, 95)


class PlayerEntityTest(TestCase):

    def test_create_player(self):
        player = Player(
            id=1,
            username="max",
            balance=5000
        )

        self.assertEqual(player.id, 1)
        self.assertEqual(player.username, "max")
        self.assertEqual(player.balance, 5000)


class BetEntityTest(TestCase):

    def test_create_bet(self):
        player = Player(
            id=1,
            username="max",
            balance=5000
        )

        horse = Horse(
            id=1,
            name="Thunder",
            base_speed=95
        )

        bet = Bet(
            player=player,
            horse=horse,
            amount=1000,
            is_win=True,
            win_amount=2500
        )

        self.assertEqual(bet.player.username, "max")
        self.assertEqual(bet.horse.name, "Thunder")
        self.assertEqual(bet.amount, 1000)
        self.assertTrue(bet.is_win)
        self.assertEqual(bet.win_amount, 2500)