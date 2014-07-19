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
from eztv_api import EztvAPI, EztvException
import yts_api


def shorten(s, l, r=">"):
    return s if len(s) <= l else s[0:l-len(r)] + r


def search_movie(**params):
    response = yts_api.search(**params)
    if type(response) != list:
        return None
    movie_list = []
    for movie in response:
        if movie["State"] != "OK":
            continue
        movie_list.append({
            "title-short": shorten(movie["MovieTitleClean"], 30),
            "title": movie["MovieTitle"],
            "year": movie["MovieYear"],
            "quality": movie["Quality"],
            "imdb": movie["ImdbLink"],
            "size": movie["Size"],
            "rating": "*" * int(float(movie["MovieRating"])),
            "genre": movie["Genre"],
            "seeds": movie["TorrentSeeds"],
            "peers": movie["TorrentPeers"],
            "torrent": movie["TorrentMagnetUrl"]
        })
    return movie_list

eztv = EztvAPI()


def search_tv_show(name):
    try:
        eztv.tv_show(name)
    except EztvException:
        return None
    response = eztv.seasons()
    return response
