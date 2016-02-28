from django.shortcuts import render,get_object_or_404
from main.models import Post,User
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
import random
import hashlib
import sys

# Create your views here.

def index(request):
	print >>sys.stderr,"WHAT THE FUCK"
	u = checkCookies(request)
	if u == False:
		return login(request)
	else:
		print >>sys.stderr,"SUBMIT POST"
		context = {'user' : u}
		return render(request,'main/submitpost.html',context)

def signup(request):
	if request.POST.has_key('login'):
		new_user = User()
		new_user.setName(request.POST['login'])
		new_user.save()
		response = HttpResponseRedirect(reverse('main:randompost'))
		response.set_cookie('login',request.POST['login'])
		return response

def login(request):
	if request.POST.has_key('login'):
		hash_name = hashlib.sha512(request.POST['login']).hexdigest()
		for u in User.objects.all():
			if u.hash_name == hash_name:
				response = HttpResponseRedirect(reverse('main:index'))
				response.set_cookie('login',request.POST['login'])
				return response
		else:
			return signup(request)
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

def submitpost(request):
	u = checkCookies(request)
	print >>sys.stderr,'FUCKING HELL {}'.format(u)
	if u != False:
		if request.POST.has_key('content'):
			post = Post(author=u)
			post.setContent(request.POST['content'])
			# post.author = u
			post.save()
			return randompost(request)

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
