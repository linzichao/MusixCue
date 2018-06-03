from django.db import models

# Create your models here.
class Member(models.Model):
    UserID = models.IntegerField(primary_key = True)
    UserAccount = models.CharField(max_length = 100)
    UserPassword = models.CharField(max_length = 100)
    UserName = models.CharField(max_length = 100)
    UserAuth = models.CharField(max_length = 100)
    UserEmail = models.CharField(max_length = 100)

class PlayList(models.Model):
    PlayListID = models.IntegerField(primary_key = True)
    PlayListName = models.CharField(max_length = 100)
    CreatedBy = models.ForeignKey('Member')

class Song(models.Model):
    SongID = models.IntegerField(primary_key = True)
    SongName = models.CharField(max_length = 100)
    SongLyrics = models.TextField(blank = True)
    SongLink = models.URLField(blank = False)

class Album(models.Model):
    AlbumID = models.IntegerField(primary_key = True)
    AlbumName = models.CharField(max_length = 100)

class Artist(models.Model):
    ArtistID = models.IntegerField(primary_key = True)
    ArtistName = models.CharField(max_length = 100)

class Release(models.Model):
    ArtistID = models.ForeignKey('Artist')
    AlbumID = models.ForeignKey('Album')
    class Meta:
        unique_together = ( ('ArtistID', 'AlbumID'),  )

class BelongTo(models.Model):
    AlbumID = models.ForeignKey('Album')
    SongID = models.ForeignKey('Song')
    class Meta:
        unique_together = ( ('AlbumID', 'SongID'), )

class AddTo(models.Model):
    SongID = models.ForeignKey('Song')
    PlayListID = models.ForeignKey('PlayList')
    class Meta:
        unique_together = ( ('SongID', 'PlayListID'), )

class CommentOn(models.Model):
    CommentID = models.IntegerField(primary_key = True)
    CommentContent = models.TextField()
    CommentTime = models.DateTimeField(auto_now_add = True)
    MemberID = models.ForeignKey('Member')
    SongID = models.ForeignKey('Song')
