import aiohttp
from aiohttp import web

async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                data = {'some': 'data'}
                await ws.send_json(data)
                #await ws.close()
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                    ws.exception())

    print('websocket connection closed')

    return ws

app = web.Application()
app.add_routes([web.get('/ws', websocket_handler)])
web.run_app(app)