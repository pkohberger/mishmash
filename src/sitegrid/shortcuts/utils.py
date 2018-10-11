from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.mail import send_mail, EmailMessage
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.encoding import smart_text
from django.utils.html import strip_tags


from logs.models import Error

import math
import traceback as traceback_mod

import re
import os
import sys

from decimal import *
import datetime
from dateutil import relativedelta, parser
import unicodedata
import string

from urllib.parse import unquote


VALID_DIR_NAME_CHARS = "-_()%s%s" % (string.ascii_letters, string.digits)


def pad(s, length, char="0"):
    if len(s) < length:
        pads = length - len(s)
        padding = char * pads
        return "%s%s" % (padding, s,)
    return s
    
    
def Value(s, numtype="int", precision=2):
    if numtype == 'int':
        try:
            if type(s) == settings.TYPE_INTEGER:
                return s
            return int(s.strip())
        except ValueError:
            return 0
    elif numtype == "dec":
        try:
            getcontext().prec = 28
            multiplier = "1.%s" % (pad("", precision, "0"), )
            return Decimal(s) * Decimal(multiplier)
        except ValueError:
            return Decimal("0.00")
    else:
        return 0  # for now


def value_or_None(s, numtype="int", precision=2):
    if numtype == 'int':
        try:
            if type(s) == settings.TYPE_INTEGER:
                return s
            return int(s.strip())
        except ValueError:
            return None
    elif numtype == "dec":
        try:
            getcontext().prec = 28
            dec_s = Decimal(s)
            new_prec = abs(dec_s.as_tuple().exponent)
            if new_prec < precision:
                multiplier = "1.%s" % (pad("", precision, "0"), )
                return Decimal(s) * Decimal(multiplier)
            elif new_prec < precision:
                return Decimal(long(dec_s * 100)) / Decimal(100)
            return dec_s
        except ValueError:
            return None
    return None  # for now


def float_to_int(s, method="round"):
    try:
        if method == "round":
            return int(round(float(s)))
        return int(math.floor(float(s)))
    except ValueError:
        return 0    
    
    
def empty(mystring):
    if mystring is not None:
        if type(mystring) == type("string") or type(mystring) == type(u"string"):
            if mystring.strip() != '':
                return False
        elif getattr(mystring, '__str__', None) and str(mystring).strip() != '':
            return False
    return True
    

def get_string_or_None(mystring, lowercase=False):
    if not empty(mystring):
        mystring = mystring.strip()
        if lowercase:
            mystring = mystring.lower()
        return mystring
    return None


def normalize(item, ret_type="string", default=None):
    if item is not None:
        if type(item) == settings.TYPE_STRING or type(item) == settings.TYPE_UNICODE:
            if item.strip() != '':
                item = item.strip()
            else: 
                item = None
        elif type(item) == settings.TYPE_INTEGER or type(item) == settings.TYPE_FLOAT or type(item) == type(Decimal('1.00')) or type(item) == settings.TYPE_BOOLEAN:
            item = str(item)


        if item is not None:
            if ret_type == 'string':
                return str(item)
            if ret_type == 'unicode':
                return unicode(item)
            if ret_type == 'int':
                if default is None:
                    return value_or_None(item)
                else:
                    ret_val = Value(item)
                    if str(ret_val) != item:
                        return default
                    else:
                        return ret_val
            if ret_type == 'dec' or ret_type == 'float':
                point = item.rfind('.')
                if point >= 0:
                    dec_part = item[point+1:len(item)]
                    prec = len(dec_part)
                else:
                    prec = 0

                if ret_type == 'dec':
                    ret_val = value_or_None(item, 'dec', prec)
                    if ret_val is not None:
                        return ret_val
                elif ret_type == 'float':
                    ret_val = float(item)
                    return ret_val
            if ret_type == 'bool':
                if item.lower() == 'true':
                    return True
                if item.lower() == 'false':
                    return False
                    
    
    return default


def smart_truncate(mystring='', endchars='...', cutoff=159):
    if mystring is None:
        mystring = ''
    retstring = mystring[:cutoff - 3]
    if len(mystring) != len(retstring):
        retstring += endchars
        
    return retstring

def check_create_dir(dirname, root_path):
    if dirname and dirname != '' and root_path and root_path != '':
        new_path = os.path.join(root_path, dirname)
        if not new_path.endswith(os.sep):
            new_path = "%s%s" % (new_path, os.sep)
        if os.path.exists(new_path) and os.path.isdir(new_path):
            return True
        elif os.path.isfile(new_path):
            # Dunno how this could be, but return false!
            return False
        elif not os.path.exists(new_path):
            try:
                os.makedirs(new_path)
                return True
            except OSError as e:
                print("Tried to make dir %s.  Failed with error: %s" % (new_path, str(e)))
                return False
                
        else:
            print("Tried to make dir %s.  Failed with unknown error!" % new_path)
            return False  # Something else is wrong, but who knows what?!


def safe_decode(s, encodings=('ascii', 'utf8', 'latin1', 'iso-8859-1', 'windows-1252', 'iso-8859-2')):
    for encoding in encodings:
    	try:
    		return s.decode(encoding)
    	except UnicodeDecodeError:
    		pass
    return s.decode('ascii', 'ignore')


def recode(s, initial_encoding='windows-1252', final_encoding='utf-8'):
    
    return s.decode(initial_encoding).encode(final_encoding)
    

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    Note - MUST be utf-8!
    """
    #value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)
    
    
def safe_decimal(mystring):
    try:
        retval = Decimal(mystring)
    except InvalidOperation as e:
        return 0
    return retval


def get_base_url(ssl=False):
    site = Site.objects.all()[:1][0]
    if ssl:
        url = "https://%s" % (site,)
    else:
        url = "http://%s" % (site,)
    return url


def get_current_url(request):
    current_url = get_base_url() + request.path_info
    return current_url


def send_email(recipient, subject, template, passed_obj=None, **kwargs):

    content_type = None
    attachments = []
    if kwargs.get('email_type'):
        content_type = kwargs['email_type']
    if kwargs.get('attachments'):
        attachments = kwargs['attachments']
    if isinstance(recipient, basestring):
        recipient = User(email=recipient)
    try:
        context = kwargs
        context.update(locals())
        message_text = render_to_string(template, context)
    except TemplateDoesNotExist:
        message_text = "Could not find a valid email template! %s" % (template, )
        recipient.email = settings.ADMINS[0][1]
    
    try:
        #send_mail(unicode(subject.encode('utf-8'), errors='ignore'), unicode(message_text.encode('utf-8'), errors='ignore'), settings.EMAIL_DEFAULT_ACCOUNT, [recipient.email])
        msg = EmailMessage(unicode(subject.encode('utf-8'), errors='replace'), unicode(message_text.encode('utf-8'), errors='replace'), settings.EMAIL_DEFAULT_ACCOUNT, [recipient.email,])
        msg.content_subtype = "html"
        if content_type:
            msg.content_subtype = content_type
        if attachments:
            for attachment in attachments:
                if len(attachment) == 2:
                    msg.attach(filename=attachment[0], content=attachment[1])
                elif len(attachment) == 3:
                    msg.attach(filename=attachment[0], content=attachment[1], mimetype=attachment[2])
                else:
                    pass #Ignore, because it is not formatted correctly
        msg.send()
    except Exception as e:
        if settings.DEBUG:
            print("Email sent!\nFrom: %s\nTo: %s\nmessage text: %s\n\n%s" % (settings.EMAIL_DEFAULT_ACCOUNT,
                                                                             recipient.email,
                                                                             unicode(subject.encode('utf-8'), errors='ignore'),
                                                                             unicode(message_text.encode('utf-8'), errors='ignore')))
            print(e)
        else:
            Error.objects.create(error_class=e.__class__.__name__,
                                 error_trace=traceback_mod.format_exc(),
                                 message="sender: %s\nrecipient: %s\n\n%s" % (settings.EMAIL_DEFAULT_ACCOUNT,
                                                                              recipient.email,
                                                                              smart_text(e),
                                                                             ),
                                 )
                                 

def parse_zipcode_string(zip_string=None):
    zipcode = None
    ziptest = re.compile('^\d{1,5}$')
    plus4test = re.compile('^\d{1,4}$')
    zipplus4 = None
    if zip_string and (zip_string.strip() != '' or zip_string.strip() != '-'):
        if len(zip_string) <= 5:
            zipmatch = ziptest.match(zip_string)
            if zipmatch:
                zipcode = zipmatch.string.zfill(5)
        else:
            ziplist = zip_string.split('-')
            if len(ziplist[0]) > 0 and len(ziplist[0]) <=5:
                zipmatch = ziptest.match(ziplist[0])
                if zipmatch:
                    zipcode = zipmatch.string.zfill(5)
                
                if len(ziplist) == 2 and len(ziplist[1]) > 0 and len(ziplist[1]) <= 4:
                    plus4match = plus4test.match(ziplist[1])
                    if plus4match:
                        zipplus4 = plus4match.string.zfill(4)


    return zipcode, zipplus4


def get_file_from_url(url_to_get=None):
    #import pdb
    #pdb.set_trace()
    if url_to_get is None or url_to_get.strip() == '' or not (url_to_get.startswith('http://') or url_to_get.startswith('https://')):
        return None
    response = requests.get(url_to_get, verify=False)

    img_temp = NamedTemporaryFile()
    img_temp.write(response.content)
    img_temp.flush()

    return img_temp



def removeDisallowedDirnameChars(dirname):
    cleanedDirname = unicodedata.normalize('NFKD', dirname).encode('ASCII', 'ignore')
    return ''.join(c for c in cleanedDirname if c in VALID_DIR_NAME_CHARS)


def get_admin_image_path(filename, subfolders=[]):
    extra_folders = ''
    if len(subfolders) > 0:
        for subfolder in subfolders:
            # test for valid name here
            if subfolder is None:
                extra_folders = ''
                break
            subfolder = unicode(subfolder)
            subfolder = subfolder.strip()
            if subfolder == '':
                extra_folders = ''
                break
            temp = removeDisallowedDirnameChars(subfolder)
            if temp == subfolder:
                extra_folders += "%s/" % (temp, )
            else:
                extra_folders = ''
                break
        
    return "%s%s%s" % (settings.PHOTOBUCKET_BASE_FOLDER, extra_folders, filename)


def admin_image_path(instance, filename, subfolders=[]):
    # file will be uploaded to MEDIA_ROOT/admin/media/<extra_folders_list>/<filename>
    file_path = get_admin_image_path(filename, subfolders)
    return file_path


def get_filepath_from_url(url=None):
    file_path = None
    if url is not None and url.strip() != '':
        url_route = url.split('/')
        url_segments = [unquote(x.strip()) for x in url_route if unquote(x.strip()) != '' and not x.strip().startswith("?")]
        if url_segments[0] == 'static':
            temp_path = os.path.join(settings.DIR_ROOT, *url_segments)
            temp_path2 = None
        else:
            temp_path = os.path.join(settings.STATIC_ROOT, *url_segments)
            temp_path2 = os.path.join(settings.MEDIA_ROOT, *url_segments)
            
        if os.path.isfile(temp_path) or (temp_path2 is not None and os.path.isfile(temp_path2)):
            if temp_path2 is not None and os.path.isfile(temp_path2) and not os.path.isfile(temp_path):
                temp_path = temp_path2
            if os.path.join(settings.MEDIA_ROOT, "") in temp_path:
                temp_path = temp_path.replace(os.path.join(settings.MEDIA_ROOT, ""), '')
            elif os.path.join(settings.STATIC_ROOT, "") in temp_path:
                temp_path = temp_path.replace(os.path.join(settings.STATIC_ROOT, ""), '')
            elif os.path.join(settings.DIR_ROOT, "") in temp_path:
                temp_path = temp_path.replace(os.path.join(settings.DIR_ROOT, ""), '')
            
            file_path = temp_path
    
    return file_path    
    

def strip_html_tags(mystring=''):
    retstring = strip_tags(mystring)
    retstring = retstring.replace('&nbsp;', ' ').replace('"', '\'').replace("'", '\'')
    return retstring
    


def get_date_or_None(date_string=None, date_time=False, datetime_to_use="now"):
    if date_string and date_string.strip() != '':
        try:
            parsed_date = parser.parse(date_string).date()
            if date_time:
                if datetime_to_use == 'min':
                    parsed_date = datetime.datetime.combine(parsed_date, datetime.datetime.min.time())
                elif datetime_to_use == 'max':
                    parsed_date = datetime.datetime.combine(parsed_date, datetime.datetime.max.time())
                else:
                    parsed_date = datetime.datetime.combine(parsed_date, datetime.datetime.timetz(datetime.datetime.now()))
        except Exception as e:
            print(e)
            pass
        else:
            return parsed_date
    return None


def create_pagination(paginator, request):
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        posts = paginator.page(page)
    except:
        posts = paginator.page(paginator.num_pages)

    return posts


def string_to_list(mystring):
    retlist = []
    if not empty(mystring):
        mystring = mystring.strip()
        if mystring != '':
            mylist = mystring.split(' ')
            for listitem in mylist:
                commalist = listitem.split(',')
                mylist2 = [x.strip() for x in commalist if x.strip() != '']
                retlist.extend(mylist2)
      
    return retlist


def get_general_settings(setting=None):
    from main.models import GeneralSetting
    retval = None
    if not empty(setting):
        general_setting = get_object_or_None(GeneralSetting, key=setting)
        if general_setting is not None:
            retval = general_setting.value
    return retval


def validate_phonenumber(phone_num, ret_val="string"):
    PHONE_REGEX = "^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$"
    phone_reg = re.compile(PHONE_REGEX)
    if phone_num is not None and not empty(phone_num):
        raw_number = phone_reg.split(phone_num)
        cleaned_number = [x for x in raw_number if len(x) > 0]
        if ret_val == "list":
            return cleaned_number
        elif ret_val == "e164":
            str_num = "".join(cleaned_number)
            if len(str_num) == 10:
                return "+1{}-{}-{}".format(str_num[0,3], str_num[3,5], str_num[6,9],)
        return "".join(cleaned_number)

