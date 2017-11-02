import tornado.ioloop
import tornado.web
from tornado.httpclient import AsyncHTTPClient
from tornado.httpserver import HTTPServer
from tornado.web import RequestHandler
from tornado.ioloop import IOLoop


class IORequestHandler(RequestHandler):
    async def get(self):
        delay = self.get_query_argument('delay', '')
        http_client = AsyncHTTPClient()
        await http_client.fetch(f'http://nginx/{delay}')
        self.write('Request finished!')


class CPURequestHandler(RequestHandler):
    async def get(self):
        iterations = int(self.get_query_argument('iterations', '0'))
        for _ in range(iterations):
            iterations -= 1
        self.write('Request finished!')


def make_app():
    return tornado.web.Application([
        (r"/io", IORequestHandler),
        (r"/cpu", CPURequestHandler),
    ])


def run():
    AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
    http_server = HTTPServer(make_app())
    http_server.bind(5000)
    http_server.start(0)
    IOLoop.current().start()


if __name__ == "__main__":
    run()
