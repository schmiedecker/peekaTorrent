#!/usr/bin/env python

###########################################################
#                                                         #
# (PoC) Torrent Chunk Hash Extract0r                      #
#                                                         #
# This script parses torrent infos (by using bencode)     #
# Extract piece length distribution                       #
# Extract piece hashes and prints to stdout               #
#                                                         #
# Input:                                                  #
#   - A directory containing torrents. The naming         #
#     convention of those torrents is <info_hash>.torrent #
#                                                         #
# Called:                                                 #
# python2 hash_extract0r.py <directory of torrents>       #
#                                                         #
# Output:                                                 #
#   - All chunk hashes, printed to stdout                 #
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


# Check if torrent directory is supplied
if len(sys.argv) < 2:
  sys.exit("Too few arguments. Please supply the torrent directory")

torrentdir = sys.argv[1]

torrent_abspath = abspath(torrentdir)



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

    # some variable we will use later
    old_pieces = 0
    sha1_length = 20
    piece_length = metainfo['info']['piece length']



    if multifile == True:
      # Do multifile stuff here


      try:
        pieces = metainfo['info']['pieces']
        hashes = [pieces[i:i+sha1_length] for i in range(0, len(pieces), sha1_length)]
      except Exception, e:
        print e
        print "at file " + str(torrentfile)
        continue


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

        # print filename, infohash and piece length
        print "#", str(filename), "\t", str(torrentHash), "\t", str(piece_length)

	counter = 0
        # Iterate through the hashes and print them
        for h in file_hashes:
	  counter += 1
	  print str(torrentHash) + "\t" + str(hexlify(h)) + "\t" + str(counter)


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


      try:
      	pieces = metainfo['info']['pieces']

        num_pieces = int(math.ceil(float(filelength)/float(piece_length)))
        hashes = [pieces[i:i+sha1_length] for i in range(0, len(pieces), sha1_length)]
      except Exception, e:
	print e
	print "at file " + str(torrentfile)
	continue

      # print filename, infohash and piece length
      print "#", str(torrentHash), "\t", str(torrentHash), "\t", str(piece_length)
  
      counter = 0
      # Iterate through the hashes and print them
      for h in hashes:
        counter += 1
        print str(filename) + "\t" + str(hexlify(h)) + "\t" + str(counter)






