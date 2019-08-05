from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post
from django.core.paginator import Paginator
from django.views.generic import ListView
from .form import *


# Create your views here.
def index(request):
	posts = Post.objects.all()
	paginator = Paginator(posts, 5)
	page = request.GET.get('page')
	posts = paginator.get_page(page)

	context = {
		'title' : 'Latest Posts',
		'posts' : posts
	}

	return render(request, 'posts/index.html', context)


def about_page_view(request):
    return render(request, 'about.html')	


# def get_redirected(queryset_or_class, lookups, validators):
# 	"""
# 	Calls get_object_or_404 and conditionally builds redirect URL
# 	"""
# 	obj = get_object_or_404(queryset_or_class, **lookups)
# 	for key, value in validators.items():
# 		if value != getattr(obj, key):
# 			return obj, obj.get_absolute_url()
# 	return obj, None				

def details(request, slug):
	post = get_object_or_404(Post, slug = slug)
	comments = post.comments.filter(active=True, parent__isnull=True)
	if request.method == 'post':
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():	
			Parent_obj = None
			try:
				Parent_id = int(request.POST.get('Parent_id'))
			except:
				Parent_id = None
			if Parent_id:
					Parent_obj = Comment.objects.get(id=Parent_id)
					if Parent_obj:
						reply_comment = comment_form.save(commit=False)
						reply_comment.Parent = Parent_obj
			new_comment = comment_form.save(commit=False)
			new_comment.Post = post
			new_comment.save()

			return redirect('posts/details.html', slug)
	else:
		comment_form = CommentForm()
	
	context = {
		'post' : post,
		'comment' : comments,
		'comment_form': comment_form
	}

	return render(request, 'posts/details.html', context)	