#!/usr/bin/env bash

wrk -t2 -c${3} -d${4} -R2000 --latency http://${1}:80/${2} > ${5}
