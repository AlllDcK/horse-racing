from core.repositories.interfaces import HorseRepositoryInterface
from core.services.odds_service import OddsService
from core.use_cases.run_race import RunRaceUseCase
from core.use_cases.place_bet import PlaceBetUseCase
from core.use_cases.deposit import DepositUseCase
from core.use_cases.withdraw import WithdrawUseCase
from core.use_cases.bet_history import BetHistoryUseCase

from races.repositories import (
    HorseRepository,
    PlayerRepository,
    BetRepository
)


class UseCaseFactory:

    @staticmethod
    def place_bet() -> PlaceBetUseCase:
        return PlaceBetUseCase(
            player_repo=PlayerRepository(),
            bet_repo=BetRepository()
        )

    @staticmethod
    def run_race() -> RunRaceUseCase:
        return RunRaceUseCase()

    @staticmethod
    def deposit() -> DepositUseCase:
        return DepositUseCase(
            player_repo=PlayerRepository()
        )

    @staticmethod
    def withdraw() -> WithdrawUseCase:
        return WithdrawUseCase(
            player_repo=PlayerRepository()
        )

    @staticmethod
    def bet_history() -> BetHistoryUseCase:
        return BetHistoryUseCase()

    @staticmethod
    def horse_repo() -> HorseRepositoryInterface:
        return HorseRepository()

    @staticmethod
    def player_repo():
        return PlayerRepository()

    @staticmethod
    def bet_repo():
        return BetRepository()