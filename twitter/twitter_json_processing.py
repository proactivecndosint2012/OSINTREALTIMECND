#!/usr/local/bin/python

'''
Date July 2, 2012
Author: www.shellguardians.com
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Disclaimer:
All software provided as is. All software covered under the GPL license and free for public redistribution.
If unintended consequences occur due to utilization of this software, user bears the resultant outcome.
The rule of thumb is to test and validate properly all solutions prior to implementation within a production environment.
All solutions should be subject to public scrutiny, and peer review.
'''

import urllib2, json, csv, re, datetime
from error_handle import ConvertExceptions

@ConvertExceptions(StandardError, 0)
def search_watchlist(watchlist_search):
    for line in open(watchlist_search, 'r'):
        yield line.strip('\n')

@ConvertExceptions(StandardError, 0)
def username_watchlist(watchlist_usernames):
    for line in open(watchlist_usernames, 'r'):
        yield line.strip('\n')

@ConvertExceptions(StandardError, 0)
def twitter_global_username_plusWatchlist(csv_filename_one):
    f = csv.writer(open(csv_filename_one, "wb+"))
    f.writerow(["Created_At","From_User","Tweet_Text"])
    for user in username_watchlist(watchlist_usernames):
        for search in search_watchlist(watchlist_search):
            SEARCH_BASE = 'http://search.twitter.com/search.json?q=%40' + user
            data = json.load(urllib2.urlopen(SEARCH_BASE))
            data_list3 = list(data['results'])
            for result in data_list3:
                ipsrch = re.compile(r'\b%s\b' %search, re.IGNORECASE)
                if ipsrch.findall(result['text']):
                    f.writerow([result['created_at'].encode('ascii','ignore'),result['from_user'].encode('ascii','ignore'),result['text'].encode('ascii','ignore')])

@ConvertExceptions(StandardError, 0)
def twitter_global_Watchlist(csv_filename_two):
    f = csv.writer(open(csv_filename_two, "wb+"))
    f.writerow(["Created_At","From_User","Tweet_Text"])
    for search in search_watchlist(watchlist_search):
        SEARCH_BASE = 'http://search.twitter.com/search.json?q=' + search
        data = json.load(urllib2.urlopen(SEARCH_BASE))
        data_list3 = list(data['results'])
        for result in data_list3:
            ipsrch = re.compile(r'\b%s\b' %search, re.IGNORECASE)
            if ipsrch.findall(result['text']):
                f.writerow([result['created_at'].encode('ascii','ignore'),result['from_user'].encode('ascii','ignore'),result['text'].encode('ascii','ignore')])
                

# Global Variables
watchlist_usernames = "watchlist/twitter_usernames.txt"
watchlist_search = "watchlist/twitter_watchlist.txt"
date_time_one = (str(datetime.datetime.now()).split(' ')[0])
date_time_two = (str(datetime.datetime.now())).split(' ')[1].replace(':','-').split('.')[0]
csv_filename_one = "culled_product/search_one/Twitter-Global-Username-WatchList" + '-' + date_time_one + '-' + date_time_two + '.csv'
csv_filename_two =  "culled_product/search_two/Twitter-Global-WatchList" + '-' + date_time_one + '-' + date_time_two + '.csv'

# Main Excecution 
if __name__ == '__main__':
    twitter_global_username_plusWatchlist(csv_filename_one)
    twitter_global_Watchlist(csv_filename_two)

