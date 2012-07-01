#!/usr/bin/python

'''
Date June 10, 2012
Author: www.shellguardians.com
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Disclaimer:
All software provided as is. All software covered under the GPL license and free for public redistribution.
If unintended consequences occur due to utilization of this software, user bears the resultant outcome.
The rule of thumb is to test and validate properly all solutions prior to implementation within a production environment.
All solutions should be subject to public scrutiny, and peer review.
'''

# Written by Xavier Garcia
# www.shellguardians.com
# Modifications
# AlienOne added error handling decorator

import re
import BeautifulSoup
import urllib2
import time
import Queue
import threading
import sys
import datetime
import random
import os
from error_handle import ConvertExceptions

pastesseen = set()
pastes = Queue.Queue()

@ConvertExceptions(StandardError, 0)
def downloader():
    while True:
        paste = pastes.get()
        fn = "pastebins/%s-%s.txt" % (paste, datetime.datetime.today().strftime("%Y-%m-%d"))
        content = urllib2.urlopen("http://pastebin.com/raw.php?i=" + paste).read()
        if "requesting a little bit too much" in content:
            print "Throttling... requeuing %s" % paste
            pastes.put(paste)
            time.sleep(0.1)
        else:
            f = open(fn, "wt")
            f.write(content)
            f.close()
        delay = 1.1 # random.uniform(1, 3)
        sys.stdout.write("Downloaded %s, waiting %f sec\n" % (paste, delay))
        time.sleep(delay)
        pastes.task_done()

@ConvertExceptions(StandardError, 0)
def scraper():
    scrapecount = 0
    while scrapecount < 10:
        html = urllib2.urlopen("http://www.pastebin.com").read()
        soup = BeautifulSoup.BeautifulSoup(html)
        ul = soup.find("ul", "right_menu")
	for li in ul.findAll("li"):
	    href = li.a["href"]
            if href in pastesseen:
                sys.stdout.write("%s already seen\n" % href)
            else:
                href = href[1:] # chop off leading /
                pastes.put(href)
                pastesseen.add(href)
                sys.stdout.write("%s queued for download\n" % href)
        delay = 12 # random.uniform(6,10)
        time.sleep(delay)
        scrapecount += 1

num_workers = 1
for i in range(num_workers):
    t = threading.Thread(target=downloader)
    t.setDaemon(True)
    t.start()

if not os.path.exists("pastebins"):
    os.mkdir("pastebins") # Thanks, threecheese!

#Global Variable Assignment 
s = threading.Thread(target=scraper)

# Main Execution
if __name__ == '__main__':
    s.start()
    s.join()
