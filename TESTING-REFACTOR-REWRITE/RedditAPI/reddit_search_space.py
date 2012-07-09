#!/usr/local/bin/python3.2

import re, requests
from bs4 import BeautifulSoup

def search_watchlist(watchlist_search):
    for line in open(watchlist_search, 'rt'):
        yield line.strip('\n')


def cull_urlSearchSpace():
    for search_string in search_watchlist(watchlist_search):
        SEARCH_BASE = "http://www.reddit.com/search?q=" + search_string
        request_url = SEARCH_BASE
        request_urlGet = requests.get(request_url)
        if request_urlGet.status_code == 200:
            html_page = request_urlGet.text
            soup = BeautifulSoup(html_page)
            url_search_space = []
            for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
                suffix = "/"
                if link.get('href').endswith(suffix):
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
        print(element)
    

