#!/usr/bin/env python

"""Tests for `Web3_Subscriber` package."""

import json
import logging
import os
import threading
import aiohttp
from signal import SIGINT
import time
from tests.conftest import NewSub3, ErrSub3

# from web3_subscriber import RPCMaker, SubscriberClient


async def test_successful_request():

    sub = NewSub3("http://127.0.0.1:8080/ws", {"data":"successful test"})
    
    sub.start()

    assert sub.connect == "connected"
    assert json.loads(sub.data) == {"result": "data"}
    assert json.loads(sub.confirmation) == {"result": "success"}    
    assert sub.closed == True
    assert sub.disconnected == True

async def test_failed_request():

    sub = NewSub3("http://127.0.0.1:8080/ws", {"data":"unsuccessful test"})
    
    sub.start()

    assert json.loads(sub.request_error) == {'error': "failure"}   

async def test_text_rpc_and_logger():

    logger = logging.Logger("test_logger")
    rpc = json.dumps({"data":"successful test"})
    sub = NewSub3("http://127.0.0.1:8080/ws", rpc, logger=logger)
    sub.start()
    assert json.loads(sub.data) == {"result": "data"}

async def test_connection_error():

    sub = ErrSub3("http://127.0.0.1:8080/ws",
                 {"data":"successful test"},
                 aiohttp.ClientConnectionError)
    sub.start()

    assert sub.connect_exception == True

async def test_general_error():

    sub = ErrSub3("http://127.0.0.1:8080/ws",
                 {"data":"successful test"},
                 ValueError)
    sub.start()

    assert sub.general_exception == True

async def test_signal_handling():

    pid = os.getpid()

    def trigger_signal():
        time.sleep(1)
        os.kill(pid, SIGINT)

    thread = threading.Thread(target=trigger_signal)
    thread.daemon = True
    thread.start()

    sub = NewSub3("http://127.0.0.1:8080/ws",
                 {"data":"keepalive"})
    sub.start()