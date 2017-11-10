#!/usr/bin/env sh

echo "GET http://${1}/${2}" | vegeta attack -rate=100 -duration=30s -output ${3}
