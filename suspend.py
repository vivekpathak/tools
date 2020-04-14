#!/usr/bin/env python
"""
suspend computer once idle exceeds 
vivek pathak
"""
import sys
import time
import subprocess

SKIP_TRIES = 3
MAX_SECONDS = 10*60 if len(sys.argv) == 1 else int(sys.argv[1])
print("timeout %d seconds" % MAX_SECONDS)
s = 0
while True:
    idlemillis = int(subprocess.check_output("xprintidle")) 
    print(idlemillis)
    subprocess.check_call("date", shell=True)
    time.sleep(15)
    s += 1
    if s > SKIP_TRIES and idlemillis > MAX_SECONDS*1000 :
        print("suspend now")
        try:
            subprocess.check_call("systemctl suspend", shell=True)
        except:
            s = 0
            thread.sleep(30)
            pass
