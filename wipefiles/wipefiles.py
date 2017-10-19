
import os
import sys
import random
import string


class wipefile(object):

    def __init__(self, filename):
        self.filename = filename
        self.statinfo = os.stat(filename)
        self.chars = string.ascii_letters + string.digits
        for i in range(0, 3):
            self._wipe()

    def _wipe(self):
        print 'working on ' + self.filename
        fd = open(self.filename, "w+")
        print fd
        charlist = list(self.chars)
        for offset in range(0, 1 + int(self.statinfo.st_size/len(self.chars))):
            random.shuffle(charlist)
            print fd
            fd.write(''.join(charlist))
        fd.flush()


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        wipefile(arg)
