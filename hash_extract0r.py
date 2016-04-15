#!/usr/bin/env python

###########################################################
#                                                         #
# (PoC) Torrent Chunk Hash Extract0r                      #
#                                                         #
# This script parses torrent infos (by using bencode)     #
# Extract piece length distribution                       #
# Extract piece hashes and save them into DB              #
# Create an Index on the table hashes                     #
#                                                         #
# Input:                                                  #
#   - A directory containing torrents. The naming         #
#     convention of those torrents is <info_hash>.torrent #
#                                                         #
# Called:                                                 #
# python2 hash_extract0r.py <directory of torrents>       #
#                                                         #
# Output:                                                 #
#   - A mysql DB, filled with the chunk hashes of         #
#     the torrents supplied                               #
#                                                         #
# (c) 2016                                                #
#                                                         #
# License: GPL v2                                         #
#                                                         #
###########################################################

import bencode
import sys
import math
from binascii import hexlify, unhexlify
import os
from os import listdir
from os.path import isfile, join, abspath
from collections import Counter
import MySQLdb

# Check if torrent directory is supplied
if len(sys.argv) < 2:
  sys.exit("Too few arguments. Please supply the torrent directory")

torrentdir = sys.argv[1]

torrent_abspath = abspath(torrentdir)


cnt = Counter()


# Setup and connect the DB
db = MySQLdb.connect(host="localhost",
                     user="torrent",
                     passwd="torrent",
                     db="torrentChunkHash")

c = db.cursor()

# Create the actual table "hashes" and correspondig "files" table
c.execute('CREATE TABLE IF NOT EXISTS hashes( Id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, InfoHash CHARACTER(40), ChunkHash CHARACTER(40) );')
c.execute('CREATE TABLE IF NOT EXISTS files( Id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, Filename TEXT, InfoHash CHARACTER(40), PieceLength CHARACTER(20) );')

for root, dirnames, filenames in os.walk(torrentdir):
  for torrentfile in filenames:

    # This check for files with duplicate name (results in "<hash> (1).torrent")
    if str(torrentfile)[:-8][-1:] == ")":
      torrentHash = (str(torrentfile)[:-12]).lower()
    else:
      torrentHash = (str(torrentfile)[:-8]).lower()

    torrentfilepath = abspath(root) + "/" + torrentfile

    # Open the torrent file and read it
    with open(torrentfilepath, "rb") as t:
      torrent = t.read()

    # Parse the torrent file
    # Sometimes torrents are fucked up -> try/catch/pass
    try:
      metainfo = bencode.bdecode(torrent)
    except:
      continue

    multifile = False

    for mf in metainfo['info']:
      if mf == "files":
        if len(metainfo['info']['files']) > 0:
          multifile = True

    old_pieces = 0

    if multifile == True:
      # Do multifile stuff here

      piece_length = metainfo['info']['piece length']

      cnt[piece_length] += 1

      sha1_length = 20
      pieces = metainfo['info']['pieces']
      hashes = [pieces[i:i+sha1_length] for i in range(0, len(pieces), sha1_length)]

      for files in metainfo['info']['files']:
        if len(files['path']) > 1:
          filename = str('/'.join(str(files['path'])))
        else:
          filename = files['path'][0]

        filelength = files['length']

        num_pieces = int(math.ceil(float(filelength)/float(piece_length)))
        file_hashes = hashes[:num_pieces]
        # Skip old pieces
        hashes = hashes[num_pieces:]

        # Save filename, infohash and piece length in the corresponding table
        c.execute("""INSERT INTO files(Filename, InfoHash, PieceLength) VALUES (%s, %s, %s);""", ( str(filename), str(torrentHash), str(piece_length) ) )

        # Iterate through the hashes and save them into the DB
        for h in file_hashes:
          c.execute("""INSERT INTO hashes(InfoHash, ChunkHash) VALUES (%s, %s);""", ( str(torrentHash), str(hexlify(h)) ) )


    else:
      # This branch is the single-file branch
      # Extract the details from the torrent used later on

      try:
        filename = metainfo['info']['name']
        filelength = metainfo['info']['length']
      except Exception, e:
        print e
        print "At file " + str(torrentfile)
        continue

      piece_length = metainfo['info']['piece length']

      cnt[piece_length] += 1

      pieces = metainfo['info']['pieces']

      num_pieces = int(math.ceil(float(filelength)/float(piece_length)))

      # Some of the torrents trigger this check...
      if len(pieces)/20 != num_pieces:
        with open("torrents_piece_mismatch.txt", "a") as fail:
          fail.write(str(torrentfile) + "\n")

      sha1_length = 20

      hashes = [pieces[i:i+sha1_length] for i in range(0, len(pieces), sha1_length)]

      # Save filename, infohash and piece length in the corresponding table
      c.execute("""INSERT INTO files(Filename, InfoHash, PieceLength) VALUES (%s, %s, %s);""", ( str(filename), str(torrentHash), str(piece_length) ) )

      # Iterate through the hashes and save them into the DB
      for h in hashes:
        c.execute("""INSERT INTO hashes(InfoHash, ChunkHash) VALUES (%s, %s);""", ( str(torrentHash), str(hexlify(h)) ) )

    db.commit()

db.commit()

c.execute("ALTER TABLE hashes ADD KEY(InfoHash);")

# Commit the remaining stuff and close the DB connection
db.commit()
db.close()
