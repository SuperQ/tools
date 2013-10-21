#!/bin/bash
#
# Author: Ben Kochie <ben@nerp.net>
#
# Description: Setup a policy route

usage() {
  echo "usage: $(basename $0) [-d] <routing table> <gateway> <network interface>"
  echo "  gateway and interwork interface only needed for add"
}

delete=0
if [ "$1" = "-d" ] ; then
  delete=1
  shift 1
  if [ $# -ne 1 ] ; then
    usage
    exit 1
  fi
else
  if [ $# -ne 3 ] ; then
    usage
    exit 1
  fi
fi

table="$(egrep -v '^(#|$)' /etc/iproute2/rt_tables | awk "\$2 == \"$1\" {print \$2}")"
if [ -z "${table}" ] ; then
  echo "ERROR: invalid table $1"
  echo "  You must add the table name to '/etc/iproute2/rt_tables'"
  usage
  exit 1
fi

if [ "${delete}" -eq 0 ] ; then
  gateway="$2"
  if [ -z "${gateway}" ] ; then
    echo "ERROR: invalid gateway ${gateway}"
    usage
    exit 1
  fi
  interface="$3"
  ip link show dev "${interface}" > /dev/null 2>&1
  if [ $? -gt 0 ] ; then
    echo "ERROR: invalid interface ${interface}"
    usage
    exit 1
  fi
  
  network="$(ip route show dev "${interface}" | awk '{print $1}')"
  if [ -z "${network}" ] ; then
    echo "ERROR: invalid gateway ${network}"
    usage
    exit 1
  fi
  
  address="$(ip addr show dev "${interface}" primary \
             | awk '$1 == "inet" {print $2}' | cut -f1 -d'/')"
  if [ -z "${address}" ] ; then
    echo "ERROR: invalid gateway ${address}"
    usage
    exit 1
  fi
  
  table_test=$(ip route show table "${table}" 2> /dev/null)
  if [ -n "${table_test}" ] ; then
    echo "Table ${table} already configured"
    exit
  fi

  echo "Found network ${network}, address ${address}"
  ip route add "${network}" dev "${interface}" src "${address}" table "${table}"
  ip route add default via "${gateway}" dev "${interface}" table "${table}"
  ip rule add from "${address}"/32 table "${table}"
  ip rule add to "${address}"/32 table "${table}"
else
  ip rule del table "${table}"
  ip rule del table "${table}"
fi
