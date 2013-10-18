#!/usr/bin/env python

# 1) Recursively parses an offlineimap localfolder
# 2) uses regex to extract supported fields from each e-mail
# 3) pushes resulting document into mongodb

import sys
import time
import os
import re
import pymongo

class Convert():
    def __init__(self, dirName):
        """
        Convert a list of imap files from offlineimap to key value pairs
        """
        if not os.path.isdir(dirName):
            print 'Error! Target Directory not found: {0}'.format(dirName)
            sys.exit(1)

        self.fnames = []
        for root, dirs, files in os.walk(dirName):
            self.fnames.extend(os.path.join(root, name) for name in files)

    def process(self):
        """
        Extract key/values from files
        """
        dtimePattern = re.compile('^Date:\s+(?P<date>.*)$', re.MULTILINE)
        fromPattern = re.compile('^From:\s+(?P<from>.*)$', re.MULTILINE)
        for fname in self.fnames:
            with open(fname, 'r') as f:
                match = re.search(dtimePattern, f.read())
                if match:
                    date = match.group('date')
                # this feels like a procedural kludge
                # if only i learned more Haskell then my
                # functional programming skills would yield
                # more elegant python.  My spelling is just doomed.
                f.seek(0)
                match = re.search(fromPattern, f.read())
                if match:
                    frm = match.group('from')
                if date and frm:
                    # yield a tuple so this is a generator
                    # can tidy up the frm field as you see fit
                    yield ( date, frm.replace('"', '') )


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: {0} ~/Mail/gmail'.format(sys.argv[0])
        sys.exit(1)
    imapdir = sys.argv[1]

    mongohost = 'localhost'
    mongoport = 27017
    print 'Opening mongodb connection at {0}:{1}'.format(mongohost, mongoport)
    client = pymongo.MongoClient(mongohost, mongoport)
    db = client.gmail
    collection = db.email
    # WARNING: cleans up old stuff by droping entire collection!
    collection.drop()

    print 'Extracting and dumping e-mail data to mongodb.'
    con = Convert(imapdir)
    for date, email in con.process():
        document = {'date': date, 'email':email}
        collection.save(document)

