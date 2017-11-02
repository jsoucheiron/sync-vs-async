from aiohttp import ClientSession, TCPConnector
from sanic import Sanic
from sanic.response import text

app = Sanic()


@app.route("/io")
async def io_handler(request):
    delay = request.args.get('delay', '')
    client = ClientSession(
        connector=TCPConnector(limit=10000)
    )
    async with client as session:
        async with session.get(f'http://nginx/{delay}') as response:
            await response.read()
    return text('Request finished!')


@app.route('/cpu')
async def cpu_handler(request):
    iterations = int(request.args.get('iterations', '0'))
    for _ in range(iterations):
        iterations -= 1
    return text('Request finished!')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, workers=4)
