from django.core.urlresolvers import reverse
from django import template



register = template.Library()


@register.simple_tag
def url_or_blank(reverse_name=""):
    url=''
    try:
        url = reverse(reverse_name)
    except Exception, e:
        pass
    
    return url
    