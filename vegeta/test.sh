#!/usr/bin/env sh

echo "GET http://${1}/${2}" | vegeta attack -rate=${3} -duration=${4} -output ${5}
