from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/io')
def io_handler():
    delay = request.args.get('delay', '')
    requests.get(f'http://nginx/{delay}')
    return 'Request finished!'


@app.route('/cpu')
def cpu_handler():
    iterations = int(request.args.get('iterations', '0'))
    for _ in range(iterations):
        iterations -= 1
    return 'Request finished!'


if __name__ == '__main__':
    app.run()
