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

import time, os, tarfile, hashlib, fnmatch
from error_handle import ConvertExceptions

# Function to create the MD5 digest 
@ConvertExceptions(StandardError, 0)
def md5_checksum(file_name):
    use_md5_hash = hashlib.md5()
    try:
        use_md5_hash.update(open(file_name).read())
    except Exception,exception_output:
        print exception_output
    else:
        return use_md5_hash.hexdigest() + '\t' + file_name

# Function to bzip2 archive files 
@ConvertExceptions(StandardError, 0)
def archive_files(list_of_files, output_archive, checksum_output):
    tarball = tarfile.open(output_archive, 'w:bz2')
    chk_list = open(checksum_output, 'wb')
    for file_name in list_of_files:
        tarball.add(file_name)
        chk_list.write(md5_checksum(file_name) + "\n")
    chk_list.write(md5_checksum(os.path.join(os.getcwd(),output_archive)) + "\n")
    chk_list.close()
    tarball.close()
    return

# Generic function to list all files within a directory tree $PATH
@ConvertExceptions(StandardError, 0)
def list_all_files(start_path, filter_regex):
    theFiles = []
    for root, dirs, files in os.walk(start_path):
        for files in fnmatch.filter(files, '%s' %filter_regex):
            theFiles.append( os.path.join(root, files))
    return theFiles

# Generic function to delete a file 
@ConvertExceptions(StandardError, 0)
def del_file(filename):
	if os.path.exists(filename):
		os.remove(filename)
	else:
		pass
    
#############################################
###########         MAIN         ############
#############################################

# Filter regex for searching for files within the directory tree
filter_regex = "*.processed"
# $PATH to pastebin pastes 
path_name = "/home/alienone/Scripts/Python/PASTEBIN/pastebins"
# $PATH to where we wish to store archived pastes will be stored  
archive_dir = "/home/alienone/Scripts/Python/PASTEBIN/pastebins/ARCHIVE/"
# Create archive file name for pastbin pastes 
archive_name = archive_dir + time.strftime('%Y%m%d%H%M%S') + '.tar.bz2'
# $PATH to where the MD5 digest of pastes files and pastes archive file 
checksum_dir = "/home/alienone/Scripts/Python/PASTEBIN/pastebins/ARCHIVE/"
checksum_list = checksum_dir + time.strftime('%Y%m%d%H%M%S') + ".md5_digest" 

# Main function execution to create bzip2 archive of pastebin pastes along with MD5 digest 
archive_files(list_all_files(path_name, filter_regex),archive_name, checksum_list)

# Delete .processed pastes artifacts post archival process
for processed_file in (list_all_files(path_name, filter_regex)):
	del_file(processed_file)
 
