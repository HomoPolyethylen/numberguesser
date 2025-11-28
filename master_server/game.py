import uuid
import random
from typing import List, Tuple

from models import Answer

class Game:
    player: str
    number: int | None = None
    MIN: int | None = None
    MAX: int | None = None
    guesses: List[Tuple[int, Answer]] = [] # [(42, "higher"), (420, "lower"), ...]

    def __init__(self,
                 min: int = 1,
                 max: int = 1000):
        self.player = str(uuid.uuid4())
        self.MIN = min
        self.MAX = max
        self.number = int(self.MIN + random.random() * abs(self.MAX - self.MIN))
