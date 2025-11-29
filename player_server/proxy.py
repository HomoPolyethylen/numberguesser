"""this module holds implementations of the MasterClientInterface.

the player uses one of these to talk to the game master.
"""

import httpx
import os
from fastapi import HTTPException

from models import Answer
from .interfaces import MasterClientInterface


class MasterClientHttpx(MasterClientInterface):
    """this class represents an HTTP Client for the player to talk to the game master"""

    _client: httpx.Client

    def __init__(self, base_url: str):
        self._client = httpx.Client(base_url=base_url)

    def init_game(self, min: int = 1, max: int = 1000) -> str:
        r = self._client.get("/new-game", params={"min": min, "max": max})
        r.raise_for_status()
        return r.json()

    def guess(self, guess: int, player_id: str) -> Answer:
        r = self._client.get("/guess", headers={"player-id": player_id}, params={"guess": guess})
        r.raise_for_status()
        return r.json()
    
    def get(self, path: str, headers: dict|None=None, params: dict|None=None):
        try:
            r = self._client.get(path, headers=headers, params=params)
            r.raise_for_status()
            return r.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=503, detail=str(e))

#
# METHODS
#
def get_master_client() -> MasterClientInterface:
    """retrieves the client talking to the game master server
    """
    return MasterClientHttpx(base_url=os.getenv('GAME_MASTER_ADDR', default="http://127.0.0.1:8000"))
