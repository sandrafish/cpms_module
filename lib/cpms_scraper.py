#!/usr/bin/env python
import os
import re
import time
import urllib2
import requests
from bs4 import BeautifulSoup

# An alternative strategy to consider: Scrape the index of data pages from the start page (http://cpms.dfa.state.nm.us/),
# year by year, and then download each page. This has the benefit of being more dynamic, in the sense that you can
# run the scraper again to get future updates.

# You can apparently download the entire index in a single call, but the page load takes a looooooong time,
# and it's kinder to fetch year by year (at the expense of a little more complexity).

# As part of above strategy, you could cache the index pages and detailed data pages locally for downstream use in parsing.
# Also, this could be useful down the road for logic that checks the latest year's index, say on a daily basis, and compares
# that page to the locally cached one to determine if there are any new records to process.

# Finally, take the above with a grain of salt :) This is just one way of doing things, and it's quite possibly overkill for your needs.
# If nothing else, perhaps there are a few bits you'll find useful.


####  Partially implemented code for above strategy ####

# Use a top-level "main" function to quarterback the script by invoking
# task-specific functions, defined below. The "main" function is invoked
# at bottom of script.
def main():
    index_pages = fetch_index_pages()
    detail_page_links = scrape_detail_page_links(index_pages)
    download_detail_pages(detail_page_links)

# This function will save pages locally to cache and return list of page content as raw html strings
def fetch_index_pages():
    # Fetch search page as string using "requests" library
    search_page_url = "http://cpms.dfa.state.nm.us/"
    # Extract the available years from the page (this is intended to future-proof the script)
    search_page_html = requests.get(search_page_url).content
    # We tuck away the unsightly code for plucking out year options in yet another function...
    years = scrape_year_options(search_page_html)

    # We'll use the cache dir downstream to stash downloaded pages
    cache_dir = create_cache_directory()

    POST_URL = "http://cpms.dfa.state.nm.us/doProjectSearch.aspx"
    pages = []
    # Below, we fetch and save every year's page.  If the page is in cache, we don't download it again.
    # Alternatively, you might want to always download, say, the current and most recent years.
    # Might be overkill, but something to consider if you need to check regularly for updates (including the prior year
    # on the (possibly faulty) assumption that at the start of a year, there might be adjustments to prior year's appropriations).
    for year in years[-1:]:
        try:
            cache_page = cached_index_page_path(cache_dir, year)
            html = open(cache_page, 'rb').read()
            print 'Fetched index page from cache: {}'.format(cache_page)
        except IOError:
            # An error signals that the page isn't cached locally, so we'll fetch it and save the content
            html = requests.post(POST_URL, {'FiscalYear': year}).content
            # Save the page locally
            save_index_page(cache_dir, year, html)
        pages.append(html)
    # Return html all "new" pages for downstream scraping of detail link pages
    return pages

def scrape_year_options(search_page_html):
    years = []
    search_soup = BeautifulSoup(search_page_html, "lxml")
    # Pluck out the select menu containing the year options
    year_select_menu= search_soup.find('select', {"name": "FiscalYear"})
    # Create a regex pattern to use below to filter our menu options
    year_pattern = re.compile('\d\d')
    # Use a gross list comprehension to filter out two-digit years for download downstream.
    # This is needed to exclude the ALL option and a strange blank menu option
    years = [opt['value'] for opt in year_select_menu.findAll('option') if year_pattern.match(opt['value'])]
    return years

def create_cache_directory():
    # Create a hidden, local cache directory
    # We need the error handling in case the directory already exists
    # (there is a more complex/professional way to do this, but this gets the job done for our purposes)
    # NOTE: we'll put the cache dir in the top-level directory (above lib/)
    top_level_dir = os.path.abspath(os.path.join(os.path.realpath(__file__), '../..')) 
    cache_dir = os.path.join(top_level_dir, '.cache')
    try:
        os.makedirs(cache_dir)
    except OSError:
        pass
    return cache_dir

def save_index_page(cache_dir, year, html):
    # NOTE: You might want to add some logic here to check if the incoming page has a local version in cache 
    # and, if so, check whether the incoming page content matches the cached version:
    # if page matches, skip the download
    # if page isn't in cache or has been updated (i.e. doesn't match pre-existing version), then save it locally
    cached_page = cached_index_page_path(cache_dir, year)
    print "Saving index page: {}".format(cached_page)
    with open(cached_page, 'wb') as local_file:
        local_file.write(html)

def cached_index_page_path(cache_dir, year):
    return os.path.join(cache_dir, 'index_page_{}.html'.format(year))

def scrape_detail_page_links(index_pages):
    links = []
    # Pull out the detail page links, possibly using findAll('a') or somesuch
    base_url = "http://cpms.dfa.state.nm.us/"
    url_pattern =  re.compile(r'\d+-\d+')
    for html in index_pages:
        # Example URL
        # http://cpms.dfa.state.nm.us/doShowAppropriations.aspx?pid=15-1101
        soup = BeautifulSoup(html, 'lxml')
        # Another list comprehension that finds all target urls on page, then combines it with the base url to
        # form the final URL for detail data pages
        # NOTE: This is quick-and-dirty; the URL regex pattern might need tuning...
        detail_page_links = [base_url + url['href'] for url in soup.findAll('a', href=url_pattern)]
        links.extend(detail_page_links)
    return links

def download_detail_pages(links):
    # Once again, we check the cache for the page, and if it doesn't exist, then download it
    # (similar to logic used above in fetch_index_pages function)
    cache_dir = create_cache_directory()
    pid_pattern = re.compile(r'pid=(\d+-\d+)$')
    print "Downloading detail data pages..."
    # For each link, we check if the page is in cache based on page id; if not, we download and save the file
    already_in_cache = 0
    for link in links:
        page_id = pid_pattern.search(link).groups()[0]
        cache_page = cached_detail_page_path(cache_dir, page_id)
        # NOTE: Below we're only checking for file existence. This is a really naive (read bad) strategy! Should update this
        # to include a more robust check, e.g. based on contents of file.
        if os.path.isfile(cache_page):
            already_in_cache += 1
        else:
            html = requests.get(link).content
            save_detail_page(cache_dir, page_id, html)
            # Include a one-second delay between requests to be nice to their servers.
            time.sleep(1)

    print 'NOTE: {} pages were already in cache (and therefore not downloaded)'.format(already_in_cache)

def save_detail_page(cache_dir, page_id, html):
    cached_page = cached_detail_page_path(cache_dir, page_id)
    print "Saving detail page: {}".format(cached_page)
    with open(cached_page, 'wb') as local_file:
        local_file.write(html)

def cached_detail_page_path(cache_dir, page_id):
    return os.path.join(cache_dir, 'detail_page_{}.html'.format(page_id))

if __name__ == '__main__':
    main()

# ORIGINAL CODE (with some suggested tweaks)
#for i in xrange(1100, 1322):
#    #TODO: Add a time.sleep(1) call to stagger the scrape by 1 second. Another way to be friendly to their server(s).
#    try:
#        #TODO: Use a function to check if file is stored locally, and if not, download and store locally (as described above)
#        page = urllib2.urlopen('file:cpms/doShowAppropriations.aspx?pid=10-{}'.format(i))
#    except:
#        continue
#    else:
#        soup = BeautifulSoup(page.read())
