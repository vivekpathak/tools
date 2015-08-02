#!/usr/bin/env python 

from bs4 import BeautifulSoup
import tempfile
import os

# create a subclass and override the handler methods
class HTMLTagParser:

    def __init__(self, tagid, filename) :
        self.soup = BeautifulSoup( open(filename).read(), 'html.parser')
        self.match = self.soup.select( '#%s' % tagid )[0] 
        #print self.match

    def replace(self, other) :
        self.match.replace_with( other.match )
        #return str( self.soup )
        return self.soup.prettify()


if __name__ == "__main__":
    import sys
    
    tagid = sys.argv[1]
    src = sys.argv[2]
    dst = sys.argv[3]

    sp = HTMLTagParser(tagid, src)
    dp = HTMLTagParser(tagid, dst)
    newhtml = dp.replace(sp)

    backup = tempfile.NamedTemporaryFile(delete=False)
    replacement = tempfile.NamedTemporaryFile(delete=False)
    print 'backing up %s to %s' % (dst, backup.name)
    os.system( "cp %s  %s" % (dst, backup.name))
        
    print 'writing new code to %s' % (replacement.name)
    replacement.write( newhtml ) 
        
    if raw_input( 'now moving code in tagid %s from %s to %s.\nEnter y|n > ' % (tagid, src, dst) ) == 'y':        
        replacement.close()
        print 'copying %s to %s' % (replacement.name, dst)
        os.system( "cp %s  %s" % (replacement.name, dst))
        print 'done!'  
    else:
        print 'exiting...' 
