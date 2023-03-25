from django.shortcuts import render, redirect
from . models import Album, Season, Year, Images, Comment
from . forms import AlbumForm, ImagesForm, CommentForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import EmptyPage, Paginator
from django.core.mail import send_mail
from members.models import CustomUser
from django.urls import reverse
from members.models import Profile
from django.shortcuts import render, get_object_or_404, redirect
from chat.models import ChatMessages
# from django.contrib import settings


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
    chat_messages = ChatMessages.objects.all()
    return render(request, 'baseApp/home.html', {
        'all_albums': all_albums,
        'all_years': all_years,
        'all_seasons': all_seasons,
        'all_album_images': all_album_images,
        'chat_messages': chat_messages
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
                subject = 'Album created'
                message = f"Album '{f.album_name}' successfully created, check it here https://deki90to.pythonanywhere.com/"
                send_mail(
                    subject,
                    message,
                    email,
                    [f.album_owner.email, 'deki90to@gmail.com']
                )
                return redirect('display_all_images_from_single_album', f.pk)



@login_required(login_url='login')
def display_all_images_from_single_album(request, pk):
    # global album_details used in commented_album
    global album_details
    album_details = Album.objects.get(pk=pk)

    album_likes = album_details.likes.all()
    album_images = album_details.images_set.all()

    return render(request, 'baseApp/parts/display_all_images_from_single_album.html', {
        'album_details': album_details,
        'album_images': album_images,
        'album_likes': album_likes,
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
            f = comment_form.save(commit=False)
            f.comment_owner = request.user
            f.commented_album = album_details
            f.save()
            # messages.success(request, 'Comment created')
            # if f.comment_owner.email != f.commented_album.album_owner.email:
            email = f.comment_owner.email
            subject = 'New comment'
            message = f"{f.comment_owner.username} ({f.comment_owner.email}) commented your album: \n \
                {f.commented_album.album_name} > '{f.comment}' \n\n See here https://deki90to.pythonanywhere.com/"

            #notif album owner about comments that are not his
            if f.comment_owner.email != f.commented_album.album_owner.email:
                send_mail(
                    subject,
                    message,
                    email,
                    [f.commented_album.album_owner.email]
                )
            #notif admin about persons who comment own albums and it's not me
            if f.comment_owner.email == f.commented_album.album_owner.email and f.comment_owner.email != 'deki90to@gmail.com':
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



def album_slideshow(request, pk):
    album_details = Album.objects.get(pk=pk)
    album_images = album_details.images_set.all()
    return render(request, 'baseApp/parts/album_slideshow.html', {
        'album_details': album_details,
        'album_images': album_images,
    })

@login_required(login_url='login')
def addLike(request, pk):
    album = Album.objects.get(pk=pk)

    isDislike = False
    for dislike in album.dislikes.all():
        if dislike == request.user:
            isDislike = True
            break
    if isDislike:
        album.dislikes.remove(request.user)
    isLike = False
    for like in album.likes.all():
        if like == request.user:
            isLike = True
    if not isLike:
        album.likes.add(request.user)
        messages.success(request, f'{album.album_name} liked')
    if isLike:
        album.likes.remove(request.user)
        messages.success(request, f'{album.album_name} unliked')
    return redirect('home')


@login_required(login_url='login')
def addDislike(request, pk):
    album = Album.objects.get(pk=pk)
    
    isLike = False
    for like in album.likes.all():
        if like == request.user:
            isLike = True
            break
    if isLike:
        album.likes.remove(request.user)
    isDislike = False
    for dislike in album.dislikes.all():
        if dislike == request.user:
            isDislike = True
            break
    if not isDislike:
        album.dislikes.add(request.user)
        messages.success(request, f'{album.album_name} disliked')
    if isDislike:
        album.dislikes.remove(request.user)
        messages.success(request, f'{album.album_name} undisliked')
    return redirect('home')


def display_all_likes(request, pk):
    album_details = Album.objects.get(pk=pk)
    album_likes = album_details.likes.all()
    return render(request, 'baseApp/parts/display_all_likes.html', {
        'album_likes': album_likes,
    })

def display_all_dislikes(request, pk):
    album_details = Album.objects.get(pk=pk)
    album_dislikes = album_details.dislikes.all()
    return render(request, 'baseApp/parts/display_all_dislikes.html', {
        'album_dislikes': album_dislikes
    })


def profile(request, pk):
    profile = Profile.objects.get(user_id=pk)

    if request.method == 'POST':
        user_profile = request.user.profile
        action = request.POST['follow']
        
        if action == 'unfollow':
            user_profile.follows.remove(profile)
        elif action == 'follow':
            user_profile.follows.add(profile)
        user_profile.save()

    return render(request, 'baseApp/parts/profile.html', {
        'profile': profile
    })



def display_user_profile(request, pk):
    profile = Profile.objects.get(user_id=pk)
    profile_album = profile.user.album_set.all()
    return render(request, 'baseApp/parts/display_user_profile.html', {
        'profile': profile,
        'profile_album': profile_album
    })


def like_album(request, pk):
    album = Album.objects.get(pk=pk)
    if request.user in album.likes.all():
        album.likes.remove(request.user)
    else:
        album.likes.add(request.user)
    return redirect('display_all_images_from_single_album', album.pk)