from .quiz import QuizGameType
from .puzzle import PuzzleGameType
from .math import MathGameType
from .memory import MemoryGameType


GAME_TYPES = {
    'quiz': QuizGameType,
    'puzzle': PuzzleGameType,
    'math': MathGameType,
    'memory': MemoryGameType,
}

def get_game_type(game_type):

    game_class = GAME_TYPES.get(
        game_type.key
    )

    if not game_class:
        raise ValueError(
            f"Unknown game type: {game_type.key}"
        )

    return game_class