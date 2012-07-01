#!/usr/bin/python

'''
Date June 10, 2012
Author: Justin Jessup
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Disclaimer:
All software provided as is. All software covered under the GPL license and free for public redistribution.
If unintended consequences occur due to utilization of this software, user bears the resultant outcome.
The rule of thumb is to test and validate properly all solutions prior to implementation within a production environment.
All solutions should be subject to public scrutiny, and peer review.
'''

from error_handle import ConvertExceptions
import time
import os.path
import os
import fnmatch


# Generic function to list all directories and files within a given $PATH filtered by a regular expression 
@ConvertExceptions(StandardError, 0)
def list_all_files(start_path, filter_regex):
    theFiles = []
    for root, dirs, files in os.walk(start_path):
        for files in fnmatch.filter(files, '%s' %filter_regex):
            theFiles.append( os.path.join(root, files))
    return theFiles

# Function to to determine if a file is older than 30 days in age. 
# If the file is older than 30 days in age then delete the file 
@ConvertExceptions(StandardError, 0)
def determine_mtime_filename(path):    
    ftime = os.path.getmtime(path)
    curtime = time.time()
    difftime = (curtime - ftime) / 86400 
    if difftime > 30 and not None:
        return os.remove(path)

# $PATH to where bzip2 compressed pastes are being archived 
start_path1 = "/home/alienone/Scripts/Python/PASTEBIN/pastebins/ARCHIVE"
filter_regex1 = "*.bz2"

for element in list_all_files(start_path1, filter_regex1):
    determine_mtime_filename(str(element)) 

# $PATH to MD5 digest of pastes 
start_path2 = "/home/alienone/Scripts/Python/PASTEBIN/pastebins/ARCHIVE"
filter_regex2 = "*.md5_digest"

for element in list_all_files(start_path2, filter_regex2):
    determine_mtime_filename(str(element))

