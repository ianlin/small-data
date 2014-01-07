#!/usr/bin/python
# coding=utf8

import sys
import json
import urllib2

try:
    query_type = sys.argv[1]
except:
    query_type = ''

if query_type == 'store_discount':
    url = 'http://data.taipei.gov.tw/opendata/apply/json/NzRBNTc0NDUtMjMxMi00RTk1LTkxMjgtNzgzMzU5MEQzRDc3'
    required_keys = ('name', 'district', 'address', 'telephone', 'discountContent')
elif query_type == 'companies_in_neihu':
    url = 'http://data.taipei.gov.tw/opendata/apply/json/OUU2MzJDRTEtRTA4Ri00Q0FDLTkzQjctQUE5OUNCREREMjFE'
    required_keys = ('VAT', 'Name', 'Address')
elif query_type == 'public_toilet':
    url = 'http://data.taipei.gov.tw/opendata/apply/query/NTQ4QTg2RjMtQjg0NC00REIxLUFCMUMtMzBGNTE5RTdCRUY3?$format=json'
    required_keys = ('title', 'dep_content', 'address', 'lng', 'lat')
else:
    print '[ERROR] Unsupported query type ({0})'.format(query_type)
    sys.exit(1)

f = urllib2.urlopen(url)
data = json.loads(f.read())

cnt = 0
result = ''
for d in data:
    row = ''
    for k in required_keys:
        if not row:
            row = str(cnt)
        if d[k]:
            value = d[k].encode('utf8').strip()
            if query_type == 'public_toilet' and k == 'title':
                value = value.replace('公廁坐落：', '')
            row += ',' + value

    if not result:
        result += row
    else:
        result += '\n' + row
    cnt += 1

print result
