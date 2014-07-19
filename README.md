# PyCorn Time
PyCorn Time is a clone of the popular project Popcorntime, but it is implemented in Python and doesn't have a graphical user interface but a command line interface.

## Pre-Requisites
In order to work correctly PyCorn needs a few things already installed:
* A media player, the default is mplayer, but you can change this as shown below
* [Peerflix](https://github.com/mafintosh/peerflix) for streaming the torrents
* [BeautifulSoup](https://pypi.python.org/pypi/beautifulsoup4/), this is used to get parse html. You can install it this way: ´pip install beautifulsoup4´

## Installing
To install PyCorn Time simply clone the github repository and run the setup.py file:

```
$ git clone https://github.com/sacovo/pycorn-time.git
$ cd pycorn-time
$ python setup.py install # This might require root
```

After installing you can run the program:
´´´
$ pycorntime
´´´

## Configuration
To configure the behavior of the program you can use the file ´~/.pycorn.conf´.
After the first a default file will be written:

```
# This is the config file for pycorntime
# To change a value uncomment the line and make your changes

# Commands

#player_command = /usr/bin/env peerflix "%s" --mplayer
#imdb_command = /bin/xdg-open %s
#download_command = /usr/bin/env aria2c -d {location} "{torrent_link}"

# Uncomment this to disable the welcome message
#show_welcome = false

# YTS-Api values, more information: https://yts.re/api#listDocs

#limit = 20     # 1 - 50 (inclusive)
#quality = all  # 720p, 1080p, 3D, All
#rating = 0     # 0 - 9 (inclusive)
#sort = date    # date, seeds, peers, size, alphabet, rating, downloaded, year
#order = desc   # desc, asc
```


## Screenshots
![](https://raw.githubusercontent.com/sacovo/pycorn-time/gh-pages/images/2014-07-19--1405785255_956x511_scrot.png)
