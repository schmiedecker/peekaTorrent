# peekatorrent
This is the proof-of-concept code of the peekatorrent paper, to be published at DFRWS'16, and will be pubished with "Digital Investigation" - if you use the torrents, please cite it:


PeekaTorrent: Leveraging P2P Hash Values for Digital Forensics
Sebastian Neuner, Martin Schmiedecker, Edgar R. Weippl
SBA Research


All software here is GPL 2, if not specified otherwise. You can find the paper as well as as plenty of data at https://www.peekatorrent.org


This git repo contains the following:
* hash_extract0r.py: Reads the piece (chunk) hash values from torrent files and outputs them to stdout for import in hashdb
* DHT: simple DHT client to retrieve metainfo for torrents from the DHT
* Crawler: Crawl kickass/piratebay and download the torrents.
* bulk_extractor: compiled binary and SHA-1 module for bulk_extractor. Make sure to set BE_PATH to the folder of the .so file.
