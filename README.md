# 1-900-BAD-SEXT

My friends Maggie and Beth wanted a Twitter bot that could tweet out some bad
sexts. I bet that you could make some by just searching for already-existing
tweets containing a few key present-tense phrases and just drop "SEXT:" in
 front of it. These jokes literally write themselves.
 
## Dependencies

I took two steps to install the necessary libraries:

```
$ pip install tweepy
$ pip install nltk
```

Here's me setting up the Python environment:

```
(badsext)primo:badsext brian$ pip install tweepy
Downloading/unpacking tweepy
  Downloading tweepy-3.4.0-py2.py3-none-any.whl
Downloading/unpacking requests>=2.4.3 (from tweepy)
  Downloading requests-2.8.1-py2.py3-none-any.whl (497kB): 497kB downloaded
Downloading/unpacking six>=1.7.3 (from tweepy)
  Downloading six-1.10.0-py2.py3-none-any.whl
Downloading/unpacking requests-oauthlib>=0.4.1 (from tweepy)
  Downloading requests_oauthlib-0.5.0-py2.py3-none-any.whl
Downloading/unpacking oauthlib>=0.6.2 (from requests-oauthlib>=0.4.1->tweepy)
  Downloading oauthlib-1.0.3.tar.gz (109kB): 109kB downloaded
  Running setup.py (path:/Users/brian/.virtualenvs/badsext/build/oauthlib/setup.py) egg_info for package oauthlib
    
Installing collected packages: tweepy, requests, six, requests-oauthlib, oauthlib
  Running setup.py install for oauthlib
    
Successfully installed tweepy requests six requests-oauthlib oauthlib
Cleaning up...
(badsext)primo:badsext brian$ pip install nltk
Downloading/unpacking nltk
  Downloading nltk-3.1.tar.gz (1.1MB): 1.1MB downloaded
  Running setup.py (path:/Users/brian/.virtualenvs/badsext/build/nltk/setup.py) egg_info for package nltk
    
    warning: no files found matching 'README.txt'
    warning: no files found matching 'Makefile' under directory '*.txt'
    warning: no previously-included files matching '*~' found anywhere in distribution
Installing collected packages: nltk
  Running setup.py install for nltk
    
    warning: no files found matching 'README.txt'
    warning: no files found matching 'Makefile' under directory '*.txt'
    warning: no previously-included files matching '*~' found anywhere in distribution
Successfully installed nltk
Cleaning up...
```

Here's what I got installed afterwards:

```
(badsext)primo:badsext brian$ pip freeze
nltk==3.1
oauthlib==1.0.3
requests==2.8.1
requests-oauthlib==0.5.0
six==1.10.0
tweepy==3.4.0
wsgiref==0.1.2
```
