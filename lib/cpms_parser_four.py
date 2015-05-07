# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import csv 
import re


 
id = soup.find_all(text = re.compile("Appropriation ID:"))
print id

#this isn't getting datetime fields UnicodeEncodeError: 'ascii' codec can't encode character u'\xa0' in position 0: ordinal not in range(128) 


table = soup.find('table', border=6)
data = {}    
for row in table.findAll('tr')[42:]:
    cells = row.findAll('td')
    key = cells[0].string
    #print key
    value = cells[1].string
    #print value
    data[key] = value
    print data
    record = (id, key, value)
    writer = csv.writer(open('cpms4.csv', 'ab'))
    writer.writerow(record)