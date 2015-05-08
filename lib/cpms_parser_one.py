#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

#would prefer to use something like this for id; but it doesn't get what i want
#id = soup.find('td', bgcolor="#A3D5E4")

#this returns [u'\r\nAppropriation ID:\xa0\xa010-1100'] when i'd prefer just 010-1100
id = soup.find_all(text = re.compile("Appropriation ID:"))
#printing just to see that something's happening
print id
 

table = soup.find('table', border=6)

data = {}
for row in table.findAll('tr')[3:]:
    #this works, tho it doesn't get the first row (year) where there's a weird image spacer thing between two tds 
    cells = row.findAll('td')
    key = cells[0].text.strip()
    #the following throws a list index out of range error, but gets the stuff
    value = cells[1].text.strip()
    data[key] = value
    print data
    record = (id, key, value)
    writer = csv.writer(open('cpms.csv', 'ab'))
    writer.writerow(record)
