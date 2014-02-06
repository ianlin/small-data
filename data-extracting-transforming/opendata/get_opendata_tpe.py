#!/usr/bin/python
# coding=utf8

import sys
import json
import urllib2

def usage():
    print 'Usage: python get_opendata_tpe.py [store_discount|companies_in_neihu|public_toilet]'

def extract_data(url):
    f = urllib2.urlopen(url)
    data = json.loads(f.read())
    return data

def transform_data(data):
    cnt = 0
    result = ''
    for d in data:
        row = ''
        for k in required_keys:
            if not row:
                row = str(cnt)
            if d[k]:
                value = d[k].encode('utf8')
                # 去掉前後空白
                value = value.strip()
                # 去掉全形空白
                value = value.replace('　', '')
                if query_type == 'public_toilet' and k == 'title':
                    value = value.replace('公廁坐落：', '')
                if query_type == 'public_toilet' and k == 'dep_content':
                    value_split = value.split('，')
                    value = ''
                    if len(value_split) == 5:
                        handicapped = '0'
                    else:
                        handicapped = '1'
                    for i in xrange(5):
                        value += value_split[i].split('：')[1] + ','
                    value += handicapped
                row += ',' + value

        if not result:
            result += row
        else:
            result += '\n' + row
        cnt += 1
    return result

if __name__ == '__main__':
    try:
        query_type = sys.argv[1]
    except:
        usage()
        sys.exit(1)

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
        print '[ERROR] Unsupported query type ({0})\n'.format(query_type)
        usage()
        sys.exit(1)

    data = extract_data(url)
    #print data

    result = transform_data(data)
    print result
