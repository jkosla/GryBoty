from src.two_player_games.move import Move
from src.two_player_games.state import State
from abc import ABC, abstractmethod
from src.two_player_games.player import Player


class Bot(Player, ABC):
    @abstractmethod
    def get_move(self, state: State) -> Move:
        raise NotImplementedError


class ValidBot1(Bot):
    def get_move(self, state: State) -> Move:
        return list(state.get_moves())[0]
