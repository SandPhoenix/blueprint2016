from django.shortcuts import render,get_object_or_404
from main.models import Post,User,Feed
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
		print >>sys.stderr,"FEED POSTS {}".format(u.feed_set.all()[0].post_set.all())
		return render(request,'main/submitpost.html',context)

def signup(request):
	if request.POST.has_key('login'):
		new_user = User()
		new_user.setName(request.POST['login'])
		feed = Feed()
		feed.parent = new_user
		new_user.save()
		feed.save()
		response = HttpResponseRedirect(reverse('main:index'))
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
		context = {}
		if len(posts) > 0:
			p = posts[random.randint(0,len(posts)-1)]
			context = {'post':p}
			print >>sys.stderr,"fuckfuckfuck {}".format(p)
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
			post.save()
			#for follower in u.is_followed.all():
			#	print >>sys.stderr, "ADDING POST TO FEED"
			#	follower.feed.post_set.add(post)
			return randompost(request)
		else:
			return error(request,"I don't even know")
	else:
		return error(request,"I don't even know")

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
