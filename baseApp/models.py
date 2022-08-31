from distutils.command.upload import upload
from django.db import models
from django.conf import settings
from django_resized import ResizedImageField
from django.core.validators import MinValueValidator, MaxValueValidator



class Season(models.Model):
    season_name = models.CharField(max_length=255, null=True, blank=False)
    def __str__(self):
        return f'{self.season_name}'



class Year(models.Model):
    album_year = models.IntegerField(
        validators=[MinValueValidator(1990), MaxValueValidator(2022)], default=2022
        )
    def __str__(self):
        return f'{self.album_year}'
    class Meta:
        ordering = ['-album_year']



class Album(models.Model):
    album_name = models.CharField(max_length=255, null=True)
    album_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    season_name = models.ForeignKey(Season, on_delete=models.CASCADE, null=True)
    album_year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
    album_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f'{self.album_name}, {self.season_name}, {self.album_created.date()}'
    class Meta:
        ordering = ['-album_created']



class Images(models.Model):
    images = models.ImageField(upload_to='images/')
    album_images = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=False)



class Comment(models.Model):
    comment = models.CharField(max_length=1000, null=True, blank=False)
    commented_album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=False)
    comment_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  null=True, blank=False)
    comment_created = models.DateTimeField(auto_now_add=True, null=True, blank=False)
    def __str__(self):
        return f'{self.comment_owner}, {self.comment}, {self.commented_album}, {self.comment_created.date()}'