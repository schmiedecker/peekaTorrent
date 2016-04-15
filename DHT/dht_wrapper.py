#!/usr/bin/env python

import os
from os.path import isfile, join, abspath
from os import listdir
import time
import subprocess
import sys

if len(sys.argv) < 2:
  sys.exit("Please supply the openbay hashset directory")

openbay_hashset = sys.argv[1]

onlyfiles = [ f for f in listdir( openbay_hashset ) if isfile(join( openbay_hashset, f)) ]

for o in onlyfiles:
  path = abspath( o )

  os.system("python dht_client.py " + path + " &")

  time.sleep(1)
