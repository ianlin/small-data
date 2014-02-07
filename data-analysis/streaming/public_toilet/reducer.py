#!/usr/bin/python
# coding=utf8

from __future__ import division
import sys

def main(stdin):
    """
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
    """

    result = {}
    stdin = stdin.readlines()
    total_toilet = len(stdin)
    lastkey = None
    cnt = 0
    for line in stdin:
        key, value = line.strip().split('\t')
        if not lastkey:
            lastkey = key
        if key not in result:
            result[key] = {'total': 0, 'good': 0}
        if key == lastkey:
            cnt += 1
            result[key]['good'] += int(value)
            result[key]['total'] += 1
        else:
            result[lastkey]['good'] += int(value)
            result[key]['total'] += 1
            print '\t'.join((lastkey, str(result[lastkey]['total']), str(result[lastkey]['good']),\
                             str(float(result[lastkey]['good'] / result[lastkey]['total']))))
            cnt = 1
        lastkey = key
    if lastkey:
        print '\t'.join((lastkey, str(result[lastkey]['total']), str(result[lastkey]['good']),\
                         str(float(result[lastkey]['good'] / result[lastkey]['total']))))

if __name__ == '__main__':
    stdin = sys.stdin
    main(stdin)
