from django.shortcuts import render,get_object_or_404
from main.models import Post,User
from django.http import HttpResponse,HttpResponseRedirect
import random
import hashlib

# Create your views here.

def index(request):
	u = checkCookies(request)
	if u == False:
		return login(request)
	else:
		context = {'user' : u}
		return render(request,'main/index.html',context)

def signup(request):
	if request.POST.has_key('login'):
		new_user = User()
		new_user.setName(request.POST['login'])
		new_user.save()
		return randompost(request)

def login(request):
	if request.POST.has_key('login'):
		hash_name = hashlib.sha512(request.POST['login']).hexdigest()
		for u in User.objects.all():
			if u.hash_name == hash_name:
				response = HttpResponseRedirect(reverse('blog:index'))
				response.set_cookie('login',request.POST['login'])
				return render(request,'main/index.html',{})
		else:
			return render(request,'main/index.html',{})
	else:
		return render(request,'main/index.html',{})

def randompost(request):
	if checkCookies(request) != False:
		posts = Post.objects.all()
		p = posts[random.randint(0,len(posts))]
		context = {'post':p}
		return render(request,'main/randompost.html',context)
	else:
		return error(request,"Not Authorized")

# def submitpost(request):
# 	u = checkCookies(request)
# 	if u != False:



def error(request,string):
	context = {'string' : string }
	return render(request,'main/error.html',context)

def checkCookies(request):
	if request.COOKIES.has_key('login'):
		hash_name = hashlib.sha512(request.COOKIES['login']).hexdigest()
		for u in User.objects.all():
			if u.hash_name == hash_name:
				return u
		else:
			return False
	else:
		return False
