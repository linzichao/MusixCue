
import lyricwikia
import json
import time
import sys

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
        if 'imUrl' not in data:
            continue
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
                    time.sleep(2) # let's be gentle
                except Exception:
                    pass
                else:
                    pass
                    songs.append( { "pk": first_unused_songid
                                  , "model": "music.song"
                                  , "fields": { "SongID": first_unused_songid
                                              , "SongName": s['title']
                                              , "SongLyrics": lyrics
                                              , "SongLink": data['imUrl']
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

