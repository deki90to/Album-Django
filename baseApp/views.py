from django.shortcuts import render, redirect
from . models import Album, Season, Year, Images, Comment
from . forms import AlbumForm, ImagesForm, CommentForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


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


# @login_required(login_url='login')
# def display_my_albums(request):
#     my_albums = Album.objects.all()
#     return render(request, 'baseApp/parts/display_my_albums.html', {
#         'my_albums': my_albums,
#     })

@login_required(login_url='login')
def one_season_albums_display(request, pk):
    one_season = Season.objects.get(pk=pk)
    choosen_season = one_season.album_set.all()
    return render(request, 'baseApp/parts/one_season_albums_display.html', {
        'one_season': one_season,
        'choosen_season': choosen_season,
    })

@login_required(login_url='login')
def one_year_album_display(request, pk):
    one_year = Year.objects.get(pk=pk)
    choosen_year = one_year.album_set.all()
    return render(request, 'baseApp/parts/one_year_album_display.html', {
        'one_year': one_year,
        'choosen_year': choosen_year,
    })


# ALBUM CREATING
@login_required(login_url='login')
def create_new_album_form_display(request):
    form = AlbumForm()
    images_form = ImagesForm()
    return render(request, 'baseApp/parts/create_new_album_form_display.html',{
        'form': form,
        'images_form': images_form,
    })

@login_required(login_url='login')
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
            return redirect('create_new_album')
        else:
            print(form.errors)
    else:
        form = AlbumForm()
    content = '<h5> Album created </h5>'
    return HttpResponse(content)





@login_required(login_url='login')
def display_all_images_from_single_album(request, pk):
    # global album_details used in commented_album
    global album_details
    album_details = Album.objects.get(pk=pk)
    album_images = album_details.images_set.all()
    return render(request, 'baseApp/parts/display_all_images_from_single_album.html', {
        'album_details': album_details,
        'album_images': album_images,
    })




#COMMENTS
@login_required(login_url='login')
def comment_form_display(request):
    comment_form = CommentForm()
    return render(request, 'baseApp/parts/comment_form_display.html', {
        'comment_form': comment_form,
        'album_details': album_details,
    })

@login_required(login_url='login')
def create_comment(request):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # comment_form.save()
            f = comment_form.save(commit=False)
            f.comment_owner = request.user
            f.commented_album = album_details
            f.save()
            messages.success(request, 'Comment created')
            return redirect('comment_form_display')
        else:
            comment_form = CommentForm()
    content = '<h5> Comment created </h5>'
    return HttpResponse(content)



@login_required(login_url='login')
def display_my_albums(request):
    my_albums = Album.objects.all()
    return render(request, 'baseApp/parts/display_my_albums.html', {
        'my_albums': my_albums,
    })



@login_required(login_url='login')
def albums_search(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    searched_albums = Album.objects.filter(Q(album_name__icontains=q))
    return render(request, 'baseApp/parts/albums_search.html', {
        'searched_albums': searched_albums,
         'q': q,
    })