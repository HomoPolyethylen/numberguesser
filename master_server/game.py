import uuid
import random
from typing import List, Tuple

from models import Answer

class Game:
    player  : str
    number  : int
    MIN     : int
    MAX     : int
    guesses : List[Tuple[int, Answer]] # [(42, "higher"), (420, "lower"), ...]

    def __init__(self,
                 game_min: int = 1,
                 game_max: int = 1000):
        self.player = str(uuid.uuid4())
        self.MIN = game_min
        self.MAX = game_max
        self.number = int(self.MIN + random.random() * abs(self.MAX - self.MIN))
        self.guesses = []