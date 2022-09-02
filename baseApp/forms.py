from xml.etree.ElementTree import Comment
from django import forms
from django.forms import ModelForm
from django.db.models import fields
from . models import Album, Images, Comment


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = '__all__'
        exclude = ['album_owner']




class ImagesForm(ModelForm):
    images = forms.ImageField(
        label='Images', 
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
    )
    class Meta:
        model = Images
        fields = '__all__'
        exclude = ['album_images']




class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ['comment_owner', 'commented_album']