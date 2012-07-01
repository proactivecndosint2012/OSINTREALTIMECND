#!/usr/bin/python3

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

import pyinotify, time, os, fnmatch, subprocess

# Generic function to check that a file exists - if the file does exist - null the file out
def chk_file(file_name):
    check_file = os.path.isfile(file_name)
    if(check_file == True):
        os.remove(file_name)
    else:
        pass

def printTimeStamp(event_pathname, event_maskname):
    print(time.strftime('%Y-%m-%d %H:%M:%S ' +event_pathname + ' ' +event_maskname))
    return

def exec_process(process_name):
  ps = subprocess.Popen(process_name, shell=True, stdout=subprocess.PIPE)
  output = ps.stdout.read()
  ps.stdout.close()
  ps.wait()
  return

process_name = "/home/alienone/Scripts/Python/PASTEBIN/./cull_pastebin.py"
wm = pyinotify.WatchManager() # Watch Manager
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVED_TO # watched events

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        printTimeStamp(event.pathname, event.maskname)

    def process_IN_CLOSE_WRITE(self, event):
        if fnmatch.fnmatch(event.name, '*.txt'):
            printTimeStamp(event.name, event.maskname)
            exec_process(process_name)
        else:
            printTimeStamp(event.pathname, event.maskname)

    def process_IN_DELETE(self, event):
        printTimeStamp(event.pathname, event.maskname)

    def process_IN_MOVED_TO(self, event):
        printTimeStamp(event.pathname, event.maskname)

# Variable assignment 
handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch('/home/alienone/Scripts/Python/PASTEBIN/pastebins', mask, rec=True)
pid_file = "/home/alienone/Scripts/Python/PASTEBIN/var/run/pyinotify.pid"
log_file = "/home/alienone/Scripts/Python/PASTEBIN/var/log/pyinotify.log"
chk_file(pid_file)
chk_file(log_file)

# To Debug from Commandline uncomment
#notifier.loop()
# To run as a Daemon uncomment
notifier.loop(daemonize=True, callback=None, pid_file='/home/alienone/Scripts/Python/PASTEBIN/var/run/pyinotify.pid', stdout='/home/alienone/Scripts/Python/PASTEBIN/var/log/pyinotify.log')