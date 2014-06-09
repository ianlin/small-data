#!/usr/bin/python
# coding=utf8

import sys
import re

def is_good_toilet(total, first, second):
    return True if (float(first) + float(second)) / float(total) >= 0.75 else False

def str_to_utf8(data):
    if not isinstance(data, unicode):
        data = data.decode('utf-8')
    return data

def utf8_to_str(data):
    if isinstance(data, unicode):
        data = data.encode('utf-8')
    return data

def main():
    for line in sys.stdin:
        if not line.startswith('#'):
            line_split = line.strip().split(',')
            address = str_to_utf8(line_split[8])
            pattern = re.compile(u"^臺北市([^市區]+區).*")
            match = pattern.match(address)
            good_toilet = '0'
            if match:
                district = utf8_to_str(match.group(1))
                if line_split[7] == '1' and line_split[2] != '0':
                    total = line_split[2]
                    first = line_split[3]
                    second = line_split[4]
                    if is_good_toilet(total, first, second):
                        good_toilet = '1'
                print '\t'.join((district, '1', good_toilet ,'0'))

if __name__ == '__main__':
    main()
