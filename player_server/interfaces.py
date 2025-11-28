"""this module holds interfaces and protocols for different classes to avoid circular imports"""

from abc import ABC, abstractmethod

from models import Answer

class MasterClientInterface(ABC):

    @abstractmethod
    def get_player_id(self) -> str:
        ...
    
    @abstractmethod
    def init_game(self, min:int, max:int) -> str:
        """initialize a new game and return the new player id"""
        ...
    
    @abstractmethod
    def guess(self) -> Answer:
        """submit a guess to the game master"""
        ...
    
    @abstractmethod
    def get(self, headers: dict=None, json: dict=None):
        """send a GET request to the game master"""
        ...

class PlayerInterface(ABC):
    strategy        : GuessStrategy
    master_client   : MasterClientInterface

    @abstractmethod
    def get_player_id() -> str:
        ...
    
    @abstractmethod
    def set_player_id() -> str:
        ...
    
    @abstractmethod
    def init_game(self, game_min:int, game_max: int) -> None:
        ...
    
    @abstractmethod    
    def add_guess(self, guess: int, Answer: Answer) -> None:
        ...
    
    @abstractmethod
    def summarize_history(self) -> dict:
        ...
    
    @abstractmethod
    def get_last_answer(self) -> Answer:
        ...
    
    @abstractmethod
    def take_guess(self, guess: int) -> Answer:
        ...
    
    @abstractmethod
    def play_game(self):
        ...
    

class GuessStrategy(ABC):
    lower_bin = None
    upper_bin = None

    @abstractmethod
    def next_guess(self, player: PlayerInterface):
        ...
