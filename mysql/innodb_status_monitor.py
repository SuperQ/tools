#!/usr/bin/python
#
# Description: Quick and dirty polling of "SHOW ENGINE INNODB STATUS"
#
# Author: Ben Kochie <bjk@soundcloud.com>

import MySQLdb
import datetime
import time
import gzip
import platform

log_dir = "/test-data/innodb-engine-status/"

log_file_template = "IES-" + platform.node()

wait_time = 1.0

db = MySQLdb.connect(read_default_file="~/.my.cnf")

cur = db.cursor()

while True:
  cur.execute("SHOW ENGINE INNODB STATUS")
  now = datetime.datetime.now()
  logfile = log_file_template + now.strftime("-%Y-%m-%d_%H%M%S.%f.log.gz")
  print "Logging to: " + logfile 
  f = gzip.open(log_dir + logfile, 'w')
  f.write(cur.fetchone()[2])
  f.close()
  time.sleep(wait_time)
