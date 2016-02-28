from django.shortcuts import render,get_object_or_404
from main.models import Post,User
import random
import hashlib

# Create your views here.

def index(request):
	if not request.COOKIES.has_key('login'):
		return signup(request)
	else:
		for u in User.objects.all():
			hash_name = hashlib.sha512(request.COOKIES['login']).hexdigest()
			if u.hash_name == hash_name
				context = {'user' : u}
				return render(request,'main/index.html',context)
			else:
				return signup(request)

def signup(request):
	for u in User.objects.all():
			if u.hash_name == request.COOKIES['login']
				context = {'user' : u}

def randompost(request):
	posts = Post.objects.all()
	p = posts[random.randint(0,len(posts))]
	context = {'post':p}
	return render(request,'main/randompost.html',context)
