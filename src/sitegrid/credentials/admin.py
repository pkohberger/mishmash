from django.contrib import admin


from credentials.models import Project, ProjectCredentialConnection, CredentialType, Credential
from credentials.utils import rsa_decrypt

import base64

class ProjectCredentialInline(admin.TabularInline):
    model = ProjectCredentialConnection
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    
    list_display = ('name', )

    save_on_top = True
    
    inlines = [
        ProjectCredentialInline,
        ]

class CredentialAdmin(admin.ModelAdmin):
    
    def raw_credential(self, obj):
        encrypted_credential = [obj.session_key.encode('utf-8'), obj.nonce.encode('utf-8'), obj.key_tag.encode('utf-8'), obj.credential.encode('utf-8')]
        try:
            decrypted_cred = rsa_decrypt(encrypted_credential)
        except Exception as e:
            return "???? %s" % (e, )
        else:
            return decrypted_cred
  
    list_display = ('credential_name', 'credential_domain', 'credential_type', 'credential_username', 'raw_credential', )

    
    #raw_id_fields = ('user', )
    save_on_top = True

    inlines = [
        ProjectCredentialInline,
        ]


class CredentialTypeAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', )

    
    save_on_top = True



admin.site.register(Project, ProjectAdmin)
admin.site.register(Credential, CredentialAdmin)
admin.site.register(CredentialType, CredentialTypeAdmin)

