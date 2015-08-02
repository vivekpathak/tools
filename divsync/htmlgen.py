#!/usr/bin/env python 

from bs4 import BeautifulSoup
from jsmin import jsmin
import tempfile
import os


# create a subclass and override the handler methods
class HTMLCompiler:

    def __init__(self,  filename) :
        self.basepath = os.path.dirname(os.path.realpath(filename))
        self.soup = BeautifulSoup( open(filename).read(), 'html.parser')
        self._replace_scripts()
        
    def output(self):
        return str(self.soup)
    
    def _replace_scripts(self) :
        for s in self.soup.find_all('script'):
            if s.has_attr('src') and s['src'][0:4] != 'http' :
                s.string = self._minify(self._inline_script_from_src(s['src']))
                del s['src']
                

    def _inline_script_from_src(self, filename):
        fullfilename = self.basepath + "/" + filename 
        return open(fullfilename).read()

    def _minify(self, s):
        return jsmin(s)
    
    def _minify2(self, s) :
        src = tempfile.NamedTemporaryFile(delete = False)
        src.write(s)
        src.close()

        tgt = tempfile.NamedTemporaryFile(delete = False)
        os.system( "closure-compiler %s --js_output_file %s" % (src.name, tgt.name) )
        smin = tgt.read()
        os.system( "rm " + src.name + " " + tgt.name )  
        return smin




if __name__ == "__main__":
    import sys
    src = sys.argv[1]

    parse = HTMLCompiler(src)

    print( parse.output() )  

