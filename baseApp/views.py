from django.shortcuts import render, redirect
from . models import Album, Season, Year, Images, Comment
from . forms import AlbumForm, ImagesForm, CommentForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import EmptyPage, Paginator
from django.core.mail import send_mail


@login_required(login_url='login')
def home(request):
    album_p = Paginator(Album.objects.all(), 5)
    page = request.GET.get('page')
    try:
        all_albums = album_p.get_page(page)
    except EmptyPage:
        all_albums = album_p.get_page(album_p.num_pages)

    # all_albums = Album.objects.all()
    all_years = Year.objects.all()
    all_seasons = Season.objects.all()
    all_album_images = Images.objects.all()
    return render(request, 'baseApp/home.html', {
        'all_albums': all_albums,
        'all_years': all_years,
        'all_seasons': all_seasons,
        'all_album_images': all_album_images,
    })



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
    all_albums = Album.objects.all()
    form = AlbumForm()
    images_form = ImagesForm()
    return render(request, 'baseApp/parts/create_new_album_form_display.html',{
        'form': form,
        'images_form': images_form,
        'all_albums': all_albums,
    })

@login_required(login_url='login')
def create_new_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        files = request.FILES.getlist('images')
        if len(files) > 20:
            content = '<p> Max number of images is 20 </p>'
            return HttpResponse(content)
        else:
            if form.is_valid():
                f = form.save(commit=False)
                f.album_owner = request.user
                f.save()
                for i in files:
                    Images.objects.create(
                        album_images = f,
                        images = i                 
                    )
                email = f.album_owner.email
                subject = f.album_name
                message = f"Album {f.album_name} successfully created, check it here http://localhost:8000/"
                send_mail(
                    subject,
                    message,
                    email,
                    [f.album_owner.email, 'deki90to@gmail.com']
                )
                return redirect('display_my_albums')
                # content = f"<p>{f.album_name} album was created <a href='/' boost='true'> <b> refresh </b> </a></p>"
                # return HttpResponse(content)
            # else:
            #     print(form.errors)
    # else:
    #     form = AlbumForm()
    # content = '<p> Album created </p>'
    # return HttpResponse(content)


def redirect_to_right_column(request):
    all_albums = Album.objects.all()
    return render(request, 'baseApp/columns/right_column.html', {
        'all_albums': all_albums,
    })



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
            # messages.success(request, 'Comment created')
            # if f.comment_owner.email != f.commented_album.album_owner.email:
            email = f.comment_owner.email
            subject = f.comment
            message = f"Comment >>>>> {f.comment} <<<<< successfully created"
            if f.comment_owner.email != f.commented_album.album_owner.email:
                send_mail(
                    subject,
                    message,
                    email,
                    [f.commented_album.album_owner.email, 'deki90to@gmail.com']
                )
            if f.comment_owner.email == f.commented_album.album_owner.email:
                send_mail(
                    subject,
                    message,
                    email,
                    ['deki90to@gmail.com']
                )
            return redirect('comment_form_display')
        else:
            comment_form = CommentForm()
        # content = '<h5> Comment created </h5>'
        # return HttpResponse(content)



@login_required(login_url='login')
def display_my_albums(request):
    my_albums = Album.objects.all()
    return render(request, 'baseApp/parts/display_my_albums.html', {
        'my_albums': my_albums,
    })



@login_required(login_url='login')
def albums_search(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    searched_albums = Album.objects.filter(
        Q(album_name__icontains=q) 
        | 
        Q(album_owner__email__icontains=q)
    )
    return render(request, 'baseApp/parts/albums_search.html', {
        'searched_albums': searched_albums,
         'q': q,
    })



@login_required(login_url='login')
def delete_album(request, pk):
    delete_album = Album.objects.get(pk=pk)
    if request.method == 'DELETE':
        delete_album.delete()
        content = f"<p> {delete_album.album_name} - album is deleted </p>"
        return HttpResponse(content)

def delete_album_comment(request, pk):
    album_comment = Comment.objects.get(pk=pk)
    if request.method == 'DELETE':
        album_comment.delete()
        content = "<p> Comment deleted </p>"
        return HttpResponse(content)




def display_participants(request):
    participants = Comment.objects.all()
    return render(request, 'baseApp/parts/display_participants.html', {
        'participants': participants,
    })



def all_albums_display(request):
    album_p = Paginator(Album.objects.all(), 5)
    page = request.GET.get('page')
    try:
        all_albums = album_p.get_page(page)
    except EmptyPage:
        all_albums = album_p.get_page(album_p.num_pages)

    return render(request, 'baseApp/parts/all_albums_display.html', {
        'all_albums': all_albums, 
        'album_p': album_p, 
        'page': page
    })
    

def album_slideshow(request, pk):
    album_details = Album.objects.get(pk=pk)
    album_images = album_details.images_set.all()
    return render(request, 'baseApp/parts/album_slideshow.html', {
        'album_details': album_details,
        'album_images': album_images,
    })