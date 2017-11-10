from aiohttp import web, ClientRequest, ClientSession, TCPConnector

import asyncio
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def io_handler(request: ClientRequest):
    delay = request.query.get('delay', '')
    client = ClientSession(
        connector=TCPConnector(limit=10000)
    )
    async with client as session:
        async with session.get(f'http://nginx/{delay}') as response:
            await response.read()
    return web.Response(text='Request finished!')


async def cpu_handler(request: ClientRequest):
    iterations = int(request.query.get('iterations', '0'))
    for _ in range(iterations):
        iterations -= 1
    return web.Response(text='Request finished!')


app = web.Application()
app.router.add_route('GET', '/io', io_handler)
app.router.add_route('GET', '/cpu', cpu_handler)


if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=80)
