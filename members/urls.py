from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('login/', views.login_, name='login'),
    path('logout/', views.logout_, name='logout'),
    path('register/', views.register_, name='register'),

    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='reset_password.html'), name='reset_password'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='reset_password_done.html'), name='reset_password_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='reset_password_confirm.html'), name='reset_password_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='reset_password_complete.html'), name='reset_password_complete'),

    path('contact-me/', views.contact_me, name='contact_me'),
]
