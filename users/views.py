# users/views.py

from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import UserRegisterForm, UserProfileUpdateForm, UserUpdateForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import logout as auth_logout
from django.views.generic import ListView, DeleteView,DetailView,UpdateView, CreateView
from django.core.paginator import Paginator
from topics.models import Upvoter, UpvoterAnswer, Topic, Answer
from django.core.paginator import Paginator

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user_image = form.cleaned_data.get('profile_picture')
            if user_image:
                user.profile.profile_picture = user_image
                user.profile.save()
            

            # Authenticate and log in the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            messages.success(request, 'Account created')
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})



def loginUser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or Password')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form':form})


@login_required
def LogOut(request):
    auth_logout(request)
    return redirect('/')

def view_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    topics = Topic.objects.filter(topic_author = profile_user)
    
    
    books = profile_user.books_uploaded.all()
    saved_topics = profile_user.saved_topics.all()
    is_own_profile = request.user.is_authenticated and request.user == profile_user
    
    context = {
        'profile_user': profile_user,
        'topics':topics,
        'is_own_profile': is_own_profile,
        'saved_topics':saved_topics,
        'books':books
    }
    return render(request, 'users/view_profile.html', context)


@login_required
def update_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    if request.user == profile_user:
        user = request.user
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                
                return redirect(reverse('profile', kwargs={'username': request.user.username}))
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = UserProfileUpdateForm(instance=request.user.userprofile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user':user
    }

    return render(request, 'users/update_profile.html', context)



class UsersList(ListView):
    model = User
    ordering = ['username']
    
    paginate_by = 9
    template_name = 'users/users_list.html'
    

