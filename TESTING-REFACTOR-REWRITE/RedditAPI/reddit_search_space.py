#!/usr/local/bin/python

from BeautifulSoup import BeautifulSoup
import urllib2
import re
import requests


def search_watchlist(watchlist_search):
    for line in open(watchlist_search, 'r'):
        yield line.strip('\n')
        
def search_watchlist_url(watchlist_search_url):
    for line in open(watchlist_search_url, 'r'):
        yield line.strip('\n')
        
def cull_urlSearchSpace():
    for search_string in search_watchlist(watchlist_search):
        SEARCH_BASE = "http://www.reddit.com/search?q=" + search_string
        request_url = SEARCH_BASE
        request_urlGet = requests.get(request_url)
        if request_urlGet.status_code == 200:
            html_page = urllib2.urlopen(SEARCH_BASE)
            soup = BeautifulSoup(html_page)
            url_search_space = []
            for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
                suffix = "/"
                if link.endswith(suffix):
                    url_search_space.append(link.get('href')+ ".json")
                else:
                    url_search_space.append(link.get('href')+ "/.json")
                for url_path in url_search_space:
                    yield url_path

# Global Variable Assignment
watchlist_search = "watchlist/reddit_watchlist.txt"

# Main Execution
if __name__ == '__main__':
    for element in cull_urlSearchSpace():
        print element
    

