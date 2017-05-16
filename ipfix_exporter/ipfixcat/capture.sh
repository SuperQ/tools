#!/bin/bash

port="$1"

if [[ -z "${port}" ]] ; then
  echo "usage: $(basename $0) <port>"
  exit
fi

set -o pipefail

socat "udp-recv:${port}" stdout \
  | /srv/ipfixcat/ipfixcat -dict procera-fields.ini \
  | /srv/ipfixcat/parse-flow.py >> "/srv/ipfixcat/log/flows-${port}.log"
