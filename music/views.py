from django.shortcuts import render
from django.db import models
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from music.models import Song, Album, Artist, Release, BelongTo, PlayList, AddTo
from django.contrib.auth.models import User
import json

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
        one_tuple['Art_Song'] = s.ArtistName + ' - ' + s.SongName
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
        one_tuple['Art_Song'] = s.ArtistName + ' - ' + s.SongName
        ls_return.append(one_tuple)

    username = None
    if request.user.is_authenticated():
        username = request.user.username

    return render(request, 'index.html', locals())

# User's playlist
def playlist(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            PlayListing = PlayList.objects.filter(CreatedBy = request.user)
            ls_return = []

            for p in PlayListing:

                sql = "select * from music_song as SONG \
                        INNER JOIN music_belongto as BLON \
                            on SONG.SongID = BLON.SongID_id \
                        INNER JOIN music_album as ALB \
                            on BLON.AlbumID_id = ALB.AlbumID \
                        INNER JOIN music_release as REL \
                            on ALB.AlbumID = REL.AlbumID_id \
                        INNER JOIN music_artist as ART \
                            on REL.ArtistID_id = ART.ArtistID \
                        INNER JOIN music_addto as ADDTO \
                            on ADDTO.SongID_id = SONG.SongID \
                        WHERE \
                            PlayListID_id = \"{}\" ".format(p.PlayListID)

                songs = Song.objects.raw(sql)


                ls_songs = []

                for s in songs:
                    ls_songs.append({ 'SongName': s.SongName, 'AlbumName': s.AlbumName,
                        'ArtistName': s.ArtistName, 'SongID':s.SongID })

                print(ls_songs)
                ls_return.append({ 'playlist_id': p.PlayListID, 'playlist_name': p.PlayListName
                           , 'songs': ls_songs })



            return render(request, 'playlist.html', locals())
    else:
        return HttpResponseRedirect("/accounts/login/")

def create_playlist(request):
    if request.user.is_authenticated():
        if request.GET:
            pid = 1
            while PlayList.objects.filter(PlayListID = pid):
                pid += 1 # find the first unused pid, stupid and can be problematic when there are concurrent requests
            p = PlayList.objects.create(
                    PlayListID = pid ,
                    PlayListName = request.GET['playlist_name'],
                    CreatedBy = request.user
                )
            p.save()
            return HttpResponse('ok, playlist id = ' + str(pid), status=200)
        else:
            return HttpResponse('Bad Request', status=400)
    else:
        return HttpResponse('Unauthorized', status=401)

def delete_playlist(request):
    if request.user.is_authenticated():
        if request.GET:
            p = PlayList.objects.filter(PlayListID = request.GET['playlist_id'])
            if p:
                p.delete()
                return HttpResponse('ok', status=200)
            else:
                return HttpResponse('playlist not found', status=200)
        else:
            return HttpResponse('Bad Request', status=400)
    else:
        return HttpResponse('Unauthorized', status=401)

def modify_playlist_name(request):
    if request.user.is_authenticated():
        if request.GET:
            a = PlayList.objects.get(PlayListID = request.GET['playlist_id'])
            
            if a:
                a.PlayListName = request.GET['playlist_name']
                a.save()
                return HttpResponse('ok', status=200)
            else:
                return HttpResponse('playlist not found or name is null', status=200)
        else:
            return HttpResponse('Bad Request', status=400)
    else:
        return HttpResponse('Unauthorized', status=401)

def add_song_to_playlist(request):
    if request.user.is_authenticated():
        if request.GET:
            a = AddTo.objects.create(
                    SongID = Song.objects.get(SongID = request.GET['song_id']),
                    PlayListID = PlayList.objects.get(PlayListID = request.GET['playlist_id'])
                )
            a.save()
            return HttpResponse('Ok', status=200)
        else:
            return HttpResponse('Bad Request', status=400)
    else:
        return HttpResponse('Unauthorized', status=401)

def delete_song_from_playlist(request):
    if request.user.is_authenticated():
        if request.GET:
            p = PlayList.objects.filter(
                    SongID = Song.objects.get(SongID = request.GET['song_id']),
                    PlayListID = PlayList.objects.get(PlayListID = request.GET['playlist_id'])
            )
            if p:
                p.delete()
                return HttpResponse('ok', status=200)
            else:
                return HttpResponse('record not found', status=200)
        else:
            return HttpResponse('Bad Request', status=400)
    else:
        return HttpResponse('Unauthorized', status=401)


def get_my_playlist(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            x = PlayList.objects.filter(CreatedBy = request.user)
            return JsonResponse({'data': list(x.values())})
        else:
            return HttpResponse('Bad Request', status=400)
    else:
        return HttpResponse('Unauthorized', status=401)

def get_my_playlist_with_song_info(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            playlists = PlayList.objects.filter(CreatedBy = request.user)
            ret = []
            for p in playlists:
                a = AddTo.objects.filter(PlayListID = p.PlayListID)
                print({ 'playlist_name': p.PlayListName
                       , 'songs': list(Song.objects.filter(SongID__in = a).values()) })
                ret.append( { 'playlist_name': p.PlayListName
                       , 'songs': list(Song.objects.filter(SongID__in = a).values()) })
            return JsonResponse({'data': ret})
        else:
            return HttpResponse('Bad Request', status=400)
    else:
        return HttpResponse('Unauthorized', status=401)

def comment(request):
    if request.user.is_authenticated():
        if request.method == 'GET':

            SongID = request.GET.get('songid', '')
            song = Song.objects.get(SongID=int(SongID))
            ThisSongName = Song.objects.get(SongID=int(SongID)).SongName
            ThisSongLyrics = Song.objects.get(SongID=int(SongID)).SongLyrics

            #ThisSongLyrics = ThisSongLyrics.replace('\n','<br>')

            SongUrl = Song.objects.get(SongID=int(SongID)).SongLink
            SongBelongAlbum = BelongTo.objects.get(SongID_id=SongID)
            ArtistReleaseAlbum = Release.objects.get(AlbumID=SongBelongAlbum.AlbumID_id)

            ThisAlbumName = Album.objects.get(AlbumID=SongBelongAlbum.AlbumID_id).AlbumName
            ThisArtistName = Artist.objects.get(ArtistID=ArtistReleaseAlbum.ArtistID_id).ArtistName


            return render(request, 'comment.html', locals())
    else:
        return HttpResponseRedirect("/accounts/login/")

def test_page(request):
    return render(request, "test_page.html", locals())
