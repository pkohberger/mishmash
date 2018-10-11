from django.db import models


from clients.models import ClientAccount




class Project(models.Model):
    name = models.CharField(max_length=190)
    client = models.ForeignKey(ClientAccount, on_delete=models.CASCADE, related_name="client_projects")
    

    def __str__(self):
        return self.name
        
    def __unicode__(self):
        return u"%s" % (self.name, )




class Credential(models.Model):
    credential_name = models.CharField(max_length=80, blank=True, null=True)
    credential_username = models.CharField(max_length=80, blank=True, null=True)
    credential_domain = models.CharField(max_length=80, blank=True, null=True)
    credential = models.TextField(blank=True, null=True)
    nonce = models.TextField(blank=True, null=True)
    session_key = models.TextField(blank=True, null=True)
    key_tag = models.TextField(blank=True, null=True)
    credential_type = models.ForeignKey('CredentialType', on_delete=models.CASCADE)
    credential_notes = models.TextField(blank=True, null=True)
    projects = models.ManyToManyField(Project, through='ProjectCredentialConnection')
    
    

class CredentialType(models.Model):
    friendly_name = models.CharField(max_length=80)
    
    
    def __str__(self):
        return self.friendly_name
    
    def __unicode__(self):
        return u"%s" % (self.friendly_name, )
        


class ProjectCredentialConnection(models.Model):
    credential = models.ForeignKey('Credential', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


    
    
    
    
    


