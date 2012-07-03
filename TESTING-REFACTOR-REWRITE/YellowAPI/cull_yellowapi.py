#!/usr/local/bin/python

import urllib2, json, csv
from pprint import pprint

SEARCH_BASE = 'http://api.sandbox.yellowapi.com/FindBusiness/?pg=1&what=Kennels&lang=en&where=Vancouver&pgLen=40&fmt=JSON&UID=44.44.44.44&apikey=hdh7redzysg7pe6gs7zj6unv'
data = json.load(urllib2.urlopen(SEARCH_BASE))
data_list3 = list(data["listings"])
f = csv.writer(open("kennels.csv", "wb+"))
f.writerow(["Name","Street Address","City","Province","ZipCode"])
for item in data_list3:
    f.writerow([item['name'],item['address']['street'],item['address']['city'],item['address']['prov'],item['address']['pcode']])

