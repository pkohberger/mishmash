from django.db import models
from django.utils import timezone

import datetime
import socket
import inspect
try:
    import json
except:
    from django.utils import simplejson as json



class ErrorManager(models.Manager):
    def error_save(self, request, message=None, error_class="Unspecified Error", error_trace=None):
        caller, line = inspect.stack() [1][1:3]
        data = "at line %s in %s. " % (line, caller)
        if message is None:
            message = data
        else:
            message += " %s" % data
            
        if error_trace is None:
            error_trace = request
        else:
            error_trace = "%s - %s" % (error_trace, request)
            
        kwargs = {
            "location": request.build_absolute_uri(),
            "server": socket.gethostname(),
            "message": message,
            "error_class": error_class,
            "error_trace": error_trace,
            }
            
        return self.create(**kwargs)
        
        

class Error(models.Model):
    
    error_class = models.CharField(max_length=128)
    thrown_on = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=190, null=True, blank=True)
    server = models.CharField(max_length=190, null=True, blank=True)
    error_trace = models.TextField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    
    objects = ErrorManager()
    
    

class MasterLog(models.Model):
    entry_type = models.CharField(max_length=128)
    message = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=190, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    
    
            
            