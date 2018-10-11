from django.conf.urls import *

import views
import ajax_calls


urlpatterns = patterns('',

    # Views
    url(r'^logout/$', views.user_logout, name='accounts_logout'),
    
    url(r'^login/$', views.user_login, name='accounts_login'),

    url(r'^forgot/$', views.forgotPassword, name='accounts_forgot'),

    url(r'^create-account/$', views.createAccount, name='accounts_create_account'),

    url(r'^invite-user/$', views.inviteUser, name='accounts_invite_user'),

    url(r'^account-info/$', views.accountInfo, name='accounts_account_info'),

    url(r'^upload-logo/$', views.uploadLogo, name='accounts_upload_logo'),

    # DJANGO REST PASSWORD URLS
    url(r'^activate/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/', views.activateAccount, name='accounts_activate'),
    url(r'^reset/password_reset/$', 'django.contrib.auth.views.password_reset', name="django_account_password_reset1"),
    url(r'^reset/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name="password_reset_done"),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'accounts/password_reset.html'}, name="password_reset_confirm"),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'accounts/password_reset_done.html'}, name="password_reset_complete"),
    # DJANGO REST PASSWORD URLS

    # AJAX CALLS
    #url(r'^edit-client-info/$', ajax_calls.editClientInfo, name='accounts_edit_client_info'),
    url(r'^edit-profile-info/$', ajax_calls.editProfileInfo, name='accounts_edit_profile_info'),
    url(r'^edit-user-info/$', ajax_calls.editUserInfo, name='accounts_edit_user_info'),
    url(r'^change-user-pass/$', ajax_calls.changePassword, name='accounts_change_password'),

)