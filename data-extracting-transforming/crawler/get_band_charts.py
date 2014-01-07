#!/usr/bin/python

import json
import urllib2
import urllib
import traceback
import threading
from lxml import etree

list_of_bands_url = 'http://en.wikipedia.org/wiki/List_of_bands_from_England'
uk_charts_url = 'http://www.officialcharts.com/artist/_/'

RESULT = {}
NOT_FOUND = []

def get_bands_from_england():
    ret = []
    f = urllib2.urlopen(list_of_bands_url)
    parser = etree.HTMLParser()
    tree = etree.parse(f, parser)
    cells = tree.xpath('//table[@class="multicol"]/tr/td')

    for line in cells:
        bands = line.xpath('ul/li/a')
        for band in bands:
            band_text = band.text
            if isinstance(band_text, unicode):
                band_text = band_text.encode('utf-8')
            ret.append(band_text)
    return ret

def get_uk_charts_info_thread(bands, lock):
    for band in bands:
        url = uk_charts_url + urllib.quote(band)

        if '/The%20' in url:
            url = url.replace('The%20', '')
        elif 'and%20' in url:
            url = url.replace('and', '&')
        elif 'And%20' in url:
            url = url.replace('And', '&')

        try:
            f = urllib2.urlopen(url)
        except:
            NOT_FOUND.append(url)
            continue

        RESULT[band] = {}
        parser = etree.HTMLParser()
        tree = etree.parse(f, parser)

        cells = tree.xpath('//div[@id="albums"]/table/tr[@class="entry"]')
        for td in cells:
            album = td.xpath('td[@class="info"]/h3')[0].text.strip()
            peak_position = td.xpath('td[@class="peak"]')[0].text.strip()
            with lock:
                RESULT[band][album] = peak_position

def get_uk_charts_info(bands):
    thread_list = []
    num_of_threads = 10
    quotient = len(bands) / num_of_threads
    index = quotient
    start = 0
    lock = threading.Lock()
    for i in xrange(num_of_threads):
        if i == (num_of_threads - 1):
            bands_split = bands[start:]
        else:
            bands_split = bands[start:index]
        t = threading.Thread(target=get_uk_charts_info_thread, args=(bands_split, lock))
        t.start()
        thread_list.append(t)
        start = index
        index = start + quotient

    for t in thread_list:
        t.join()

if __name__ == '__main__':
    bands = get_bands_from_england()
    get_uk_charts_info(bands)
    print json.dumps(RESULT)
