#!/usr/bin/env python

# 1) Recursively parses an offlineimap localfolder
# 2) extracts a few fields to BSON or JSON documents
# 3) pushes resulting document into mongodb

import sys
import time
import os
import re
import pymongo

class Convert():
    def __init__(self, dirName):
        """
        Convert a list of imap files from offlineimap to list of JSON documents
        """
        if not os.path.isdir(dirName):
            print 'Error! Target Directory not found: {0}'.format(dirName)
            sys.exit(1)

        self.fnames = []
        for root, dirs, files in os.walk(dirName):
            self.fnames.extend(os.path.join(root, name) for name in files)

    def process(self):
        """
        Extract key/values from files and JSONofiy them
        """
        dtimePattern = re.compile('^Date:\s+(?P<date>.*)$', re.MULTILINE)
        fromPattern = re.compile('^From:\s+(?P<from>.*)$', re.MULTILINE)
        for fname in self.fnames:
            with open(fname, 'r') as f:
                match = re.search(dtimePattern, f.read())
                if match:
                    date = match.group('date')
                f.seek(0)
                match = re.search(fromPattern, f.read())
                if match:
                    frm = match.group('from')
                if date and frm:
                    print '{0},{1}'.format(date.replace(',', ''), frm.replace('"', ''))


if __name__ == '__main__':
    print 'Opening mongodb connection'
    con = Convert('/home/garm/Mail/gmail')
    con.process()
