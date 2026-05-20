from .models import (
    Horse as HorseModel,
    Profile,
    Bet as BetModel
)

from core.entities.horse import Horse
from core.entities.player import Player
from core.entities.bet import Bet


class HorseRepository:

    def get_all(self):
        horses = HorseModel.objects.all()

        return [
            Horse(
                id=h.id,
                name=h.name,
                speed=h.base_speed
            )
            for h in horses
        ]


class PlayerRepository:

    def get_by_user(self, user):
        profile, _ = Profile.objects.get_or_create(user=user)

        return Player(
            id=user.id,
            username=user.username,
            balance=profile.balance
        )

    def save(self, user, player):
        profile = Profile.objects.get(user=user)

        profile.balance = player.balance
        profile.save()


class BetRepository:

    def create(self, user, bet):
        horse = HorseModel.objects.get(id=bet.horse.id)

        BetModel.objects.create(
            user=user,
            horse=horse,
            amount=bet.amount,
            is_win=bet.is_win,
            win_amount=bet.win_amount
        )

    def get_user_bets(self, user):
        bets = BetModel.objects.filter(
            user=user
        ).select_related('horse').order_by('-created_at')

        return [

            Bet(
                player=None,
                horse=Horse(
                    id=bet.horse.id,
                    name=bet.horse.name,
                    speed=bet.horse.base_speed
                ),
                amount=bet.amount,
                is_win=bet.is_win,
                win_amount=bet.win_amount,
                created_at=bet.created_at
            )

            for bet in bets
        ]
