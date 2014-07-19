from eztv_api import EztvAPI, EztvException
import yts_api


def search_movie(**params):
    response = yts_api.search(**params)
    if type(response) != list:
        return None
    movie_list = []
    for movie in response:
        if movie["State"] != "OK":
            continue
        movie_list.append({
            "title": movie["MovieTitleClean"],
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

