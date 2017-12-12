#!/usr/bin/env python3

from argparse import ArgumentParser
from subprocess import run, PIPE, DEVNULL
import time

SERVERS = [
    'aiohttp',
    'dropwizard',
    'express',
    'flask',
    'go-stdlib',
    'php',
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
    parser.add_argument('-r', '--rate', default=100, help="Number of concurrent requests")
    parser.add_argument('-d', '--duration', default=30, help="Duration in seconds")
    args = parser.parse_args()
    return args


def start(args):
    print('Starting...')
    run(['docker-compose', 'down', '-v'])
    for server in args.servers:
        benchmark_server(server, args.rate, args.duration)
    print('Done!')


def get_running_containers():
    result = run(['docker', 'ps', '--format={{.Names}}'], stdout=PIPE)
    return [container for container in result.stdout.decode('utf-8').split('\n') if container]


def benchmark_server(server, rate, duration):
    print("Benchmarking {}".format(server))
    run(['docker-compose', 'up', '-d', server], stdout=DEVNULL, stderr=DEVNULL)
    time.sleep(15)
    for endpoint in ENDPOINTS:
        print(f'\tTesting {endpoint}')
        base_command = "/test.sh {server} {endpoint} {rate} {duration}".format(
            server=server,
            endpoint=endpoint,
            rate=rate,
            duration=f'{duration}s',
        ).split(' ')
        vegeta_command = base_command + ['/results/{}_{}_veg.bin'.format(server, endpoint.replace('?', ''))]
        wrk2_command = base_command + ['/results/{}_{}_wrk.txt'.format(server, endpoint.replace('?', ''))]
        run(['docker-compose', 'run', 'vegeta'] + vegeta_command, stdout=DEVNULL, stderr=DEVNULL)
        run(['docker-compose', 'run', 'wrk2'] + wrk2_command, stdout=DEVNULL, stderr=DEVNULL)
    containers = get_running_containers()
    stats_command = ['docker', 'stats',  '--no-stream'] + containers
    print(stats_command)
    stats_result = run(stats_command, stdout=PIPE, stderr=DEVNULL)
    print(stats_result.stdout.decode('utf-8'))
    # TODO store stats_result
    run(['docker-compose', 'down', '-v'], stdout=DEVNULL, stderr=DEVNULL)


if __name__ == '__main__':
    start(get_args())
