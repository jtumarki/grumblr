from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class Grumbl(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
	return self.text

#class representing user profile info. Will contain photo in future
class UserInfo(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=50)
	blurb = models.CharField(max_length=200)
	about_me = models.CharField(max_length=500)
	school = models.CharField(max_length=200)
	contact = models.CharField(max_length=200)