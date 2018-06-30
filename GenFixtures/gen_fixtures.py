
import lyricwikia
import json
import time
import sys

import urllib.request
import urllib.parse
import re

# https://www.codeproject.com/Articles/873060/Python-Search-Youtube-for-Video
def get_yt_url(keyword):
    query_string = urllib.parse.urlencode({"search_query" : keyword})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    return "http://www.youtube.com/watch?v=" + search_results[0]

first_unused_songid = 1
first_unused_albumid = 1
first_unused_artistid = 1

songs = []
albums = []
belongtos = []
artists = []
releases = []
artist2ArtistID = {}

with open('mard/mard_metadata.json') as f:
    for line in f.readlines():
        data = json.loads(line)
        if 'salesRank' not in data:
            continue
        if 'Music' not in data['salesRank']:
            continue
        if data['salesRank']['Music'] > 256: # we only care popular albums
            continue
        if 'artist' not in data:
            continue
        if 'songs' in data:
            for s in data['songs']:
                print("trying to get lyrics of {", "artist: ", data['artist'], "; album title: ", data['title'], "; track title: ", s['title'], "}", file=sys.stderr)
                try:
                    pass
                    lyrics = lyricwikia.get_lyrics(data['artist'], s['title'])
                    time.sleep(5) # let's be gentle
                except Exception:
                    pass
                else:
                    try:
                        youtube_link = get_yt_url(data['artist'] + " " + s['title']);
                    except Exception as e:
                        print(e)
                    else:
                        print(youtube_link)
                    songs.append( { "pk": first_unused_songid
                                  , "model": "music.song"
                                  , "fields": { "SongID": first_unused_songid
                                              , "SongName": s['title']
                                              , "SongLyrics": lyrics
                                              , "SongLink": youtube_link
                                              }
                                  }
                                )
                    belongtos.append( { "model": "music.belongto"
                                      , "fields": { "AlbumID": first_unused_albumid, "SongID": first_unused_songid }
                                      }
                                    )
                    first_unused_songid += 1
            if data['artist'] not in artist2ArtistID:
                artists.append( { "pk": first_unused_artistid
                                , "model": "music.artist"
                                , "fields": { "ArtistID": first_unused_artistid, "ArtistName": data['artist'] }
                                }
                              )
                artist2ArtistID[data['artist']] = first_unused_artistid
                first_unused_artistid += 1
            releases.append( { "model": "music.release"
                             , "fields": { "ArtistID": artist2ArtistID[data['artist']], "AlbumID": first_unused_albumid}
                             }
                           )
            albums.append( { "pk": first_unused_albumid
                           , "model": "music.album"
                           , "fields": { "AlbumID": first_unused_albumid, "AlbumName": data['title'] }
                           }
                         )
            first_unused_albumid += 1

with open('output.json', 'w') as outfile:
    json.dump(songs + albums + belongtos + artists + releases, outfile)

