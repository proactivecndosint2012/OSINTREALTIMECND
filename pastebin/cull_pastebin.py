#!/usr/local/bin/python

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

# Function code recipe for the "grab_email" function borrowed from Active State. 
# http://code.activestate.com/recipes/138889-extract-email-addresses-from-files/
# Remainder of the script authored by AlienOne

import os, re, glob, csv, datetime
from error_handle import ConvertExceptions
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

# Generic function to create CSV full paste url and full path to the paste
@ConvertExceptions(StandardError, 0)
def globof_files():
    files = glob.glob(path)
    for element in files:
        yield("pastebin.com/" + element.split('/')[6].split('-')[0] + ',' + element)

# Generic function to zero out a file so we are starting with a clean slate 
@ConvertExceptions(StandardError, 0)
def null_file(file_path):
    f = open(file_path, 'w')
    f.close()

# Generic function to check that a file exists - if the file does exist - null the file out
@ConvertExceptions(StandardError, 0)
def chk_file(file_name):
    check_file = os.path.isfile(file_name)
    if(check_file == True):
        null_file(file_name)
    else:
        null_file(file_name)

# Generic function to rename all processed files with suffix .processed
@ConvertExceptions(StandardError, 0)
def rename_processed_files(path, filter_name):
    files = glob.glob(path)
    suffix = filter_name
    for filename in files:
        if filename.endswith(suffix) != True:
            os.rename(filename, filename + suffix)

# Function to cull email addresses from pastebin dump
@ConvertExceptions(StandardError, 0)
def grab_email(filter_name, files = []):
    found = []
    if files != None:
        for file in files:
            suffix = filter_name
            if file.endswith(suffix) != True:
                for line in open(file,'r'):
                    mailsrch = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}')
                    found.extend(mailsrch.findall(line))
    u = {}
    for item in found:
        u[item] = 1
    return u.keys()

# Function to cull phone numbers from pastebin dump
@ConvertExceptions(StandardError, 0)
def grab_phone(filter_name, files = []):
    found = []
    if files != None:
        for file in files:
            suffix = filter_name
            if file.endswith(suffix) != True:
                for line in open(file,'r'):
                    phonesrch = re.compile(r'(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$')
                    found.extend(phonesrch.findall(line)) 
    u = {}
    for item in found:
        u[item] = 1
    return u.keys()

# Function to cull IP Addresses from pastebin dump
@ConvertExceptions(StandardError, 0)
def grab_ip(filter_name, files = []):
    found = []
    if files != None:
        for file in files:
            suffix = filter_name
            if file.endswith(suffix) != True:
                for line in open(file, 'r'):
                    ipsrch = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
                    found.extend(ipsrch.findall(line))
    u = {}
    for item in found:
        u[item] = 1
    return u.keys()
    a = [file for file in files]
    
# WatchList string list convert to list datastructure generator object
@ConvertExceptions(StandardError, 0)
def convert_watchlist(watchlist_name):
    for line in open(watchlist_name, 'r'):
        yield line.strip('\n')

# Function to cull WatchList Hits from pastebin dump
@ConvertExceptions(StandardError, 0)
def watchlist_hit(watchlist_name, filter_name, files = []):
    found = []
    if files != None:
        for watchlist_element in convert_watchlist(watchlist_name):
            for file in files:
                suffix = filter_name
                if file.endswith(suffix) != True:
                    for line in open(file, 'r'):
                        ipsrch = re.compile(r'\b%s\b' %watchlist_element, re.IGNORECASE)
                        found.extend(ipsrch.findall(line))
    u = {}
    for item in found:
        u[item] = 1
    return u.keys()
    
# Function to write culled indicators to file 
@ConvertExceptions(StandardError, 0)
def write_indicators(file_name, item, element):
    with open(file_name, "a") as f:
        f.write(item.split(',')[0] +','+ "".join(map(str,element))+ '\n')

# Cull email, phone, IP, watchlist indicator algorithm
@ConvertExceptions(StandardError, 0)
def cull_indicators(email_output, phone_output, ip_output, watchlist_output):
    check_list = [email_output, phone_output, ip_output, watchlist_output]
    for file_name in check_list:
        chk_file(file_name)
    for item in globof_files():
        files = []
        files.append(item.split(',')[1]) 
        for element in grab_email(filter_name, files):
            write_indicators(email_output, item, element)
            break
        for element in grab_phone(filter_name, files):
            write_indicators(phone_output, item, element)
            break
        for element in grab_ip(filter_name, files):
            write_indicators(ip_output, item, element)    
            break
        for element in watchlist_hit(watchlist_name, filter_name, files):
            write_indicators(watchlist_output, item, element)
            break
        
# Email culled product files
@ConvertExceptions(StandardError, 0)
def send_mail(send_from, send_to, subject, text, attachments=[], server="localhost"):
    assert type(send_to)==list
    assert type(files)==list
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach( MIMEText(text) )
    for f in attachments:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(file,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)
        smtp = smtplib.SMTP(server)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()

# Global Variables
date_time_one = (str(datetime.datetime.now()).split(' ')[0])
date_time_two = (str(datetime.datetime.now())).split(' ')[1].replace(':','-').split('.')[0]
output_file_name = 'culled_twit_files/' + "Twitter_Hits-" + date_time_one + "-" + date_time_two + '.csv'
path = '/Users/alienone/Downloads/OSINTCND/pastebins/*.txt'
filter_name = '.processed'
suffix = filter_name
email_output = "../product/EMAIL/email_addresses_result" + '-' + date_time_one + '-' + date_time_two + '.csv'
phone_output = "../product/PHONE/phone_numbers_result" + '-' + date_time_one + '-' + date_time_two + '.csv'
ip_output = "../product/IP/ip_addresses_result" + '-' + date_time_one + '-' + date_time_two + '.csv'
watchlist_name = "../watchlist/watchlist.txt"
watchlist_output = "../product/WATCHLIST/watchlist_hits" + '-' + date_time_one + '-' + date_time_two + '.csv'
send_from = "someone@someemail.com"
send_to = "someone@someemail.com"
subject = "Pastebin WatchList Hits"
attachments = [email_output, phone_output, ip_output, watchlist_output]

# Main execution
if __name__ == '__main__':
    cull_indicators(email_output, phone_output, ip_output, watchlist_output)
    rename_processed_files(path, suffix)
    