#!/usr/bin/env python

import httpx

def test_ping(get_master_testing_client):
    r = get_master_testing_client.get("/ping")
    
    assert r.status_code == httpx.codes.OK
    assert r.json() == "pong"

def test_new_game(get_master_testing_client):
    r = get_master_testing_client.get("/new-game")

    assert r.status_code == httpx.codes.CREATED
    assert "player-id" in r.json()

def test_new_game_min_max(get_master_testing_client):
    r = get_master_testing_client.get("/new-game", params={"min": 1, "max": 20})

    assert r.status_code == httpx.codes.CREATED
    assert "player-id" in r.json()