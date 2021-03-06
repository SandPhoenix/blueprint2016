from django.db import models
import hashlib

# Create your models here.

class User(models.Model):
	hash_name = models.CharField(max_length=32)

	def setName(self,name):
		self.hash_name = hashlib.sha512(name).hexdigest()
		self.save()

	user_follows = models.ManyToManyField('self', related_name='follows', symmetrical=False)
	follows_user = models.ManyToManyField('self', related_name='is_followed', symmetrical=False)

	def follow(u):
		for post in u.post_set.all():
			self.feed_set.all()[0].post_set.add(post)

	def __unicode__(self):
		return self.hash_name

class Feed(models.Model):
	parent = models.ForeignKey(User)

class Post(models.Model):
	content = models.CharField(max_length=140)
	hash_content = models.CharField(max_length=32,default="none")
	author = models.ForeignKey(User)
	feed = models.ForeignKey(Feed,default=1)

	def setContent(self,text):
		self.content = text
		self.hash_content = hashlib.sha512(text).hexdigest()
		self.save()
	def __unicode__(self):
		return self.content



class Comment(models.Model):
	content = models.CharField(max_length=140)
	author = models.ForeignKey(User)
	parent = models.ForeignKey(Post)
	def __unicode__(self):
		return self.content
