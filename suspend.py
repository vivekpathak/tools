"""
suspend computer once idle exceeds MAX_SECONDS from xprintidle (tested on ubuntu)
author : vivek pathak

usage:
    python suspend.py

"""
import sys
import time
import subprocess

SKIP_TRIES = 5
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
            # awakened!
            thread.sleep(30)
        finally:
            s = 0
