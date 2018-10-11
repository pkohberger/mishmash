from django.http import Http404
from django.utils.deprecation import MiddlewareMixin
from django.utils.encoding import smart_text


from logs.models import Error

import traceback
import warnings
import datetime
import socket

WRITE_404 = False

class ErrorLogMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if not WRITE_404 and isinstance(exception, Http404):
            return
        
        error_class = exception.__class__.__name__
        server = socket.gethostname()
        error_trace = traceback.format_exc()
        defaults = {
            "error_class": error_class,
            "server": server,
            "error_trace": error_trace,
            "location": request.build_absolute_uri(),
            "message": smart_text(exception),
            }
        
        try:
            Error.objects.create(**defaults)
        
        except Exception as e:
            warnings.warn(smart_text(e))
            
            
            