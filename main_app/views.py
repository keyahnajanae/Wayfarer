from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, City, Post
from .forms import Post_Form, Profile_Form

# Create your views here


#  Home view

def home(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request, 'home.html', context)

# Index & Create View 

def post_index(request):
    if request.method == 'POST':
        post_form = Post_Form(request.POST)
        if post_form.is_valid():
            post_form.save()
            return redirect('post_index')
    posts = Post.objects.all()
    post_form = Post_Form()
    context = {'posts':posts, 'post_form': post_form}
    return render(request, 'posts/index.html', context)

# Show Post View 

def post_details(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'posts/detail.html', {'post': post}) 

# Post Delete
def post_delete(request, post_id):
    post = Post.objects.get(id=post_id).delete()
    return redirect('post_index')

# Post Edit
def post_edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        post_form = Post_Form(request.POST, instance = post)
        if post_form.is_valid(): 
            post_form.save()
            return redirect('detail', post_id = post_id)
    else:
        post_form = Post_Form(instance = post)
        context = {'post':post, 'post_form':post_form}
        return render(request, 'posts/edit.html', context)

# Create your views here.

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.create(user)
            login(request, user)
            return redirect('profile_edit')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {
        'form': form,
        'error_message': error_message
    }
    return render(request, 'registration/signup.html', context)


def profile_details(request):
    profile = Profile.objects.get(user=request.user.id)
    context = {
        'profile': profile
    }
    return render(request, 'registration/detail.html', context)

def profile_edit(request):
    profile = Profile.objects.get(user=request.user.id)
    if request.method == "POST":
        #handle profile update
        profile_form = Profile_Form(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile_detail')
    else:
        #handle profile edit
        profile_form = Profile_Form(instance=profile)
        context = {
            'profile': profile,
            'form': profile_form
        }
        return render(request, 'registration/profile.html', context)

def profile_delete(request):
    pass