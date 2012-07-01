#!/usr/local/bin/python

'''
Date June 30, 2012
Author: Justin Jessup
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007   

Disclaimer
=====
All software provided as is. All software covered under the GPL license and free for public redistribution.
If unintended consequences occur due to utilization of this software, user bears the resultant outcome.
The rule of thumb is to test and validate properly all solutions prior to implementation within a production environment.
All solutions should be subject to public scrutiny, and peer review.
'''

import sys, twitter, functools, datetime, re
from error_handle import ConvertExceptions
from recipe__make_twitter_request import make_twitter_request

# WatchList string list convert to list datastructure generator object
@ConvertExceptions(StandardError, 0)
def username_watchlist(watchlist_usernames):
    for line in open(watchlist_usernames, 'r'):
        yield line.split('@')[1].strip('\n')
        
# Generator function to obtain list of twitter follower id's
@ConvertExceptions(StandardError, 0)
def get_followers(MAX_IDS):
    t = twitter.Twitter(domain='api.twitter.com', api_version='1')
    get_friends_ids = functools.partial(make_twitter_request, t, t.friends.ids)
    cursor = -1
    ids = []
    while cursor != 0:
        for user_name in username_watchlist(watchlist_usernames):
            print user_name
            response = get_friends_ids(screen_name=user_name, cursor=cursor)
            ids += response['ids']
            cursor = response['next_cursor']
            if len(ids) >= MAX_IDS:
                yield ids
            break 

# Convert list of integers ids to generator object of strings
# interger ids are related to the Users the targeted username Follows
@ConvertExceptions(StandardError, 0)
def convert_ids():
    for follower_id in get_followers(MAX_IDS):
        for int_id in follower_id:
            yield ("from_user_id_str:" + str(int_id))
        break

# Generator function to translate follower_id's into Twitter Usernames
@ConvertExceptions(StandardError, 0)
def search_twitter(MAX_IDS, RESULTS_PER_PAGE, MAX_PAGES, output_filename):
    twitter_search = twitter.Twitter(domain="search.twitter.com")
    search_results = []
    for page in range(1,MAX_PAGES+1):
        for user_id in convert_ids():
            search_string = user_id  
            search_results += twitter_search.search(q=search_string, rpp=RESULTS_PER_PAGE, page=page)['results']
            for result in search_results:
                if search_string.split(':')[1] in result['from_user_id_str']:
                    with open(output_filename, "a") as f:
                        f.write(result['from_user'])

# Global Variables
MAX_IDS = 5
MAX_PAGES = 5
RESULTS_PER_PAGE = 10
date_time_one = (str(datetime.datetime.now()).split(' ')[0])
date_time_two = (str(datetime.datetime.now())).split(' ')[1].replace(':','-').split('.')[0]
output_filename = 'culled_twit_files/' + "TwitterFollowerHits-" + date_time_one + "-" + date_time_two + '.txt'
watchlist_usernames = "watchlist/twitter_usernames.txt"
#SCREEN_NAME = [i for i in username_watchlist(watchlist_usernames)]

# Main execution 
if __name__ == '__main__':
    search_twitter(MAX_IDS, RESULTS_PER_PAGE, MAX_PAGES, output_filename)