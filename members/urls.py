from django.urls import path
from . import views 
from django.contrib.auth import views as authViews


urlpatterns = [
    path('login/', views.login_, name='login'),
    path('logout/', views.logout_, name='logout'),
    path('register/', views.register_, name='register'),

]