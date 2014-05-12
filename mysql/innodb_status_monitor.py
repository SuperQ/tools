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
import re

log_dir = "/test-data/innodb-engine-status/"
log_file_tmpl = "IES-" + platform.node()
log_line_tmpl = "Logging to: %s trx_counter=%s purge_done=%s history_lenght=%s"

run_log = open(log_dir + "run.log", 'a')

wait_time = 1.0

trx_counter_re = re.compile("^Trx id counter ")
purge_done_re  = re.compile("^Purge done for trx's n:o ")
history_re     = re.compile("^History list length ")

db = MySQLdb.connect(read_default_file="~/.my.cnf")

cur = db.cursor()

while True:
  cur.execute("SHOW ENGINE INNODB STATUS")
  now = datetime.datetime.now()
  innodb_status = cur.fetchone()[2]
  innodb_status_lines = innodb_status.splitlines()
  trx_counter = filter(trx_counter_re.search, innodb_status_lines)[0].split()[3]
  purge_done = filter(purge_done_re.search, innodb_status_lines)[0].split()[6]
  history_length = filter(history_re.search, innodb_status_lines)[0].split()[3]
  logfile = log_file_tmpl + now.strftime("-%Y-%m-%d_%H%M%S.%f.log.gz")
  log_line = log_line_tmpl % (logfile, trx_counter, purge_done, history_length)
  print log_line
  run_log.write(log_line + "\n")
  f = gzip.open(log_dir + logfile, "w")
  f.write(innodb_status)
  f.close()
  time.sleep(wait_time)
