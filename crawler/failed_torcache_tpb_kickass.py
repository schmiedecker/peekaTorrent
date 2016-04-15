#!/usr/bin/env python

import requests
import time
import sys
from BeautifulSoup import BeautifulSoup
import os
import random

# Which torrent to download from torcache
if len(sys.argv) < 2:
  sys.exit("Too few arguments")

torrent = sys.argv[1]
#torrent = "https://torcache.net/torrent/E18678A1AFDDD84844B2EFDC5E493F698F0BF576.torrent"

s = requests.Session()

user_agents = [
	'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
	'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16'
]

# Harvest all the category links
try:
  headers = {
    'User-Agent': random.choice(user_agents),
  }

  r = s.get(torrent, headers=headers)
  data = r.content

except Exception, e:
  print e
  #print "The exception happened in the torcache stuff"

  # since (almost) all of the errors happen here, I will save a list for later access
  with open( "still_failed_torcache_tpb_kickass.txt", "a") as ftc:
    ftc.write( str(torrent) + "\n")

  sys.exit()

if "DOCTYPE" in data:
  with open( "still_failed_torcache_tpb_kickass_404.txt", "a") as ftc:
    ftc.write( str(torrent) + "\n")

  sys.exit()

torrentname = torrent.split("torrent/")[1][:40]


# If not already there: create daily directory structure
torrentdir = str(time.strftime("%d%m%Y")) + "reCheck"

if not os.path.exists(torrentdir):
  os.makedirs( torrentdir )

if not os.path.exists(torrentdir + "/torrents/" ):
  os.makedirs( torrentdir + "/torrents/" )


with open(torrentdir + '/torrents/' + torrentname + ".torrent", 'wb') as f:
  f.write(data)
