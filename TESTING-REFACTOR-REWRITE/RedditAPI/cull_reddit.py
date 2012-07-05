#!/usr/local/bin/python

'''
Date July 4, 2012
Author: Justin Jessup
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Disclaimer:
All software provided as is. All software covered under the GPL license and free for public redistribution.
If unintended consequences occur due to utilization of this software, user bears the resultant outcome.
The rule of thumb is to test and validate properly all solutions prior to implementation within a production environment.
All solutions should be subject to public scrutiny, and peer review.
'''

import urllib2, json, csv, re, datetime

def search_watchlist(watchlist_search):
    for line in open(watchlist_search, 'r'):
        yield line.strip('\n')
        
def cull_reddit(csv_filename):
    f = csv.writer(open(csv_filename, "wb+"))
    f.writerow(["Created","Origin FQDN","Title","URL","ID","Name","Author"])
    SEARCH_BASE = 'http://www.reddit.com/.json'
    data = json.load(urllib2.urlopen(SEARCH_BASE))
    data_list = list(data["data"]["children"])
    for search_string in search_watchlist(watchlist_search):
        for item in data_list:
            ipsrch = re.compile(r'\b%s\b' %search_string, re.IGNORECASE)
            if ipsrch.findall(result['text']):
                f.writerow([item['data']['created'],item['data']['domain'].encode('ascii','ignore'),\
                            item['data']['title'].encode('ascii','ignore'),item['data']['id'].encode('ascii','ignore'),\
                            item['data']['name'].encode('ascii','ignore'),item['data']['author'].encode('ascii','ignore')])

def cull_subreddit(csv_filename):
    f = csv.writer(open(csv_filename, "wb+"))
    f.writerow(["Created","Origin FQDN","Title","URL","ID","Name","Author"])
    for search_string in search_watchlist(watchlist_search):
        SEARCH_BASE = 'http://www.reddit.com/r/' + search_string + '.json'
        data = json.load(urllib2.urlopen(SEARCH_BASE))
        data_list = list(data["data"]["children"])
        for item in data_list:
            ipsrch = re.compile(r'\b%s\b' %search_string, re.IGNORECASE)
            if ipsrch.findall(result['text']):
                f.writerow([item['data']['created'],item['data']['domain'].encode('ascii','ignore'),\
                            item['data']['title'].encode('ascii','ignore'),item['data']['id'].encode('ascii','ignore'),\
                            item['data']['name'].encode('ascii','ignore'),item['data']['author'].encode('ascii','ignore')])

# Global Variable Assignment
watchlist_search = "watchlist/reddit_watchlist.txt"
date_time_one = (str(datetime.datetime.now()).split(' ')[0])
date_time_two = (str(datetime.datetime.now())).split(' ')[1].replace(':','-').split('.')[0]
csv_file_one = "culled_product/search_one/Reddit-Global-WatchList" + '-' + date_time_one + '-' + date_time_two + '.csv'
csv_file_two =  "culled_product/search_two/SubReddit-Global-WatchList" + '-' + date_time_one + '-' + date_time_two + '.csv'

# Main Excecution 
if __name__ == '__main__':
    cull_reddit(csv_file_one)
    cull_subreddit(csv_file_two)