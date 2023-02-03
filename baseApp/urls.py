from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('one_season_albums_display/<pk>/', views.one_season_albums_display, name='one_season_albums_display'),
    path('one_year_album_display/<pk>/', views.one_year_album_display, name='one_year_album_display'),

    path('create_new_album_form_display/', views.create_new_album_form_display, name='create_new_album_form_display'),
    path('create_new_album/', views.create_new_album, name='create_new_album'),
    
    path('display_all_images_from_single_album/<pk>/', views.display_all_images_from_single_album, name='display_all_images_from_single_album'),
    
    path('comment_form_display/', views.comment_form_display, name='comment_form_display'),
    path('create_comment/', views.create_comment, name='create_comment'),
    
    path('display_my_albums/<pk>/', views.display_my_albums, name='display_my_albums'),
    path('albums_search/', views.albums_search, name='albums_search'),
    path('delete_album/<pk>/', views.delete_album, name='delete_album'),
    path('delete_album_comment/<pk>/', views.delete_album_comment, name='delete_album_comment'),
    path('display_participants/', views.display_participants, name='display_participants'),
    path('album_slideshow/<pk>/', views.album_slideshow, name='album_slideshow'),

    path('like/<pk>/', views.addLike, name='like'),
    path('dislike/<pk>/', views.addDislike, name='dislike'),
    path('display_all_likes/<pk>/', views.display_all_likes, name='display_all_likes'),
    path('display_all_dislikes/<pk>/', views.display_all_dislikes, name='display_all_dislikes'),

    path('profile/<pk>/', views.profile, name='profile'),

    path('display_user_profile/<pk>/', views.display_user_profile, name='display_user_profile'),

    path('album/<int:pk>/like/', views.like_album, name='like_album'),
         
]