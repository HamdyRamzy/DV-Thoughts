from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .forms import SignUp
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import UpdateView
# Create your views here.


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = SignUp()
        if request.method == 'POST':
            form = SignUp(request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                return redirect('home')

        return render(request, 'signup.html', {'form':form})        


        



