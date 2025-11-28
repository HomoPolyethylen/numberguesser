#!/usr/bin/env python

import httpx

def test_health(get_player_testing_client):
    r = get_player_testing_client.get("/health")

    assert r.status_code == httpx.codes.OK
    assert r.json() == "healthy"


def test_ping_master(get_player_testing_client):
    r = get_player_testing_client.get("/ping-master")
    
    assert r.status_code == httpx.codes.OK
    assert r.json() == {"player received": "pong"}

def test_play(get_player_testing_client):
    r = get_player_testing_client.get("/play", params={"game_min": 1, "game_max": 20})

    assert r.status_code == httpx.codes.OK
    assert "number of guesses" in r.json()