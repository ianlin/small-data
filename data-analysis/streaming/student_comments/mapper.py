#!/usr/bin/python

import sys
import json

def main():
    for line in sys.stdin:
        line = line.strip().split(',')
        student = line[0]
        age = line[1]
        district = line[2]
        comments = line[3]
        print ','.join((student, comments))

if __name__ == '__main__':
    main()
