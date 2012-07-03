#!/usr/local/bin/python

'''
Date June 30, 2012
Author: Justin Jessup
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Disclaimer:
All software provided as is. All software covered under the GPL license and free for public redistribution.
If unintended consequences occur due to utilization of this software, user bears the resultant outcome.
The rule of thumb is to test and validate properly all solutions prior to implementation within a production environment.
All solutions should be subject to public scrutiny, and peer review.
'''
import sys, datetime, json, twitter, re, glob, csv
from error_handle import ConvertExceptions

# Generator object function creates glob of filename $PATHS
@ConvertExceptions(StandardError, 0)
def globof_files(path, filter_name):
    files = glob.glob(path)
    for filename in files:
        suffix = filter_name
        if filename.endswith(suffix) == True:
            yield(filename)
            
# WatchList string list convert to list datastructure generator object
@ConvertExceptions(StandardError, 0)
def username_watchlist(watchlist_usernames):
    for line in open(watchlist_usernames, 'r'):
        yield line.strip('\n')

# WatchList string list convert to list datastructure generator object
@ConvertExceptions(StandardError, 0)
def search_watchlist(watchlist_search):
    for line in open(watchlist_search, 'r'):
        yield line.strip('\n')

# Search Twitter Function
@ConvertExceptions(StandardError, 0)
def search_twitter(search_usernames, search_list, int_one, int_two, output_file_name):
    MAX_PAGES = int_one
    RESULTS_PER_PAGE = int_two
    twitter_search = twitter.Twitter(domain="search.twitter.com")
    search_results = []
    for page in range(1,MAX_PAGES+1):
        for search_string in search_usernames:
            search_results += twitter_search.search(q=search_string, rpp=RESULTS_PER_PAGE, page=page)['results']
            for result in search_results:
                field_one = (json.dumps(result['created_at']))
                field_two = (json.dumps(result['from_user_name']))
                field_three = (json.dumps(result['text']))
                f = csv.writer(open(output_file_name, "wb+"))
                f.writerow(["Created_At","From_User_Name","Tweet_Text"])
                f.writerow([field_one,field_two,field_three])

# Global Variables
path = "/Users/alienone/Downloads/alienone-PASTEBIN-9fd9c83/twitter/*.txt"
filter_name = ".txt"
watchlist_usernames = "watchlist/twitter_usernames.txt"
watchlist_search = "watchlist/twitter_watchlist.txt"
search_usernames = [i for i in username_watchlist(watchlist_usernames)]
search_list = [i for i in search_watchlist(watchlist_search)]
int_one = 100
int_two = 100
date_time_one = (str(datetime.datetime.now()).split(' ')[0])
date_time_two = (str(datetime.datetime.now())).split(' ')[1].replace(':','-').split('.')[0]
output_file_name = 'culled_twit_files/' + "Twitter_Hits-GlobalSearch-WatchList" + date_time_one + "-" + date_time_two + '.csv'


# Main Execution
if __name__ == '__main__':
    search_twitter(search_usernames, search_list, int_one, int_two, output_file_name)
    