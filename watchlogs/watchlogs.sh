#!/bin/bash 

ps -eaf | grep java | grep -v grep |  awk '{print $2}' | while read pid; do sudo ls -l /proc/$pid/fd; done | grep -e 'log$' | awk '{print $11}' | while read logfilename ; do wc -l $logfilename; done
