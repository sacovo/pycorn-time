# -*- coding: utf-8 -*-
# This file is part of 'pycorn-time' a cli-version of popcorntime, a torrent
# streaming software
# Copyright (C) 2014  Sandro Covo

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import sys
import urllib.parse
import subprocess
import os
import webbrowser
from pycorn.unified_api import search_movie, search_tv_show
settings_dict = {
    'player_command': '/usr/bin/env peerflix "%s" --mplayer',
    'imdb_command': '/bin/xdg-open %s',
    'download_command': '/usr/bin/env aria2c -d {location} "{torrent_link}"'
    }

config_path = os.path.join(os.environ['HOME'], '.pycorn.conf')

if not os.path.isfile(config_path):
    import shutil
    shutil.copyfile('default_config.conf', config_path)


def read_config():
    with open(config_path, "r") as conf:
        conf_dict = {
            'limit': '20',
            'quality': 'all',
            'rating': '0',
            'sort': 'date',
            'order': 'desc'
            }
        for l in conf.readlines():
            l = l[0:l.find('#')] if('#' in l) else l
            try:
                k, v = l.lower().split("=")
                k, v = k.strip(), v.strip()
                if k in conf_dict.keys():
                    conf_dict[k] = v
                elif k in settings_dict.keys():
                    settings_dict[k] = v
            except Exception:
                continue

    return conf_dict

read_config()


def prompt_exit():
    a = input("\n\x1b[1;31mAre you sure? (y/n): \x1b[0m")
    if a.lower() in ("yes", "y"):
        sys.exit(0)


def input_wrapper(prompt, color=7):
    ps = "\x1b[1;3{color}m{prompt}\x1b[0m".format(color=color, prompt=prompt)
    while 1:
        try:

            i = input(ps).lower()
            if i == 'q':
                prompt_exit()
                continue
            return i
        except KeyboardInterrupt:
            prompt_exit()


def input_number(prompt, empty_value='', color=8):
    nr = None
    while nr is None:
        try:
            nr = int(input_wrapper(prompt, color) or empty_value)
        except ValueError:
            nr = None
    return nr


def watch_movie(torrent_link, imdb='', movie_title=''):
    while 1:
        null = open('NUL', "w")
        print("\x1b[1;35m{}\x1b[0m".format(movie_title))
        choice = input_wrapper("(W)atch selected movie, open (I)MDb, (d)ownl" +
                               "oad movie or (r)eturn to main menu: ", 4) \
            or 'w'
        if choice == 'w':
            print("Starting stream, this could take a while...")
            try:
                subprocess.call([settings_dict['player_command'] %
                                torrent_link, ],
                                shell=True, stdin=subprocess.PIPE)
            except KeyboardInterrupt:
                pass

        if choice == 'i':
            if settings_dict['imdb_command']:
                subprocess.call([settings_dict['imdb_command'] % imdb],
                                stdout=None, shell=True)
            else:
                webbrowser.open(imdb)

        if choice == 'd':
            path = input_wrapper("Enter download folder: ")
            subprocess.call([settings_dict['download_command'].format(
                            torrent_link=torrent_link, location=path)],
                            shell=True)

        null.close()
        if choice == 'r':
            return 0


def search_show():
    term = input_wrapper("Enter title of the show: ")
    if term is '':
        print("No results! :/")
        return 0
    result = search_tv_show(term)

    if result is None:
        print("No results! :/")
        return 0

    s = input_number("Enter Season {!r}: ".format(list(result.keys())))
    e = input_number("Enter Episode {!r}: ".format(list(result[s].keys())))
    imdb = 'http://www.imdb.com/find?s=' + urllib.parse.quote(term)
    watch_movie(result[s][e], imdb, term.title())
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
        if result is None:
            print("No results! :/")
            return 0
        print("┌────┬──────────────────────────────┬──────────┬────────\
─┬──────────┬─────────────┬─────────┬─────────┐")
        print("│ Nr │            Title             │   Year   │ Quality\
 │  Rating  │    Genre    │  Seeds  │  Peers  │")
        print("│────┼──────────────────────────────┼──────────┼────────\
─┼──────────┼─────────────┼─────────┼─────────│")
        for i, movie in enumerate(result):
            print("│{nr: >3} │\x1b[1;36m{title-short: <30}\x1b[0m│{year:\
^10}│\x1b[1;32m{quality: ^9}\x1b[0m\
│\x1b[1;33m{rating: >10}\x1b[0m│{genre: ^13}│{seeds: >8} │{peers: >8} \
│".format(**dict(nr=i+1, **movie)))
        print("└────┴──────────────────────────────┴──────────┴────────\
─┴──────────┴─────────────┴─────────┴─────────┘")
        nr = input_number("Enter number of movie (enter to see more): ", 0)
    watch_movie(result[nr-1]['torrent'], result[nr-1]['imdb'],
                "{title}".format(**result[nr-1]))
    return 0


def main():
    i = input_wrapper("Search (m)ovie, tv (s)how or (q)uit [m]: ") or 'm'
    if i == 's':
        return search_show()
    if i == 'm':
        return _search_movie()
    else:
        print("Invalid input! ;(")
        return 0


def main_loop():
    while 1:
        main()
