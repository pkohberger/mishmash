#  HTTP
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

# JSON
import json
from django.template.loader import render_to_string

# UTILS
from annoying.functions import get_object_or_None

# FUNCTIONS
from accounts.functions import *

# BACKEND
from accounts.models import *
from forms import *
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate

########## ACCOUNT CALLS START ##########


def editProfileInfo(request):
    response_data = {}
    user_id = request.user.id

    edit_profile_info_form = EditProfileInfoForm(request.POST)
    if edit_profile_info_form.is_valid():
        edit_profile_info_form.save(user_id=user_id)

        response_data['success'] = 'edited profile'
    else:
        response_data['error'] = 'form errors'
        response_data['form_errors'] = []
        for field in edit_profile_info_form:
            if field.errors:
                for error in field.errors:
                    response_data['form_errors'].append({'id': 'id_' + field.name, 'error': error})

    edit_profile_info_form = EditProfileInfoForm()

    user_profile   = UserProfile.objects.get(user_id=user_id)

    profile_info_html = render_to_string( 'accounts/ajax_html/profile_info.html', {
        'edit_profile_info_form': edit_profile_info_form, 
        'user_profile': user_profile
    })

    response_data['profile_info_html'] = profile_info_html

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def editUserInfo(request):
    response_data = {}
    user_id = request.user.id

    edit_user_info_form = EditUserForm(request.POST)

    if edit_user_info_form.is_valid(user_id, request.POST.get('username')):
        edit_user_info_form.save(user_id=user_id)

        response_data['success'] = 'edited user'
    else:
        response_data['error'] = 'form errors'
        response_data['form_errors'] = []
        for field in edit_user_info_form:
            if field.errors:
                for error in field.errors:
                    response_data['form_errors'].append({'id': 'id_' + field.name, 'error': error})

    edit_user_info_form = EditUserForm()

    user_profile   = UserProfile.objects.get(user_id=user_id)

    user_info_html = render_to_string( 'accounts/ajax_html/user_info.html', {
        'edit_user_info_form': edit_user_info_form, 
        'user_profile': user_profile
    })

    response_data['user_info_html'] = user_info_html

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def changePassword(request):
    print request.POST
    response_data = {}
    user_id = request.user.id

    change_pass_form = ChangePasswordForm(request.POST)

    if change_pass_form.is_valid():
        change_pass_form.save(user_id=user_id)

        # MUST LOGIN WITH NEW PASS
        user = authenticate(username=request.user.username, password=request.POST['password'])
        auth_login(request, user)

        response_data['success'] = 'changed password'
    else:
        response_data['error'] = 'form errors'
        response_data['form_errors'] = []
        for field in change_pass_form:
            if field.errors:
                for error in field.errors:
                    response_data['form_errors'].append({'id': 'id_' + field.name, 'error': error})

    change_pass_form = ChangePasswordForm()

    user_profile   = UserProfile.objects.get(user_id=user_id)

    pass_html = render_to_string( 'accounts/ajax_html/change_pass.html', {
        'change_pass_form': change_pass_form, 
        'user_profile': user_profile
    })

    response_data['pass_html'] = pass_html

    return HttpResponse(json.dumps(response_data), content_type="application/json")

########## ACCOUNT CALLS START ##########