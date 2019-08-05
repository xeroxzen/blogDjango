from django.db import models
from django.urls import reverse
from datetime import datetime
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django_comments.moderation import CommentModerator
from django_comments_xtd.moderation import moderator
#from django.conf import settings
#from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):

    STATUS_CHOICES = (
        ('published', 'Published'),
        ('draft', 'Draft')
    )
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    author_twitter_account = models.CharField(max_length=255, default='', blank=True, null=True)
    sub_title = models.CharField(max_length=255, default='', blank=True, null=True)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete= models.PROTECT)
    tag = models.ForeignKey('Tag', null=True, blank=True, on_delete=models.PROTECT)
    cover = models.ImageField(upload_to='images/', null=True, height_field=None, width_field=None, max_length=None)
    cover_credits = models.CharField(max_length=255, blank=True, null=True, default='')
    seo_title = models.CharField(max_length=255, default=None)
    seo_description = models.CharField(max_length=255, default=None)
    body = RichTextUploadingField(blank=True, null=True, default='')
    allow_comments = models.BooleanField('allow_comments', default=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    published = models.DateTimeField(default=datetime.now)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='')
    slug = models.SlugField(default= '', blank=True, unique=True, max_length=255)

    def save(self):
        self.slug = slugify(self.title)
        super(Post, self).save()

    def __str__(self):
        return "{0}".format(self.title)

    def get_absolute_url(self):
        return reverse('article', kwargs={'slug': self.slug, 'id': self.id})
     
    class Meta:
        verbose_name_plural = "Posts"
        ordering = ("-created_at",)    

    
    def get_cat_list(self):
        k = self.category
        breadcrumb = ['dummy']
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent

        for i in range(len(breadcrumb) -1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i:-1])
        return breadcrumb[-1:0:-1] 

    def get_tag_list(self):
        i = self.tags
        breadcrumb = ['genius']
        while i is not None:
            breadcrumb.append(i.slug)
            i = i.parent

        for x in range(len(breadcrumb) -1):
            breadcrumb[i] = '/' .join(breadcrumb[-1:i:-1])
        return breadcrumb[-1:0:-1]                  

#Category class for the categories that are linked to posts
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, default=None, max_length=255)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete = models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        #__str__ method elaborated later in
        full_path = [self.name]
        #post use __unicode__ in place of
        k = self.parent

        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return '->' .join(full_path[::-1])

    class Meta:
        #ordering = ("-created_at",)
    	verbose_name_plural = "Categories"

#Tags posts that are to be linked to posts
class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, default=None, max_length=255)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete = models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now, blank=True)


    def __str__(self):
        full_path = [self.name]
        i = self.parent

        while i is not None:
            full_path.append(i.name)
            i = i.parent

        return '->' .join(full_path[::-1])


    class Meta:
        verbose_name_plural = 'Tags'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return "Comment By {0}" .format(self.name)           


class PostCommentModerator(CommentModerator):
    email_notification = True
    auto_moderate_field = 'publish'
    moderate_after = 365

moderator.register(Post, PostCommentModerator)              
