from django.db import models

from django.contrib.auth.models import User # I am using this
from django.contrib.auth import get_user_model #try this or Use User
from django.utils import timezone
from django.urls import reverse,reverse_lazy

from taggit.managers import TaggableManager # Third party app

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status="published")

class PublishAuthor(models.Manager):
    def get_queryset(self):
        return  super(PublishAuthor,self).get_queryset().filter(status="draft")

class Post(models.Model):
    status_choices = (("draft","Draft"),("published","Published"))

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=250,unique_for_date='publish')

    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="blog_posts")

    body = models.TextField()

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=10,choices=status_choices,default="published")

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Custom manager
    tags = TaggableManager()

    class Meta:
        ordering = ("-publish",)

    def __str__ (self):
        return self.title

    def get_absolute_url (self):
        return reverse("blog:post_detail",args=[str(self.id)])

class Comment (models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')

    name = models.CharField(max_length=200)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) # this is used at sitemps.py to get posts which are updated may be i think like this way
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created"]

    def __str__ (self):
        return "Comment by {} on {}".format(self.name,self.post)
