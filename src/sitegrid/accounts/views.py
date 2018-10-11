from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.shortcuts import get_object_or_404, render_to_response, redirect

from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from shortcuts.utils import send_email
from forms import *
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

from logs.models import Error

from annoying.functions import get_object_or_None
from annoying.decorators import render_to, ajax_request

import json as simplejson
from django.template.loader import render_to_string
from accounts.functions import *


def user_logout(request):
    logout(request)
    request.session['selected_event_id'] = 0
    request.session.save()
    return redirect('home')
    
@render_to('accounts/login.html')
def user_login(request):
    request.session['selected_event_id'] = 0
    request.session.save()

    if request.user.id:
        return redirect('alist_events')
    else:
        login_form = LoginForm()
        if request.method == 'POST':
            username = None
            temp = get_object_or_None(User, email=request.POST['email'])
            if temp is not None:
                username = temp.username
            user = authenticate(username=username, password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    profile = UserProfile.objects.get(user_id=user.id)
                    request.session['logo'] = str(profile.client.logo)
                    request.session.save()
                    return redirect('alist_events') # Will probably redirect to different pages based on permisson
                else:
                    error = 'Your account is not active'
            else:
                error = 'Email or Password is incorrect!'

        return locals()

@render_to('accounts/create_account.html')
def createAccount(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            register_form = RegisterForm()
    else:
        register_form = RegisterForm()

    return locals()

@login_required
@ajax_request
def inviteUser(request):
    userprofiles = None
    owner = False
    client_id = request.user.user_profile.client_id

    if 'account_owner' in request.session['permissions']:
        owner = True

    invite_user_form = InviteUserForm(request.POST)
    if invite_user_form.is_valid():
        user = invite_user_form.save(client_id)
        invite_user_form = InviteUserForm()
        sendInvite(request, user)
        userprofiles = UserProfile.objects.filter(client_id=client_id)
        html = render_to_string( 'alist/admins.html', { 'userprofiles': userprofiles } )
        return_dict = {'html': html, 'success' : 'SUCCESS: An email has been sent to the invited user!'}
    else:
        error_list = []
        for field in invite_user_form:
            if field.errors:
                for error in field.errors:
                    error_list.append({'field': field.name, 'error': error})
        return_dict = {'error_list': error_list, 'error': 'ERROR!'}

    return return_dict


def sendInvite(request, user):
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain

    recipient = user.email
    subject = 'A-LIST INVITATION'
    template = 'emails/invitation.html'
    uid = urlsafe_base64_encode(force_bytes(user.id))
    send_email(recipient, subject, template, passed_obj=None, current_site=current_site, domain=site_name, site_name=domain, uid=uid, token=default_token_generator.make_token(user), user=user)


def activateAccount(request, uidb64, token):
    user_id = urlsafe_base64_decode(uidb64)
    uidb64 = uidb64.encode('utf-8')
    token = token.encode('utf-8')
    
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()

    url = reverse('password_reset_confirm', kwargs={'uidb64':uidb64, 'token':token})
    return HttpResponseRedirect(url)

@render_to('accounts/login.html')
def forgotPassword(request):
    login_form = LoginForm()
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain

    recipient = request.POST.get('email')
    user = get_object_or_None(User, email=recipient)
    if user is not None:
        subject = 'A-LIST INVITATION'
        template = 'emails/invitation.html'
        uid = urlsafe_base64_encode(force_bytes(user.id))
        send_email(recipient, subject, template, passed_obj=None, current_site=current_site, domain=site_name, site_name=domain, uid=uid, token=default_token_generator.make_token(user), user=user)
    else:
        error = 'Email does not match any account'

    return locals()


@login_required
@render_to('accounts/account_info.html')
def accountInfo(request):

    client_profile = get_object_or_None(ClientProfile, user=request.user)
    
    return locals()


@login_required
def uploadLogo(request):

    if request.method == 'POST':
        client_id = request.user.user_profile.client_id
        logo = request.FILES.get('logo', None)

        if logo:
            client = ClientProfile.objects.get(id=client_id)
            client.logo = logo
            client.save()
            request.session['logo'] = str(client.logo)
            request.session.save()

    url = reverse('accounts_account_info')
    return HttpResponseRedirect(url)








