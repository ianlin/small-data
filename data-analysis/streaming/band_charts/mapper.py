#!/usr/bin/python

import sys
import json

if __name__ == '__main__':
    for line in sys.stdin:
        line = json.loads(line.strip())
        for key, value in line.iteritems():
            for subkey, subvalue in value.iteritems():
                if subvalue.strip() == '1':
                    print key + '\t' + subkey
