#!/usr/bin/perl -w 

# Prevent terminal from going idle
# my old ssh no idle tool.  put a line to start from .bashrc  (or other shell startup program) 
# @author vivek pathak
# @licence  apache 2; @see http://www.apache.org/licenses/LICENSE-2.0.html
$| = 1;
$prev = "." ;
while(1) { 
    $curr = (split( /\s+/, qx(who -um) ))[4] ; 
    #print "Time now $curr\n" ; 
    if($curr ne $prev) { 
        print "." ; 
        $prev = $curr ;
    } 
    sleep(10);
} 
