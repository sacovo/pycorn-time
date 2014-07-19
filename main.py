#!/usr/bin/env python3
import sys
import urllib.parse
import subprocess
import os
import webbrowser
from unified_api import search_movie, search_tv_show
settings_dict = {
        'player_command':'/usr/bin/env peerflix "%s" --mplayer',
        'imdb_command': '/bin/xdg-open %s',
        'download_command': '/usr/bin/env aria2c -d {location} "{torrent_link}"'
    }

def read_config():
    with open(os.path.join(os.environ['HOME'], '.pycorn.conf'), "r") as conf:
        conf_dict = {
            'limit':'20',
            'quality': 'all',
            'rating': '0',
            'sort': 'date',
            'order': 'desc'
            }
        for l in conf.readlines():
            l = l[0:l.find('#')] if('#' in l ) else l
            try:
                k,v = l.lower().split("=")
                k,v = k.strip(), v.strip()
                if k in conf_dict.keys():
                    conf_dict[k] = v
                elif k in settings_dict.keys():
                    settings_dict[k] = v
            except Exception:
                continue

    return conf_dict

read_config()

def prompt_exit():
    a = input("\nAre you sure? (y/n): ")
    if a.lower() in ("yes", "y"):
        sys.exit(0)

def input_wrapper(prompt):
    while 1:
        try:
            i = input(prompt).lower()
            if i == ':q':
               prompt_exit()
               continue
            return i
        except KeyboardInterrupt:
            prompt_exit()


def input_number(prompt, empty_value=''):
    nr = None
    while nr == None:
        try:
            nr = int(input_wrapper(prompt) or empty_value)
        except ValueError:
            nr = None
    return nr


def watch_movie(torrent_link, imdb=''):
    while 1:
        null = open('NUL', "w")
        choice = input_wrapper("(W)atch selected movie, open (I)MDb, (d)ownload movie or (r)eturn to main menu: ") or 'w'
        if choice == 'w':
            print("Starting stream, this could take a while...")
            subprocess.call([settings_dict['player_command'] % torrent_link, ], shell=True)

        if choice == 'i':
            if settings_dict['imdb_command']:
                subprocess.call([settings_dict['imdb_command'] % imdb], stdout=None, shell=True)
            else:
                webbrowser.open(imdb)

        if choice == 'd':
            path = input_wrapper("Enter download folder: ")
            subprocess.call([settings_dict['download_command'].format(torrent_link=torrent_link, location=path)], shell=True)

        null.close()
        if choice == 'r':
            return 0


def search_show():
    term = input_wrapper("Enter title of the show: ")
    if term == None:
        print("No results! :/")
        return 0
    result = search_tv_show(term)

    if result == None:
        print("No results! :/")
        return 0

    s = input_number("Enter Season {!r}: ".format(list(result.keys())))
    e = input_number("Enter Episode {!r}: ".format(list(result[s].keys())))
    imdb = 'http://www.imdb.com/find?s=' + urllib.parse.quote(term)
    watch_movie(result[s][e], imdb)
    return 0

def _search_movie():
    params = dict()
    params['keywords'] = input_wrapper("Enter Keywords: ")
    params['genre'] = input_wrapper("Enter genre: ") or "All"
    params['set'] = 0
    params.update(read_config())

    nr = 0
    while nr == 0:
        params['set'] += 1
        result = search_movie(**params)
        if result == None:
            print("No results! :/")
            return 0
        print("┏━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┯━━━━━━━━━━┯━━━━━━━━━┯━━━━━━━━━━┯━━━━━━━━━━━━━┯━━━━━━━━━┯━━━━━━━━━┓")
        print("┃ Nr ┆            Title             ┆   Year   ┆ Quality ┆  Rating  ┆    Genre    ┆  Seeds  ┆  Peers  ┃")
        print("┠────┼──────────────────────────────┼──────────┼─────────┼──────────┼─────────────┼─────────┼─────────┨")
        for i, movie in enumerate(result):
            print("┃{nr: >3} ┆{title: <30}┆{year: ^10}┆{quality: ^9}┆{rating: >10}┆{genre: ^13}┆{seeds: >8} ┆{peers: >8} ┃".format(**dict(nr=i+1, **movie)))
        print("┗━━━━┷━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┷━━━━━━━━━━┷━━━━━━━━━┷━━━━━━━━━━┷━━━━━━━━━━━━━┷━━━━━━━━━┷━━━━━━━━━┛")
        nr = input_number("Enter number of movie (enter to see more): ", 0)
    watch_movie(result[nr-1]['torrent'], result[nr-1]['imdb'])
    return 0

def main():
    i = input_wrapper("Search (m)ovie, tv (s)how or (q)uit [m]: ") or 'm'
    if i == 'q':
        return 1
    if i == 's':
        return search_show()
    if i == 'm':
        return _search_movie()
    else:
        print("Invalid input! ;(")
        return 0

code = 0
while code == 0:
    code = main()
