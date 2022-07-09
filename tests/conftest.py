import asyncio
import json
import logging
import os
from signal import SIGINT, SIGTERM
from typing import Optional, Union
import aiohttp
from aiohttp import WSCloseCode, WSServerHandshakeError, web
import multiprocessing
import nest_asyncio
import pytest
from time import sleep
from sub3 import Sub3

async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            match msg.data:
                case '{"data": "successful test"}':
                    confirmation = {'result': 'success'}
                    await ws.send_json(confirmation)
                    await asyncio.sleep(0.01)
                    data = {'result': 'data'}
                    await ws.send_json(data)
                    await ws.close()
                case '{"data": "unsuccessful test"}':
                    await ws.send_json({'error': "failure"})
                    await ws.close()
                case '{"data": "keepalive"}':
                    confirmation = {'result': 'success'}
                    await ws.send_json(confirmation)


    print('websocket connection closed')

    return ws

@pytest.fixture(autouse=True, scope="session")
def start_server():
    nest_asyncio.apply()
    app = web.Application()
    app.add_routes([web.get('/ws', websocket_handler)])
    p = multiprocessing.Process(target=web.run_app, args=(app, ))
    p.start()
    sleep(0.5)
    yield
    p.terminate()


class NewSub3(Sub3):

    def __init__(self,
                server_url: str,
                rpc: Union[str, dict],
                logger: Optional[logging.Logger] = None):
        super().__init__(server_url, rpc, logger)
        self.closed = False
        self.disconnected = False

    async def on_connect(self, connection_mess):
        self.connect = connection_mess

    async def on_request_error(self, error: str):
        self.request_error = error
        
    async def on_confirmation(self, confirmation: str):
        self.confirmation = confirmation

    async def on_data(self, raw_data: str):
        self.data = raw_data

    async def on_closed(self):
        self.closed = True

    async def on_disconnect(self):
        self.disconnected = True

class ErrSub3(Sub3):

    def __init__(self,
                server_url: str,
                rpc: Union[str, dict],
                exception: Exception,
                logger: Optional[logging.Logger] = None):
        super().__init__(server_url, rpc, logger)
        self.exception = exception
        self.connect_exception = False
        self.general_exception = False

    async def on_confirmation(self, confirmation: str):
        raise self.exception

    async def on_connection_error(self, error: str):
        self.connect_exception = True

    async def on_exception(self, exception: Exception):
        self.general_exception = True