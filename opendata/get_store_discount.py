#!/usr/bin/python
# coding=utf8

import json
import urllib2

# companies in NeiHu
#query_type = 'companies_in_neihu'
#url = 'http://data.taipei.gov.tw/opendata/apply/json/OUU2MzJDRTEtRTA4Ri00Q0FDLTkzQjctQUE5OUNCREREMjFE'

# store discount info
query_type = 'store_discount'
url = 'http://data.taipei.gov.tw/opendata/apply/json/NzRBNTc0NDUtMjMxMi00RTk1LTkxMjgtNzgzMzU5MEQzRDc3'

f = urllib2.urlopen(url)
data = json.loads(f.read())

if query_type == 'store_discount':
    required_keys = ('name', 'district', 'address', 'telephone', 'discountContent')
elif query_type == 'companies_in_neihu':
    required_keys = ('VAT', 'Name', 'Address')

cnt = 0
result = ''
for d in data:
    row = ''
    for k in required_keys:
        if not row:
            row = str(cnt)
        if d[k]:
            row += ',' + d[k].encode('utf8')

    if not result:
        result += row
    else:
        result += '\n' + row
    cnt += 1

print result
