from urllib import response
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from requests import Response
from . forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse


def register_(request):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)

            email = email
            subject = 'New registration'
            message = f'{email} successfully registred, you password is "{raw_password}", Welcome!'
            send_mail(
                subject,
                message,
                email,
                [email, 'deki90to@gmail.com']
            )
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {
        'registration_form': form,
    })



def login_(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        
        if user is not None:
            login(request, user)
            email = email
            subject = 'User logged in'
            message = f'{user.username} {email} logged in'
            if email != 'deki90to@gmail.com':
                send_mail(
                    subject,
                    message,
                    email,
                    ['deki90to@gmail.com']
                )
                # messages.success(request, 'Successfully logged in')
            return redirect('home')
        else:
            # messages.success(request, 'No user with this account')
            return redirect('login')
    else:
        return render(request, 'login.html')
    


def logout_(request):
    logout(request)
    # messages.error(request, 'Logged out')
    return redirect('login')



def resetPassword(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            email = request.POST['email']
            user = authenticate(email=email)
            login(request, user)
            # messages.success(request, 'Password Sent')
            return redirect('home')
    else:
        form = UserCreationForm()
        
    context = {'form': form}
    return render(request, 'reset_password.html', context)



def resetPasswordConfirm(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            user = authenticate(password1=password1, password2=password2)
            login(request, user)
            # messages.success(request, 'Password Saved')
            return redirect('home')
    else:
        form = UserCreationForm()
        
    context = {'form': form}
    return render(request, 'reset_password_confirm.html', context)



def contact_me(request):
    if request.method == 'POST':
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        send_mail(
            subject,
            message,
            email,
            ['deki90to@gmail.com']
        )
        messages.success(request, 'Message sent')
        return render(request, 'contact_me.html', {'email': email, 'message': message})
    else:
        return render(request, 'contact_me.html')