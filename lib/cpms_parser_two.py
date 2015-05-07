#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

 
id = soup.find_all(text = re.compile("Appropriation ID:"))
print id
 
table = soup.find('table', border=6)
data = {}    
for row in table.findAll('tr')[16:]:
    cells = row.findAll('td')
    key = cells[0].string
    #print key
    value = cells[1].text.strip()
    #print value
    data[key] = value
    print data
    record = (id, key, value)
    writer = csv.writer(open('cpms2.csv', 'ab'))
    writer.writerow(record)
