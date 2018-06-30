from django.db import models
from django.contrib.auth.models import User

class PlayList(models.Model):
    PlayListID = models.IntegerField(primary_key = True)
    PlayListName = models.CharField(max_length = 100)
    CreatedBy = models.ForeignKey(User)

class Song(models.Model):
    SongID = models.IntegerField(primary_key = True)
    SongName = models.CharField(max_length = 100)
    SongLyrics = models.TextField(blank = True)
    SongLink = models.URLField(blank = False)
    def __str__(self):
        return 'Song: {}'.format(self.SongName)

class Album(models.Model):
    AlbumID = models.IntegerField(primary_key = True)
    AlbumName = models.CharField(max_length = 100)
    def __str__(self):
        return 'Album: {}'.format(self.AlbumName)

class Artist(models.Model):
    ArtistID = models.IntegerField(primary_key = True)
    ArtistName = models.CharField(max_length = 100)
    def __str__(self):
        return 'Artist: {}'.format(self.ArtistName)

class Release(models.Model):
    ArtistID = models.ForeignKey(Artist)
    AlbumID = models.ForeignKey(Album)
    class Meta:
        unique_together = ( ('ArtistID', 'AlbumID'),  )

class BelongTo(models.Model):
    AlbumID = models.ForeignKey(Album)
    SongID = models.ForeignKey(Song)
    class Meta:
        unique_together = ( ('AlbumID', 'SongID'), )

class AddTo(models.Model):
    SongID = models.ForeignKey(Song)
    PlayListID = models.ForeignKey(PlayList)
    class Meta:
        unique_together = ( ('SongID', 'PlayListID'), )

class CommentOn(models.Model):
    CommentID = models.IntegerField(primary_key = True)
    CommentContent = models.TextField()
    CommentTime = models.DateTimeField(auto_now_add = True)
    UserID = models.ForeignKey(User)
    SongID = models.ForeignKey(Song)

