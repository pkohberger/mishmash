from django.conf import settings
#from django.contrib.auth.user import User  # Obsolete
from django.contrib.auth import get_user_model
from django.db import models

from main.models import PhoneNumber
#from credentials.models import Credential

User = get_user_model()


class ClientAccount(models.Model):
    
    name = models.CharField(max_length=190)
    address = models.CharField(max_length=190, null=True, blank=True)
    city = models.CharField(max_length=80, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True, choices=settings.US_STATES)
    zipcode = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=2, null=True, blank=True, choices=settings.COUNTRIES)
    
    phone_numbers = models.ManyToManyField(PhoneNumber, blank=True)
    

    def __str__(self):
        return self.name
        
    def __unicode__(self):
        return u"%s" % (self.name, )
        



class ClientContact(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, related_name='client_contacts', on_delete=models.CASCADE)
    clients = models.ManyToManyField(ClientAccount, through='ClientConnection')

    def __str__(self):
        return self.user.get_full_name
        
    def __unicode__(self):
        return u"%s" % (self.user.get_full_name, )
    
    def organizations(self):
        return ", \n".join([client.name for client in self.clients.all()])


class ClientConnection(models.Model):
    contact = models.ForeignKey(ClientContact, on_delete=models.CASCADE)
    account = models.ForeignKey(ClientAccount, on_delete=models.CASCADE)


