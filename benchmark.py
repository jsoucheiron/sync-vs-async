#!/usr/bin/env python

from argparse import ArgumentParser
import subprocess
import time

SERVERS = [
    'aiohttp',
    'express',
    'flask',
    'go-stdlib',
    'sanic',
    'tornado'
]

ENDPOINTS = [
    'io?delay=100ms',
    'io?delay=200ms',
    'io?delay=1s',
    'cpu?iterations=100',
    'cpu?iterations=500000'
]

def get_args():
    parser = ArgumentParser(description='Run the benchmarks on the given servers')
    parser.add_argument(
        "--servers", default=SERVERS, choices=SERVERS, nargs='*',
        help="Servers to run the benchmarks on"
    )
    args = parser.parse_args()
    return args


def run(args):
    print('Starting...')
    subprocess.call(['docker-compose', 'down', '-v'])
    for server in args.servers:
        benchmark_server(server)
    print('Done!')


def benchmark_server(server):
    print("Benchmarking {}".format(server))
    subprocess.call(['docker-compose', 'up', '-d', server])
    time.sleep(15)
    for endpoint in ENDPOINTS:
        vegeta_command = "/test.sh {server} {endpoint} {result_name}".format(
            server=server,
            endpoint=endpoint,
            result_name='/results/{}_{}'.format(server, endpoint.replace('?', ''))
        ).split(' ')
        subprocess.call(['docker-compose', 'run', 'vegeta'] + vegeta_command)
    subprocess.call(['docker-compose', 'down', '-v'])

if __name__ == '__main__':
    run(get_args())
