#!/usr/bin/python

import sys
import json

if __name__ == '__main__':
    lastkey = None
    cnt = 0
    for line in sys.stdin:
        key = line.strip().split('\t')[0]
        if not lastkey:
            lastkey = key
        if key == lastkey:
            cnt += 1
        else:
            print lastkey + '\t' + str(cnt)
            cnt = 1
        lastkey = key
    if lastkey:
        print lastkey + '\t' + str(cnt)
