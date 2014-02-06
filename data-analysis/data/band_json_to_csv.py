#!/usr/bin/python

import json

data = json.loads(open('band_charts').read())

for band, albums in data.iteritems():
    for album, rank in albums.iteritems():
        print '\t'.join((band, album, rank))
