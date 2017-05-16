#!/usr/bin/python
#
# Description: Parse IPFIX json from ipfixcat
# Author: Ben Kochie <superq@gmail.com>

import json
import sys

def parse_flow(flow):
  direction = 0
  src = ''
  src_port = 0
  dst = ''
  dst_port = 0
  packets = 0
  bytes = 0
  for field in flow:
    name = field['name']
    if name == 'destinationIPv4Address':
      dst = field['value']
    if name == 'destinationTransportPort':
      dst_port = field['value']
    if name == 'sourceIPv4Address':
      src = field['value']
    if name == 'sourceTransportPort':
      src_port = field['value']
    if name == 'packetDeltaCount':
      packets = byte_array_to_int(field['raw'])
    if name == 'octetDeltaCount':
      bytes = byte_array_to_int(field['raw'])
    if name == 'flowDirection':
      direction = field['value']

  print "%d %s:%d %s:%d %d %d" % (direction, src, src_port, dst, dst_port, packets, bytes)

def byte_array_to_int(raw):
  return (raw[0] << 24) + (raw[1] << 16) + (raw[2] << 8) + raw[3]

def main(argv):
  if sys.stdin.isatty():
    print 'This script expects json to stdin'
    print 'ex: knife search ... -F json | parse-flow.py'
    sys.exit(1)

  for line in sys.stdin:
    flow = json.loads(line)
    if flow['templateId'] in [1024, 1025]:
      parse_flow(flow['fields'])
    else:
      print "Unknown type: %d" % (flow['templateId'])

if __name__ == "__main__":
   main(sys.argv[1:])
