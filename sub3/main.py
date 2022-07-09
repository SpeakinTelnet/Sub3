import asyncio
import json
import logging
import signal
from typing import Optional, Union
from platform import python_version
import aiohttp

async def shutdown(signal, loop, log):
    """Cleanup tasks tied to the service's shutdown."""
    log.error(f"Received exit signal {signal.name}...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    log.error(f"Cancelling {len(tasks)} outstanding tasks")
    [task.cancel() for task in tasks]
    await asyncio.gather(*asyncio.all_tasks() - {asyncio.current_task()})
    loop.stop()


class Sub3:
    """
    Base connection client for asyncio JSON-RPC calls.

    :param server_url: URL of the node to connect to
    :type server_url: str
    :param rpc: Standard RPC PubSub
    :type rpc: Union[str, dict]

    .. seealso:: https://geth.ethereum.org/docs/rpc/pubsub

    """

    def __init__(self, server_url: str,
                 rpc: Union[str, dict],
                 logger: Optional[logging.Logger] = None):

        if isinstance(rpc, dict):
            self.rpc = json.dumps(rpc)
        else:
            self.rpc = rpc

        if not logger:
            logging.basicConfig(level=logging.INFO,
                    format='%(levelname)-8s %(message)s')
            self.log = logging.getLogger(__name__)
        else:
            self.log = logger

        self.server_url = server_url
        self.user_agent = (
            f"Python/{python_version()} " f"aiohttp/{aiohttp.__version__} "
        )

    def start(self, timeout=60):
        loop = asyncio.new_event_loop()
        signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
        for s in signals:
            loop.add_signal_handler(
                s, lambda s=s: loop.create_task(shutdown(s, loop, self.log))
            )
        try:
            loop.run_until_complete(self._start(timeout))
        finally:
            loop.close()

    async def _start(self, timeout: int):

        self.session = aiohttp.ClientSession(
            headers={"User-Agent": self.user_agent},
            timeout=aiohttp.ClientTimeout(sock_read=timeout),
        )

        try:
            async with self.session.ws_connect(self.server_url) as ws:
                await self.on_connect("connected")
                await ws.send_str(self.rpc)
                confirmation = await ws.receive()
                if "error" in confirmation.data:
                    await self.on_request_error(confirmation.data)
                    await self.session.close()
                    return
                await self.on_confirmation(confirmation.data)
                while True:
                    mess = await ws.receive()
                    match mess.type:
                        case aiohttp.WSMsgType.TEXT:
                            await self.on_data(mess.data)
                        case aiohttp.WSMsgType.CLOSED:
                            await self.on_closed()
                            return

        except (aiohttp.ClientConnectionError, aiohttp.ClientPayloadError) as err:
            await self.on_connection_error(err)
        except asyncio.CancelledError:
            return
        except Exception as err:
            await self.on_exception(err)
        finally:
            await self.session.close()
            await self.on_disconnect()

    async def on_connect(self, connection_mess):
        """This is called after a successfull connection"""

        self.log.info(connection_mess)

    async def on_request_error(self, error: str):
        """This is called when the rpc request returned an error"""

        self.log.error(error)

    async def on_confirmation(self, confirmation: str):
        """This is called when a confirmation is received from a successful
        RPC subscription"""

        self.log.info(confirmation)

    async def on_data(self, raw_data: str):
        """This is called to process the incoming data from the stream"""

        self.log.info(raw_data)

    async def on_closed(self):
        """This is called when the websocket has been closed"""

        self.log.error("Received a closed websocket message")

    async def on_connection_error(self, error: str):
        """This is called after a connection error from the websocket"""

        self.log.error(error)

    async def on_exception(self, exception: Exception):
        """This is called on an unknown exception"""

        self.log.error(repr(exception))

    async def on_disconnect(self):
        """This is called when the websocket has disconnected"""

        self.log.info("disconnected")
