from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from credentials.forms import CredentialForm

from annoying.decorators import render_to, ajax_request
from annoying.functions import get_object_or_None

@render_to('main/home.html')
def home(request):
    
    return locals()

@render_to('main/about.html')
def about(request):
    
    return locals()


@render_to('main/add_cred.html')
def add_cred(request):
    
    
    if request.POST:
        form = CredentialForm(request.POST)
        if form.is_valid():
            new_cred = form.save()
            #new_cred = form.save(commit=False)
            #new_cred.credential_notes = "Temporary Note for testing..."
            #new_cred.save()
            #form.save_m2m()
            
            
    else:
        form = CredentialForm()
    
    return locals()