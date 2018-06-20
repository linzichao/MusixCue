from django.shortcuts import render
from django.db import models
from django.http import HttpResponseRedirect, HttpResponse
from music.models import Song, Album, Artist, Release, BelongTo
# Create your views here.

def search(request):
    song, album, artist = request.GET['song'], request.GET['album'], request.GET['artist']
    #songs = Song.objects.filter(SongName__icontains= song)
    #albums = Album.objects.filter(AlbumName__icontains= album)
    #artists = Artist.objects.filter(ArtistName__icontains= artist)
    #AlbumID__AlbumName__icontains= album,
    sql = """select * from music_song as SONG \
                INNER JOIN music_belongto as BLON \
                    on SONG.SongID = BLON.SongID_id \
                INNER JOIN music_album as ALB \
                    on BLON.AlbumID_id = ALB.AlbumID \
                INNER JOIN music_release as REL \
                    on ALB.AlbumID = REL.AlbumID_id \
                INNER JOIN music_artist as ART \
                    on REL.ArtistID_id = ART.ArtistID"""
    songs = Song.objects.raw(sql)
    for s in songs:
        print("SongName: {}, AlbumName: {}, ArtistName: {}".format(s.SongName, s.AlbumName, s.ArtistName))
    return HttpResponse("song = {}, album = {}, artist = {}".format(song, album, artist) )


def index(request):
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
            return render(request, 'comment.html', locals())
    else:
        return HttpResponseRedirect("/accounts/login/")
