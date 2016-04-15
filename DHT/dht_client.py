#!/usr/bin/env python

import libtorrent as lt
import time
import sys
import bencode
import tempfile
import shutil
import os


# The file containing the magnet info_hashes
if len(sys.argv) < 2:
  sys.exit("Too few arguments")

magnet_file = os.path.abspath(sys.argv[1])

# Do the libtorrent stuff here
ses = lt.session()
ses.listen_on(6881, 6891)

params = {
    'save_path': '/tmp/foo/',
    'storage_mode': lt.storage_mode_t(2),
    'paused': False,
    'auto_managed': True,
    'duplicate_is_error': False
    }

ses.add_dht_router("router.utorrent.com", 6881)
ses.add_dht_router("router.bittorrent.com", 6881)
ses.add_dht_router("dht.transmissionbt.com", 6881)
ses.add_dht_router("router.bitcomet.com", 6881)
ses.add_dht_router("dht.aelitis.com", 6881)
ses.start_dht()


def crawl(magnet_link):

  print magnet_link

  h = lt.add_magnet_uri(ses, magnet_link, params)

  timeout_counter = 0

  while (not h.has_metadata()):
    #print "Sleeping..."
    time.sleep(1)

    # Kill this torrent when the timeout reaches 3minutes
    timeout_counter += 1

    if timeout_counter == 180:
      with open("failed_magnets.txt", "a") as fail:
        fail.write(magnet_link + '\n')

      return


  if h.has_metadata():
    #print "Got the metadata"

    torinfo = h.get_torrent_info()

    torfile = lt.create_torrent( torinfo )

    name = (magnet_link.split("magnet:?xt=urn:btih:")[1][:40]).upper()

    with open( name + ".torrent", "wb" ) as f:
      f.write(lt.bencode(torfile.generate()))

  return



if __name__ == '__main__':

  # Load the magnet links into a list and remove the newlines (added two newlines in my magnet scraper)
  with open(magnet_file, "r") as f:
    content = f.readlines()

  magnet_list = []

  for mf in content:
    if mf != '\n':
      temp = mf.replace('\n', '')
      magnet_list.append(temp)

  for magnet in magnet_list:
    crawl(magnet)

    os.system("rm -rf /tmp/foo/*")

  os.system("rm -rf /tmp/foo/*")
