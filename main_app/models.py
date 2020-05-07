from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

class Poem(models.Model):
  title = models.CharField(max_length=100)
  author = models.CharField(max_length=100)
  poem = models.TextField(max_length=10000)
#   genre = models.Field(dont know the model for genre)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  # date = models.DateField('Posted Date')

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('detail', kwargs={'poem_id': self.id})  

class Meta:
  ordering = ['-date']

class Comment(models.Model):
  # poem = models.TextField(max_length=200)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  poem = models.ForeignKey(Poem, on_delete=models.CASCADE)
  text = models.TextField(max_length=10000)

  def __str__(self):
    return self.text

  def get_absolute_url(self):
    return reverse('detail', kwargs={'poem_id': self.id}) 

class Photo(models.Model):
  url = models.CharField(max_length=200)
  poem = models.ForeignKey(Poem, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for poem_id: {self.poem_id} @{self.url}"

