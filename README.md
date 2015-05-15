## Overview

This is an effort at getting data from the State of New Mexico's [Capital Appropriations Search](http://cpms.dfa.state.nm.us/).

Data is tucked away in "detail" pages such as this one: http://cpms.dfa.state.nm.us/doShowAppropriations.aspx?pid=10-1100

The scraper code is configured to allow download of all years, or
selected subset of years (see Usage instructions below).

### To Dos/Issues

There are odd breaks in the HTML, so trying to parse it in four steps/files.
Comments in files indicate issues.

## Installation

Use pip, ideally in a virtualenv.

```
pip install -r requirements.txt
```

## Usage

Download data pages, optionally filtering for select year(s).

NOTE: Download for all years will take a while!

```
# Download all years
python lib/cpms_scraper.py

# Download single year
python lib/cpms_scraper.py 2015

# Download multiple years
python lib/cpms_scraper.py 2014,2015
```

TK: Instructions on running cpms_parsers??
