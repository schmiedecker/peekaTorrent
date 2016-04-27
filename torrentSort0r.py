#!/usr/bin/env python

import os, sys
import bencode

# Check if input and output directories are supplied
if len(sys.argv) < 3:
    sys.exit("Error: Too few arguments.\nUsage: torrentSort0r.py INPUTDIR OUTPUTDIR")

inputdir = sys.argv[1]
outputdir = sys.argv[2]

if not os.path.exists(outputdir):
    sys.exit("Error: Output directory does not exist") 



for root, dirs, files in os.walk(inputdir):
    for torrentfile in files:

        if (len(torrentfile) == 48) & (str(torrentfile)[-7:] == "torrent"):

            torrentfilepath = os.path.abspath(root) + "/" + torrentfile

            # Open the torrent file and read it
            with open(torrentfilepath, "rb") as t:
                torrent = t.read()

            # Parse the torrent file
            # Sometimes torrents are fucked up -> try/catch/pass
            try:
                metainfo = bencode.bdecode(torrent)
            except:
              continue

            try:
		pieceLen = metainfo['info']['piece length']
	    except:
		continue

            outdir = str(os.path.abspath(outputdir) + "/" + str(pieceLen))

            if not os.path.exists(outdir):
                os.makedirs( outdir )

            with open(outdir + "/" + torrentfile, "wb") as t:
                t.write(torrent)

