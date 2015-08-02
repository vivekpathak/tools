#!/usr/bin/env python 
# Compile an html page to inline all the scripts being referred by it.
# Pass the non minified js code linked in the page via the closure compiler
#
# Notes:
#
# 1. Although there is a lot of innovative work done on asynchronous loading
# of js includes at runtime, it seems that doing that work statically would result
# in faster loading time because only one request would be sent.
#
# 2. The idea is to replace and inline the scripts and css into the page so
# that the semantics of the html page would remain identical  
#
# Author : Vivek Pathak
#          Sun Aug  2 16:48:38 EDT 2015
#
# Changes :
#
# 

from bs4 import BeautifulSoup
import tempfile
import os
import subprocess



class HTMLCompiler:

    def __init__(self,  filename) :
        self.basepath = os.path.dirname(os.path.realpath(filename))
        self.soup = BeautifulSoup( open(filename).read(), 'html.parser')
        self._replace_scripts()
        self._replace_styles() 
        
    def output(self):
        return str(self.soup)
    
    def _replace_scripts(self) :
        for s in self.soup.find_all('script'):

            if s.has_attr('src') and s['src'][0:4] != 'http' :    # local script with src directive 
                s.string = self._inline_minify_script_from_src(self.basepath + "/" + s['src'])
                del s['src']
                
            elif not s.has_attr('src') and s.has_attr('type') and s['type'] == 'application/javascript' :  # inline script 
                copyfd = tempfile.NamedTemporaryFile(delete=False)
                copyfd.write(s.string)
                copyfd.close()
                s.string = self._inline_minify_script_from_src(copyfd.name)
                del s['src']                

    def _inline_minify_script_from_src(self, filename):
        if filename[-6:] == 'min.js' :
            return '\n' + open(filename).read() + '\n' 
        else:
            return '\n' + subprocess.check_output( [ "closure-compiler" , "--language_in=ECMASCRIPT5", "--compilation_level=WHITESPACE_ONLY", filename ] )  
    


    def _replace_styles(self):
        innerStyleTag = None 
        styles = [] 
        for s in self.soup.head.contents :
            #print 'found ' , s.name
            if not s.name:
                pass
            #if s.name == 'link' and s.has_attr('rel') and s['rel'] == 'stylesheet' and s.has_attr('href') and s['href'][0:4] != 'http' :
            elif s.name == 'link' and s.has_attr('href') and s['href'][0:4] != 'http' :
                styles.append(self._inline_minify_styles_from_src(self.basepath + "/" + s['href']))
                del s
            elif s.name == 'style' :
                 innerStyleTag = s
                 styles.append( s.string )

        if innerStyleTag is None:
            innerStyleTag = self.soup.new_tag("style", type="text/css")
            self.soup.head.append( innerStyleTag )

        innerStyleTag.string = '\n'.join( styles )
        #print styles


    def _inline_minify_styles_from_src(self, filename):
        if filename[-7:] == 'min.css' :
            return open(filename).read()
        else:
            return subprocess.check_output( [ "csstidy" , filename , "--silent=true" ] ) 
        
            

if __name__ == "__main__":
    import sys
    src = sys.argv[1]

    parse = HTMLCompiler(src)

    #print( parse.output() )  

    target = sys.argv[2]
    open( target , 'w' ).write( parse.output() )
    
