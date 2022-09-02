from django.urls import path
from . import views



urlpatterns = [

    path('', views.home, name='home'),

    path('display_my_albums/', views.display_my_albums, name='display_my_albums'),
    path('one_season_albums_display/<pk>/', views.one_season_albums_display, name='one_season_albums_display'),
    path('one_year_album_display/<pk>/', views.one_year_album_display, name='one_year_album_display'),

    path('create_new_album_form_display/', views.create_new_album_form_display, name='create_new_album_form_display'),
    path('create_new_album/', views.create_new_album, name='create_new_album'),

    path('display_all_images_from_single_album/<pk>/', views.display_all_images_from_single_album, name='display_all_images_from_single_album'),
    
    path('comment_form_display/', views.comment_form_display, name='comment_form_display'),
    path('create_comment/', views.create_comment, name='create_comment'),


    path('albums_search/', views.albums_search, name='albums_search'),

]