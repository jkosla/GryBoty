from src.bots.example_bots.example_bot import Bot
from src.two_player_games.move import Move
from src.two_player_games.state import State


class Bot_1(Bot):
    def get_move(self, state: State) -> Move:
        move = 1
        return move
