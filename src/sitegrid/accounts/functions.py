from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from shortcuts.utils import send_email

def sendInvite(request, user):
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain

    recipient = user.email
    subject = 'A-LIST INVITATION'
    template = 'emails/invitation.html'
    uid = urlsafe_base64_encode(force_bytes(user.id))
    send_email(recipient, subject, template, passed_obj=None, current_site=current_site, domain=site_name, site_name=domain, uid=uid, token=default_token_generator.make_token(user), user=user)