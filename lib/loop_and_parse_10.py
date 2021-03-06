# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import csv 

#these ranges need to be changed for each year 
for i in xrange(1100, 1322):
    try:
        page = urllib2.urlopen('file:cpms/doShowAppropriations.aspx?pid=10-{}'.format(i))
    except:
        continue
    else:
        soup = BeautifulSoup(page.read(), from_encoding='utf-8')
        
        data = []
        table = soup.find('table', border=6)
        rows = table.findAll('tr')
        for row in rows:
            cols = row.findAll('td')
            cells = [ele.text.strip() for ele in cols]
            # Get rid of empty values
            data = ([ele for ele in cells if ele]) 
            # add the id no. at the beginning
            data.insert(0, i)
            #print data
            record = (data)
            writer = csv.writer(open('cpms10.csv', 'ab'))
            writer.writerow(record)
 