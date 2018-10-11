from django import template


register = template.Library()



@register.simple_tag
def intdivide(value, arg=''): 
  if int(arg) != 0:
      return int(value) // int(arg)
  else:
      return 0
  
@register.simple_tag
def intmodulo(value, arg): 
  if int(arg) != 0:
      return int(value) % int(arg)
  else:
      return 0

@register.simple_tag
def intmultiply(value, arg=''): 
  if int(arg) != 0:
      return int(value) * int(arg)
  else:
      return 0


@register.simple_tag
def get_general_setting(setting=None):
    retval = get_general_settings(setting)
    if retval is None:
        retval = ''
    return retval

