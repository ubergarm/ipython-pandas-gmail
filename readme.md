ipython-pandas-gmail
========
This project guide shows how to download all of your gmail locally and parse
through it using ipython notebook and pandas to make pretty graphs!  If it
doesn't work perfectly, hopefully it will at least guide you in the right 
direction.  Happy Hacking!

#### Prerequisite Gmail settings:

* Log into your Gmail account
* Click the little gear drop down in the top right corner
* Click on the 'Forwarding and POP/IMAP' tab
* IMAP Access: then Enable IMAP
* The default values seem to work fine
* Save Changes

#### Setup virtualenv
I use virtualenv and a ~/projects folder to keep a tidy dev environment.
Skip this if you simply install globally, or have everything already.

    $ sudo apt-get install python-virtualenv
    $ virtualenv ~/projects/virtualenv
    # then get into virtualenv
    $ source ~/projects/virtualenv/bin/activate
 
#### Setup offlineimap and download your Gmail

    $ pip install -e git+https://github.com/OfflineIMAP/offlineimap.git#egg=offlineimap
    $ cp ~/projects/ipython-pandas-gmail/dot-offlineimaprc ~/.offlineimaprc
    # Edit your .offlineimaprc to use your Gmail address 
    # It defaults to dump your mail into ~/Mail/gmail
    $ mkdir ~/Mail
    $ imapoffline
    # It took ~2 hours for ~1.5GB locally stored e-mail

#### Install ipython notebook from github

    $ cd ~/projects/
    $ git clone --recursive https://github.com/ipython/ipython.git
    $ cd ipython
    $ pip install -e ".[notebook]"
    # run from anywhere inside virtualenv
    $ ipython notebook

#### Install supporting packages and pandas

    $ sudo apt-get install libpng-dev
    $ pip install matplotlib
    $ pip install pandas
    # $ pip install scipy
    # $ pip install sympy
    # $ pip install nose

#### Install mongodb
You can:

1. Edit the code to point at an existing mongodb server
2. Install mongodb some *normal* way
3. The new and cool happy hipster hacker way for kernel 3.8 or newer:

`$ sudo -i`
`$ cd /opt && mkdir docker && cd docker`
`$ wget --output-document=docker https://get.docker.io/builds/Linux/x86_64/docker-latest`
`$ chmod +x docker`
`$ sudo ./docker -d &`
`$ ./docker run -d -p :27017 rgarcia/mongodb mongod --noprealloc --smallfiles --nojournal`

It will take a few minutes to download the docker image the first time,
but subsequent runs will be very snappy.  When done, you can clean up
by doing:

    $ ./docker ps -a
    $ ./docker rm <container id>

This docker is a beast unto itself.  Check out the links below for more info.

#### Convert downloaded IMAP files into mongodb
Take a look at imap2json.py.  It takes less than a minute to process 1.5gb
of raw imap e-mail files.  It isn't coded very defensively and I've not tested
it on other e-mail sources or files except my own setup.  It does drop the
collection, so make sure it doesn't collide and wreck something already there.

This program could use some cleaning.  You could optionally use a plain old
CSV file instead of bothering with the mongodb, but I wanted to learn stuff.

It could also probably be more clever about how it extracts data, as there
is probably already some tool to parse this e-mail format into JSON or similar.  

Also, once could directly extract a datetime object and stick the it into
mongodb with that nifty BSON capability, but I do the conversion later in
pandas.

Finally, I apologize, I haven't installed pyflakes or various linting things to
beat me up every time I safe until I develop a better programming style.  

Fields currently extracted:

* 'Date:'
* 'From: Joe Bob <name@host>'

Usage:

    $ cd ~/projects/ipython-pandas-gmail
    $ chmod a+x ./imap2json.py
    $ ./imap2json.py ~/Mail/gmail

#### Ipython Notebook Fun:
When you run the command `ipython notebook` it should pop open your browser
pointing to localhost:8888.  There you can create a New Notebook or import
myGmail.ipynb and `Cell -> Run All` to check out data crunching and graphs.

Feel the power!

#### References:
* [virtualenv](https://pypi.python.org/pypi/virtualenv)
* [ipython notebook](http://ipython.org/notebook.html)
* [pandas](http://pandas.pydata.org/)
* [offlineimap](http://offlineimap.org/)
* [mutt + gmail + offlineimap](http://pbrisbin.com/posts/mutt_gmail_offlineimap/)
* [pymongo](http://api.mongodb.org/python/current/index.html)
* [docker](http://www.docker.io/gettingstarted/)
* [docker cgroup memory/swap support](http://docs.docker.io/en/latest/installation/kernel/)
