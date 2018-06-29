from django.shortcuts import render
from django.db import models
from django.http import HttpResponseRedirect, HttpResponse
from music.models import Song, Album, Artist, Release, BelongTo
# Create your views here.

def search(request):
    song, album, artist = request.GET['song'], request.GET['album'], request.GET['artist']

    song_like = "%%" if song == "" else "%%{}%%".format(song)
    artist_like = "%%" if artist == "" else "%%{}%%".format(artist)
    album_like = "%%" if album == "" else "%%{}%%".format(album)
    sql = "select * from music_song as SONG \
                INNER JOIN music_belongto as BLON \
                    on SONG.SongID = BLON.SongID_id \
                INNER JOIN music_album as ALB \
                    on BLON.AlbumID_id = ALB.AlbumID \
                INNER JOIN music_release as REL \
                    on ALB.AlbumID = REL.AlbumID_id \
                INNER JOIN music_artist as ART \
                    on REL.ArtistID_id = ART.ArtistID \
            WHERE \
                SONG.SongName LIKE \"{}\" AND \
                ALB.AlbumName LIKE \"{}\" AND \
                ART.ArtistName LIKE \"{}\" ".format(song_like, album_like, artist_like)

    songs = Song.objects.raw(sql)

    ls_return = []
    for s in songs:
        one_tuple = {}
        one_tuple['SongName'] = s.SongName
        one_tuple['AlbumName'] = s.AlbumName
        one_tuple['ArtistName'] = s.ArtistName
        one_tuple['SongID'] = s.SongID
        one_tuple['SongLink'] = s.SongLink
        ls_return.append(one_tuple)

    username = None
    if request.user.is_authenticated():
        username = request.user.username

    return render(request, 'index.html', locals())

def index(request):

    sql = "select * from music_song as SONG \
                INNER JOIN music_belongto as BLON \
                    on SONG.SongID = BLON.SongID_id \
                INNER JOIN music_album as ALB \
                    on BLON.AlbumID_id = ALB.AlbumID \
                INNER JOIN music_release as REL \
                    on ALB.AlbumID = REL.AlbumID_id \
                INNER JOIN music_artist as ART \
                    on REL.ArtistID_id = ART.ArtistID "

    songs = Song.objects.raw(sql)

    ls_return = []

    for s in songs:
        one_tuple = {}
        one_tuple['SongName'] = s.SongName
        one_tuple['AlbumName'] = s.AlbumName
        one_tuple['ArtistName'] = s.ArtistName
        one_tuple['SongID'] = s.SongID
        one_tuple['SongLink'] = s.SongLink
        ls_return.append(one_tuple)

    username = None
    if request.user.is_authenticated():
        username = request.user.username

    return render(request, 'index.html', locals())

# User's playlist
def playlist(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            return render(request, 'playlist.html', locals())
    else:
        return HttpResponseRedirect("/accounts/login/")

def comment(request):
    if request.user.is_authenticated():
        if request.method == 'GET':

            SongID = request.GET.get('songid', '')

            ThisSongName = Song.objects.get(SongID=int(SongID)).SongName
            ThisSongLyrics = Song.objects.get(SongID=int(SongID)).SongLyrics

            #ThisSongLyrics = ThisSongLyrics.replace('\n','<br>')

            SongBelongAlbum = BelongTo.objects.get(SongID_id=SongID)
            ArtistReleaseAlbum = Release.objects.get(AlbumID=SongBelongAlbum.AlbumID_id)

            ThisAlbumName = Album.objects.get(AlbumID=SongBelongAlbum.AlbumID_id).AlbumName
            ThisArtistName = Artist.objects.get(ArtistID=ArtistReleaseAlbum.ArtistID_id).ArtistName


            return render(request, 'comment.html', locals())
    else:
        return HttpResponseRedirect("/accounts/login/")
