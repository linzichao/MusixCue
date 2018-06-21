from django.shortcuts import render
from django.db import models
from django.http import HttpResponseRedirect

from music.models import Song, Album, Artist, BelongTo, Release

# Create your views here.

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

            SongID = request.GET.get('songid', '')

            ThisSongName = Song.objects.get(SongID=int(SongID)).SongName
            ThisSongLyrics = Song.objects.get(SongID=int(SongID)).SongLyrics

            SongBelongAlbum = BelongTo.objects.get(SongID_id=SongID)
            ArtistReleaseAlbum = Release.objects.get(AlbumID=SongBelongAlbum.AlbumID_id)

            ThisAlbumName = Album.objects.get(AlbumID=SongBelongAlbum.AlbumID_id).AlbumName
            ThisArtistName = Artist.objects.get(ArtistID=ArtistReleaseAlbum.ArtistID_id).ArtistName


            return render(request, 'comment.html', locals())
    else:
        return HttpResponseRedirect("/accounts/login/")
