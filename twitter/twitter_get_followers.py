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

import sys, twitter, functools, datetime
from recipe__make_twitter_request import make_twitter_request

# Generator function to obtain list of twitter follower id's 
def get_followers(SCREEN_NAME, MAX_IDS):
    t = twitter.Twitter(domain='api.twitter.com', api_version='1')
    get_friends_ids = functools.partial(make_twitter_request, t, t.friends.ids)
    cursor = -1
    ids = []
    while cursor != 0:
        response = get_friends_ids(screen_name=SCREEN_NAME, cursor=cursor)
        ids += response['ids']
        cursor = response['next_cursor']
        print >> sys.stderr, 'Fetched %i total ids for %s' % (len(ids), SCREEN_NAME)
        if len(ids) >= MAX_IDS:
            break
    yield ids
    
def convert_ids():
    for follower_id in get_followers(SCREEN_NAME, MAX_IDS):
        for int_id in follower_id:
            yield (str(int_id))

# Generator function to translate follower_id's into Twitter Usernames
def search_twitter(MAX_IDS, RESULTS_PER_PAGE, MAX_PAGES, output_filename):
    twitter_search = twitter.Twitter(domain="search.twitter.com")
    search_results = []
    for page in range(1,MAX_PAGES+1):
        for i in convert_ids():
            search_string = i
            search_results += twitter_search.search(q=search_string, rpp=RESULTS_PER_PAGE, page=page)['results']
            for result in search_results:
                    with open(output_filename, "a") as f:
                        f.write(json.dumps(result['from_user'], indent=0))
                    print(result['from_user'])
# Global Variables
SCREEN_NAME = "AnonymousIRC"
MAX_IDS = 500
MAX_PAGES = 50
RESULTS_PER_PAGE = 100
date_time_one = (str(datetime.datetime.now()).split(' ')[0])
date_time_two = (str(datetime.datetime.now())).split(' ')[1].replace(':','-').split('.')[0]
output_filename = 'culled_twit_files/' + "TwitterFollowerHits-" + date_time_one + "-" + date_time_two + '.txt'

# Main execution 
if __name__ == '__main__':
    search_twitter(MAX_IDS, RESULTS_PER_PAGE, MAX_PAGES, output_filename)
    