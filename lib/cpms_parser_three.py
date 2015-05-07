#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

 
id = soup.find_all(text = re.compile("Appropriation ID:"))
print id
 
#this isn't getting datetime fields UnicodeEncodeError: 'ascii' codec can't encode character u'\xa0' in position 0: ordinal not in range(128) 

table = soup.find('table', border=6)
data = {}    
for row in table.findAll('tr')[24:]:
    cells = row.findAll('td')
    key = cells[0].text.strip()
    #print key
    value = cells[1].text.strip()
    #print value
    data[key] = value
    print data
    record = (id, value)
    writer = csv.writer(open('cpms3.csv', 'ab'))
    writer.writerow(record)
