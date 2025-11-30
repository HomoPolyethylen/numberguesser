"""this module holds interfaces and protocols for different classes to avoid circular imports"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import player
    import models

class MasterClientInterface(ABC):
    
    @abstractmethod
    def init_game(self, game_min:int, game_max:int) -> dict:
        """initialize a new game and return the new player id"""
        ...
    
    @abstractmethod
    def guess(self, guess: int, player_id: str) -> "models.Answer":
        """submit a guess to the game master"""
        ...
    
    @abstractmethod
    def get(self, path: str, headers: dict|None = None, json: dict|None = None) -> dict:
        """send a GET request to the game master"""
        ...
   

class GuessStrategy(ABC):
    lower_bin = None
    upper_bin = None

    @abstractmethod
    def next_guess(self, player: "player.Player") -> int:
        ...
