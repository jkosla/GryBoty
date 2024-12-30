from src.bots.example_bots.example_bot import Bot
from src.two_player_games.move import Move
from src.two_player_games.state import State
from src.two_player_games.games.nim import NimMove


class Bot_1(Bot):
    def get_move(self, state: State) -> Move:
        move = NimMove(2, 1)
        return move
