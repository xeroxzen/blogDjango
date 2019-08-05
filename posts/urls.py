from django.conf.urls import url 
from . import views
from django.urls import path
#from .views import HomePageView


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.index, name='index'),
    url(r'^article/(?P<slug>[-_\w]+)/$', views.details, name='article'),
    url(r'^article/(?P<id>[-_\d]+)/$', views.details, name='article'),    
    path('<slug:slug>, <int:id>', views.details, name='article'),     
] 