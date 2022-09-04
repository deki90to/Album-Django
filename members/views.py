from multiprocessing import AuthenticationError
from urllib import response
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from requests import Response
from . forms import RegistrationForm




def register_(request):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
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
            messages.success(request, 'Successfully logged in')
            return redirect('home')
        else:
            messages.success(request, 'No user with this account')
            return redirect('login')
    else:
        return render(request, 'login.html')
    




def logout_(request):
    logout(request)
    messages.error(request, 'Logged out')
    return redirect('login')
