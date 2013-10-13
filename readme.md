ipython-pandas-gmail
========
This project shows how to download all of your gmail locally and parse through
it using ipython and pandas to make pretty graphs!

#### Prerequisite Gmail settings:

* Click the little gear drop down in the top right corner.
* Click on the 'Forwarding and POP/IMAP' tab.
* IMAP Access: then Enable IMAP.
* I chose left the default values alone
* Save Changes

#### Prerequisite System Setup:
I use virtualenv and source bin/activate script, then deactivate when done.
 
    $ pip install -e git+https://github.com/OfflineIMAP/offlineimap.git#egg=offlineimap
    $ cp ~/projects/virtualenv/src/offlineimap/offlineimap.conf.minimal ~/.offlineimaprc
    $ # Edit your .offlineimaprc
    $ imapoffline
    $ # It took ~2 hours for ~1.5GB locally stored

#### Convert IMAP box files into mongodb

Fields extracted:
* 'Date:'
* 'Subject:'
* 'From: <name@host>'
* 'To:'
* 'Cc:'
* 'Content-Type: text/plain;'

#### Running Demos:
The good stuff:

    $ 

#### Todo:
.offlineimaprc

    [general]
    accounts = Gmail
    maxsyncaccounts = 1
    socktimeout = 60

    ui = Curses.Blinkenlights

    [Account Gmail]
    localrepository = Local
    remoterepository = Remote
    autorefresh = 5
    quick = 1

    [Repository Local]
    type = Maildir
    localfolders = ~/Mail

    [Repository Remote]
    type = Gmail
    remotehost = imap.gmail.com
    ssl = yes
    remoteport = 993
    remoteuser = <myEmail>
    remotepass = <myPass>
    maxconnections = 1
    holdconnectionopen = no
    keepalive = 120
    realdelete = no

    [mbnames]
    enabled = yes
    filename = ~/.mutt/mailboxes
    header = "mailboxes "
    peritem = "+%(accountname)s/%(foldername)s"
    sep = " "
    footer = "\n"

.muttrc

    source ~/.mutt/mailboxes
    # folder-hook Personal set from="youremail@personal.com"
    # folder-hook Work set from="youremail@work.com"
    set mbox_type=Maildir
    set folder=$HOME/Mail
    spoolfile=+Personal/INBOX



#### References:
* [virtualenv](https://pypi.python.org/pypi/virtualenv)
* [offlineimap](http://offlineimap.org/)
* [mutt + gmail + offlineimap](http://pbrisbin.com/posts/mutt_gmail_offlineimap/)
