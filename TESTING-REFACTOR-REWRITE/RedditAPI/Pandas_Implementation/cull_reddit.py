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

import requests, json, csv, re, datetime, pprint
from pandas import *
from multiprocessing import Pool

def multi_process(jobname):
    po = Pool()
    po.apply_async(jobname)
    po.close
    po.join

def search_watchlist(watchlist_search):
    for line in open(watchlist_search, 'r'):
        yield line.strip('\n')
        
def search_watchlist_url(watchlist_search_url):
    for line in open(watchlist_search_url, 'r'):
        yield line.strip('\n')
        
def cull_reddit():
    #f = csv.writer(open(csv_filename, "wb+"))
    #f.writerow(["Created","Origin FQDN","Title","URL","Author"])
    SEARCH_BASE = 'http://www.reddit.com/.json'
    request_url = SEARCH_BASE
    request_urlGet = requests.get(request_url)
    if request_urlGet.status_code == 200:
        if 'json' in (request_urlGet.headers['content-type']):
            data = json.loads(request_urlGet.text)
            data_list = data['data']['children']
            for element in data_list:
                pprint.pprint(element['data'][media])
               
                
            #data_list = list(data['data']['children'])
            #for search_string in search_watchlist(watchlist_search):
            #    for item in data_list:
            #        ipsrch = re.compile(r'\b%s\b' %search_string, re.IGNORECASE)
            #        if ipsrch.findall(item['data']['title']):
            #            created_Time = str(item['data']['created']).split('.')[0]
            #            convert_createdTime = (datetime.datetime.fromtimestamp(int(created_Time)).strftime('%H:%M:%S %Y-%m-%d'))
            #            f.writerow([convert_createdTime,item['data']['domain'].encode('ascii','ignore'),\
            #                        item['data']['title'].encode('ascii','ignore'),item['data']['url'].encode('ascii','ignore'),\
            #                        item['data']['author'].encode('ascii','ignore')])

#def cull_subreddit(csv_filename):
#    f = csv.writer(open(csv_filename, "wb+"))
#    f.writerow(["Created","Origin FQDN","Title","URL","Author"])
#    for search_string_url in search_watchlist_url(watchlist_search_url):
#        SEARCH_BASE = 'http://www.reddit.com/r/' + search_string_url + '.json'
#        request_url = SEARCH_BASE
#        request_urlGet = requests.get(request_url)
#        if request_urlGet.status_code == 200:
#            if 'json' in (request_urlGet.headers['content-type']):
#                data = json.loads(request_urlGet.text)
#                data_list = list(data['data']['children'])
#                for search_string in search_watchlist(watchlist_search):
#                    for item in data_list:
#                        ipsrch = re.compile(r'\b%s\b' %search_string, re.IGNORECASE)
#                        if ipsrch.findall(item['data']['title']):
#                            created_Time = str(item['data']['created']).split('.')[0]
#                            convert_createdTime = (datetime.datetime.fromtimestamp(int(created_Time)).strftime('%H:%M:%S %Y-%m-%d'))
#                            f.writerow([convert_createdTime,item['data']['domain'].encode('ascii','ignore'),\
#                                    item['data']['title'].encode('ascii','ignore'),item['data']['url'].encode('ascii','ignore'),\
#                                    item['data']['author'].encode('ascii','ignore')])
#                            

# Global Variable Assignment
watchlist_search = "watchlist/reddit_watchlist.txt"
watchlist_search_url = "watchlist/reddit_watchlist_url.txt"
#date_time_one = (str(datetime.datetime.now()).split(' ')[0])
#date_time_two = (str(datetime.datetime.now())).split(' ')[1].replace(':','-').split('.')[0]
#csv_file_one = "culled_product/search_one/Reddit-Global-WatchList" + '-' + date_time_one + '-' + date_time_two + '.csv'
#csv_file_two =  "culled_product/search_two/SubReddit-Global-WatchList" + '-' + date_time_one + '-' + date_time_two + '.csv'

# Main Excecution 
if __name__ == '__main__':
    cull_reddit()
    #po = Pool()
    #job_one = target=cull_reddit(csv_file_one)
    #job_two = target=cull_subreddit(csv_file_two)
    #jobs = []
    #jobs.append(job_one)
    #jobs.append(job_two)
    #for jobname in jobs:
    #    multi_process(jobname)
    
    
    