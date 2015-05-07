#!/usr/bin/env python

import urllib2
from bs4 import BeautifulSoup


#this does actually work, tho i have five years to get through; guess i'd do this as five separate sets of things?


for i in xrange(1100, 1322):
    try:
        page = urllib2.urlopen('file:cpms/doShowAppropriations.aspx?pid=10-{}'.format(i))
    except:
        continue
    else:
        soup = BeautifulSoup(page.read())