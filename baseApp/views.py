from django.shortcuts import render, redirect
from . models import Album, Season, Year, Images, Comment
from . forms import AlbumForm, ImagesForm, CommentForm
from django.contrib import messages
from django.db.models import Q



def home(request):
    all_albums = Album.objects.all()
    all_years = Year.objects.all()
    all_seasons = Season.objects.all()
    all_album_images = Images.objects.all()
    return render(request, 'baseApp/home.html', {
        'all_albums': all_albums,
        'all_years': all_years,
        'all_seasons': all_seasons,
        'all_album_images': all_album_images,
    })



def one_season_albums_display(request, pk):
    one_season = Season.objects.get(pk=pk)
    choosen_season = one_season.album_set.all()
    return render(request, 'baseApp/parts/one_season_albums_display.html', {
        'one_season': one_season,
        'choosen_season': choosen_season,
    })



def one_year_album_display(request, pk):
    one_year = Year.objects.get(pk=pk)
    choosen_year = one_year.album_set.all()
    return render(request, 'baseApp/parts/one_year_album_display.html', {
        'one_year': one_year,
        'choosen_year': choosen_year,
    })




def create_new_album_form_display(request):
    form = AlbumForm()
    images_form = ImagesForm()
    return render(request, 'baseApp/parts/create_new_album_form_display.html',{
        'form': form,
        'images_form': images_form,
    })

def create_new_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        files = request.FILES.getlist('images')
        if form.is_valid():
            f = form.save(commit=False)
            f.album_owner = request.user
            f.save()
            for i in files:
                Images.objects.create(
                    album_images = f,
                    images = i                 
                )
            messages.success(request, 'Album created')
            return redirect('create_new_album_form_display')
        else:
            print(form.errors)
    else:
        form = AlbumForm()
        images_form = ImagesForm()

    return render(request, 'baseApp/columns/left_column.html', {
        'form': form,
        'images_form': images_form,
        'messages': messages,
    })



def display_all_images_from_single_album(request, pk):
    album_details = Album.objects.get(pk=pk)
    album_images = album_details.images_set.all()
    return render(request, 'baseApp/parts/display_all_images_from_single_album.html', {
        'album_details': album_details,
        'album_images': album_images,
    })













