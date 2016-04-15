#!/usr/bin/env python

import os
import random
import time

all_hashes = []

# This is the failed file -> contains tc links
with open("failed_torcache_tpb_kickass.txt", "r") as f1:
  content = f1.read().splitlines()

for c in content:
  all_hashes.append( (c.split("https://torcache.net/torrent/")[1][:40]).upper() )


# Get the hashes out of the daily kickass and piratebay crawl
with open("kickass_daily.txt", "r") as f2:
  content = f2.read().splitlines()

for c in content:
  if "magnet" in c:
    all_hashes.append( (c.split("magnet:?xt=urn:btih:")[1][:40]).upper() )
  else:
    continue


# Get the hashes out of the daily kickass and piratebay crawl
with open("piratebay_daily.txt", "r") as f3:
  content = f3.read().splitlines()

for c in content:
  if "magnet" in c:
    all_hashes.append( (c.split("magnet:?xt=urn:btih:")[1][:40]).upper() )
  else:
    continue

# kill duplicates
all_hashes = set(all_hashes)


# Get the already downloaded torrents to skip them
already_there = []

for root, directories, filenames in os.walk('.'):
  for filename in filenames: 
    if str(os.path.join(filename))[40:] == ".torrent":
      already_there.append( str(os.path.join(filename))[:40] )

already_there = set(already_there)

# Now the final list to download
to_get = all_hashes - already_there

print "Re-Loading " + str(len(to_get)) + " torrents"

# kickoff the download
for torcache in to_get:
  t_link = "https://torcache.net/torrent/" + torcache +".torrent"

  os.system("python failed_torcache_tpb_kickass.py " + t_link + " &")

  time.sleep( random.randint(1,3) )
