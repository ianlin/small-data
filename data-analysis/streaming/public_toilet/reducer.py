#!/usr/bin/python
# coding=utf8

from __future__ import division
import sys

def main():
    result = {}
    for line in sys.stdin:
        key, value = line.split('\t')
        if not isinstance(key, unicode):
            key = key.decode('utf8')
        if key not in result:
            result[key] = {'total': 0, 'good': 0}
        result[key]['good'] += int(value)
        result[key]['total'] += 1
    for k, v in result.iteritems():
        print '\t'.join((k, str(v['total']), str(v['good']), str(float(v['good'] / v['total']))))

if __name__ == '__main__':
    main()
