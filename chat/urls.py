# from django.urls import path
# from . import views

# urlpatterns = [
#     path("", views.chatPage, name="chat-page"),
#     path('', views.chat_home, name='chat_home'),
#     path('<str:room>/', views.room, name='room'),
#     path('checkview', views.checkview, name='checkview'),
#     path('send', views.send, name='send'),
#     path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.chat_page, name="chat-page"),
    path('chat_messages/', views.chat_messages, name='chat_messages'),
    path('new_chat_messsage/', views.new_chat_message, name='new_chat_message'),
    path('chat_section', views.chat_section, name='chat_section'),
    path('delete_message/<pk>/', views.delete_message, name='delete_message'),
]