#!/usr/bin/env python

from HTMLParser import HTMLParser
import tempfile
import os

# create a subclass and override the handler methods
class HTMLTagParser(HTMLParser):

    def __init__(self, tagid, filename) :
        HTMLParser.__init__(self)
        self.filename = filename 
        self.filedata = open(filename).read()
        self.filelines =  open(filename).readlines()
        self.tagid = tagid
        self.tagstack = []
        self.inMatch = False 
        self.feed(  self.filedata ) 

    def handle_starttag(self, tag, attrs):
        #print "Encountered a start tag:", tag
        #print "attrs:" , attrs
        for (attrname, attrvalue) in attrs :
            if attrname == 'id' and attrvalue == self.tagid:
                #print 'found required tag ' , tag , attrs
                #print 'found matcging start at ' , self.getpos()
                self.inMatch = True
                self.startpos = self.getpos()


        if self.inMatch:        
            self.tagstack.append(tag) 
            

    def handle_endtag(self, tag):
        #print "Encountered an end tag :", tag
        if self.inMatch:        
            x = self.tagstack.pop()
            if x != tag: 
                raise Exception ('tag mismatch popped %s != found %s' , (x, tag) ) 
            if self.tagstack == [] :
                #print 'found matcging end at ' , self.getpos()
                #print 'found matcging end at ' , self.getpos()
                (line, offset) = self.getpos()

                correction = self.filelines[line-1][offset:].find('>')
                if correction < 0:
                    raise Exception( 'incorrect file being parsed : ' + self.filename )
                #print 'found correct matching end at ' , (line, offset + correction) 

                self.endpos = (line, offset + correction)
                self.inMatch = False



    def replace(self, other) :
        newlines = [] 
        for i in range(0,self.startpos[0]-1):
            newlines.append( self.filelines[i] )

        newlines.append(self.filelines[ self.startpos[0]-1 ][:self.startpos[1]] + other.filelines[other.startpos[0]-1][other.startpos[1]:] ) 

        for i in range(other.startpos[0],other.endpos[0]-1):
            newlines.append( other.filelines[i] ) 

        newlines.append( other.filelines[other.endpos[0]-1][:other.endpos[1]] + self.filelines[ self.endpos[0]-1 ][self.endpos[1]:] ) 

        for i in range(self.endpos[0], len(self.filelines)):
            newlines.append( self.filelines[i] )
       
        return ''.join( newlines ) 

        


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4 :
        print 'Usage : %s %s %s %s' % (sys.argv[0] , 'tagid', 'srchtml' , 'targethtml' ) 
        sys.exit(9) 

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
    replacement.write( newhtml) 
        
    if raw_input( 'now moving code in tagid %s from %s to %s.\nEnter y|n > ' % (tagid, src, dst) ) == 'y':        
        replacement.close()
        print 'copying %s to %s' % (replacement.name, dst)
        os.system( "cp %s  %s" % (replacement.name, dst))
        print 'done!'  
    else:
        print 'exiting...' 
