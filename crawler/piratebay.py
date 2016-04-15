#!/usr/bin/env python

import requests
import time
from BeautifulSoup import BeautifulSoup
import sys
import os
import random

tpb_link = "https://thepiratebay.se/recent"

if not os.path.exists( "piratebay_daily.txt" ):
  os.mknod( "piratebay_daily.txt" )

if not os.path.exists( "kickass_daily.txt" ):
  os.mknod( "kickass_daily.txt" )

with open("piratebay_daily.txt", "r") as pbd2:
  content = pbd2.readlines()

with open("kickass_daily.txt", "r") as kad:
  kat_content = kad.readlines()

s = requests.Session()

magnets = []
day = False
download = []

user_agents = [
	'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
	'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16'
]

# This is the initial recent crawl (without a site number in the URL)
try:
  headers = {
    'User-Agent': random.choice(user_agents),
  }

  r = s.get( tpb_link, headers=headers, verify=False)
  data = r.content
  parsed = BeautifulSoup(data)
except Exception, e:
  print e
  #sys.exit()

for c in parsed.findAll('a', href=True):
  link = c.get('href')

  # Found a magnet link on piratebay
  if "magnet:?" in link:
    magnets.append( link )

for magnet in magnets:

  info_hash = (magnet.split("urn:btih:")[1])[:40].upper()
  
  # If info hash already in the TPB file, break the whole crawl
  for con in content:
    if info_hash.lower() in con:
      sys.exit("The info hash " + str(info_hash) + " is already in the piratebay file")
      break

    else:
      continue

  # If info hash already in the kickass file, break the whole crawl
  for kat in kat_content:
    if info_hash.lower() in kat:
      #sys.exit("The info hash " + str(info_hash) + " is already in the kickass file")
      break

    else:
      continue

  # Enter the date
  if day == False:
    day = True
    with open("piratebay_daily.txt", "a") as pbd:
      pbd.write( "\n### " + str( time.strftime( "%a, %d %b %Y %T %z" ) ) + " ###\n")
    
  # If it's not already in there, append the magnet link
  with open("piratebay_daily.txt", "a") as pbd3:
    pbd3.write( str(magnet) + '\n')

  # And append the info hash for later download
  download.append( info_hash )

s = requests.Session()

# go through the last 30 pages in recent
i=1
while i<=32:

  time.sleep(1)

  magnets = []

  try:
    headers = {
      'User-Agent': random.choice(user_agents),
    }

    r = s.get( tpb_link + "/" + str(i), headers=headers, verify=False )
    data = r.content
    parsed = BeautifulSoup(data)
  except Exception, e:
    print e
    #sys.exit()

  for c in parsed.findAll('a', href=True):
    link = c.get('href')
  
    # Found a magnet link on piratebay
    if "magnet:?" in link:
      magnets.append( link )
  
  for magnet in magnets:
  
    info_hash = (magnet.split("urn:btih:")[1])[:40].upper()
    
    # If info hash already in the TPB file, break the whole crawl
    for con in content:
      if info_hash.lower() in con:
        sys.exit("The info hash " + str(info_hash) + " is already in the piratebay file")
        break
  
      else:
        continue
  
    # If info hash already in the kickass file, break the whole crawl
    for kat in kat_content:
      if info_hash.lower() in kat:
        #sys.exit("The info hash " + str(info_hash) + " is already in the kickass file")
        break
  
      else:
        continue
      
    # If it's not already in there, append the magnet link
    with open("piratebay_daily.txt", "a") as pbd3:
      pbd3.write( str(magnet) + '\n')

    # And append the info hash for later download
    download.append( info_hash )

  i+=1

download = set(download)

# So download all the daily torrents from torcache (if there)
# If a download fails, its written to a textfile (failed_torcache_tpb_kickass.txt)
for torcache in download:
  t_link = "https://torcache.net/torrent/" + torcache +".torrent"

  os.system("python torcache_tpb_kickass.py " + t_link + " &")

  time.sleep( random.randint(1,3) )
