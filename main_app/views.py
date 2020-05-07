from django.shortcuts import render, redirect
from django.db import models
from .models import Poem, Photo
from .forms import CommentForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'poe-app'

# Create your views here.
# from django.http import HttpResponse

# Define the home view
# def home(request):
#   return HttpResponse('<h1>home page</h1>')

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def poems_index(request):
  poems = Poem.objects.filter(user=request.user)
  
  return render(request, 'poems/index.html', { 'poems': poems })

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('/')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

@login_required
# class PoeDetail(LoginRequiredMixin, DetailView):
#   model = Poem
def poems_detail(request, poem_id):
  poem = Poem.objects.get(id=poem_id)
  comment_form = CommentForm()
  return render(request, 'poems/detail.html', { 'poem': poem, 'comment_form': comment_form })

# @login_required
# def add_comment(request, poem_id):
#   form = CommentForm(request.POST)
#   if form.is_valid():
#     form.instance.user = request.user
#     new_comment = form.save(commit=False)
#     new_comment.poem_id = poem_id
#     new_comment.save() 
#   # return redirect(poem_id=poem_id)
#   return redirect('/poems', poem_id=poem_id)
@login_required
def add_comment(request, poem_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    form.instance.user = request.user
    new_comment = form.save(commit=False)
    new_comment.poem_id = poem_id
    new_comment.save()
  return redirect('detail', poem_id=poem_id)


class PoeCreate(LoginRequiredMixin, CreateView):
  model = Poem
  fields = ['title', 'poem']   #make author value default to the user that made the post
  success_url = '/poems/'
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class PoeUpdate(LoginRequiredMixin, UpdateView):
  model = Poem
  fields = ['title', 'poem']
  

class PoeDelete(LoginRequiredMixin, DeleteView):
  model = Poem
  success_url = '/poems/'  

def genres(request):
  return render(request, 'genres.html')  


def add_photo(request, poem_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, poem_id=poem_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', poem_id=poem_id)
