from abc import ABC, abstractmethod


class HorseRepositoryInterface(ABC):

    @abstractmethod
    def get_all(self) -> list:
        pass


class PlayerRepositoryInterface(ABC):

    @abstractmethod
    def get_by_user(self, user) -> object:
        pass

    @abstractmethod
    def save(self, user, player) -> None:
        pass


class BetRepositoryInterface(ABC):

    @abstractmethod
    def create(self, user, bet) -> None:
        pass

    @abstractmethod
    def get_user_bets(self, user) -> list:
        pass