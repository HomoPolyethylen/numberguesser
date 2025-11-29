import pytest
from fastapi.testclient import TestClient

from player_server import app as player_app
from master_server import app as master_app
from player_server.proxy import MasterClientHttpx, get_master_client

@pytest.fixture
def get_master_testing_client():
    yield TestClient(master_app)

@pytest.fixture
def get_player_testing_client(get_master_testing_client: TestClient):

    class HttpxTestingClient(MasterClientHttpx):
        """this overrides the proxys Client during initialisation"""
        def __init__(self):
            self._client = get_master_testing_client

    def get_master_client_override():
        # return get_master_testing_client
        return HttpxTestingClient()

    player_app.dependency_overrides[get_master_client] = get_master_client_override
    yield TestClient(player_app)
    player_app.dependency_overrides.clear()

