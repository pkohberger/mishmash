from django.conf import settings
from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.models import User, AnonymousUser
from django.db import models

from shortcuts.utils import empty
from annoying.fields import AutoOneToOneField
from sorl.thumbnail.fields import ImageField

import datetime

import os

class User(AbstractUser):
    prefix = models.CharField(max_length=24, null=True, blank=True)
    middle_name = models.CharField(max_length=32, null=True, blank=True)
    suffix = models.CharField(max_length=24, null=True, blank=True)
    contact_phone = models.CharField(max_length=64, null=True, blank=True)
    contact_email = models.EmailField(max_length=190, null=True, blank=True)
    account_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name
    
    def __unicode__(self):
        return u"%s" % (self.get_full_name, )
    
    @property    
    def get_full_name(self):
        name = ''
        if not empty(self.prefix):
            name += "%s " % (self.prefix, )
        if not empty(self.first_name):
            name += "%s " % (self.first_name, )
        if not empty(self.middle_name):
            name += "%s " % self.middle_name
        if not empty(self.last_name):
            name += "%s " % (self.last_name, )
        if not empty(self.suffix):
            name += "%s" % self.suffix
        return name.strip()

'''
    To get the user model in other models:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    example ForeignKey:
    
    class Book(models.Model):
        author = models.ForeignKey(User)
'''        






