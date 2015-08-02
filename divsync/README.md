
A tool to sync html blocks in different files

# Copy a div from src to target 

To preprocess and make uniform the html prior to publishing. 

Could be thought like SSI except it is done statically instead of dynamically 

Could be included as part of a toolchain target to grab common html code from a template and to 
populate it with manual oversight  

# Example with output 

    $ ./divsync.py page-visual-header-block  ~/code/jfi/web/about.html ~/code/jfi/web/add.html 
    backing up /home/vpathak/code/jfi/web/add.html to /tmp/tmpFG6xad
    writing new code to /tmp/tmpzNpB4K
    now moving code in tagid page-visual-header-block from /home/vpathak/code/jfi/web/about.html to /home/vpathak/code/jfi/web/add.html.
    Enter y|n > y
    copying /tmp/tmpzNpB4K to /home/vpathak/code/jfi/web/add.html
    done!

