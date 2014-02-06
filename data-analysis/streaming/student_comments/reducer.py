#!/usr/bin/python

import sys

def main():
    lastkey = None
    sum = 0
    for line in sys.stdin:
        key, value = line.split('\t')
        score = int(value.split(',')[-1])
        if not lastkey:
            lastkey = key
        if key == lastkey:
            sum += score
        else:
            print lastkey + '\t' + str(sum)
            sum = score
        lastkey = key
    if lastkey:
        print lastkey + '\t' + str(sum)

if __name__ == '__main__':
    main()
