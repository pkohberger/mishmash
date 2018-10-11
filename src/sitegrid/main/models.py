from django.db import models
from django.template.defaultfilters import truncatechars





class GeneralSetting(models.Model):
    key = models.CharField(max_length=80, unique=True)
    value = models.TextField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "%s" % (self.key, )

    def __unicode__(self):
        return u"%s" % (self.key, )
        
    @property
    def short_value(self):
        if self.value is not None:
            return truncatechars(self.value, 255)
        return None


class PhoneNumber(models.Model):
    NUMBER_TYPES = (
      ('fax', 'Fax Number',),
      ('home', 'Home Number',),
      ('work', 'Work Number',),
      ('cell', 'Mobile Number',),
    )
    
    e164_number = models.CharField(max_length=32, unique=True)
    number_type = models.CharField(max_length=8, null=True, blank=True, choices=NUMBER_TYPES)
    ext = models.CharField(max_length=8, null=True, blank=True)
    
    
    def __str__(self):
        return self.e164_number
    
    def __unicode__(self):
        return u"%s" % (self.e164_number, )
        