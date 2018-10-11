from django import forms

from credentials.models import Credential
from credentials.utils import rsa_encrypt
from shortcuts.forms import NoSpacesCharField

import sys

class CredentialForm(forms.ModelForm):
    raw_credential = NoSpacesCharField(max_length=80, required=True, label="Credential")
  
    class Meta:
        model = Credential
        fields = ['raw_credential', 'credential_name', 'credential_username', 'credential_domain', 'credential_type', 'credential_notes', ]
        #fields = ['credential_name', 'credential_username', 'credential_domain', 'credential_type', 'credential_notes', 'projects', 'raw_credential', ]
    
    def clean(self):
        cleaned_data = super(CredentialForm, self).clean()
        #raw = cleaned_data.get('raw_credential')
        #sys.stderr.write('Raw: %s' % (raw, ))
        '''
        if raw is not None:
            cred_list = rsa_encrypt(raw)
            if not cred_list:
                #sys.stderr.write('Cred List: %s' % (cred_list, ))
                raise forms.ValidationError('Unable to process credential.  Try again with a different credential!')
        
            cleaned_data['session_key'] = cred_list[0]
            cleaned_data['nonce'] = cred_list[1]
            cleaned_data['key_tag'] = cred_list[2]
            cleaned_data['credential'] = cred_list[3]
        '''
        
        return cleaned_data
              
        
    def save(self, commit=True, *args, **kwargs):
        # TODO pop projects and add them to the through table, AFTER saving the model commit False, to get a pk.
        raw = self.cleaned_data.pop('raw_credential')
        data = self.cleaned_data
        cred = super(CredentialForm, self).save(commit=False)
        cred_list = rsa_encrypt(raw)
        cred.session_key = cred_list[0].decode('utf-8')
        cred.nonce = cred_list[1].decode('utf-8')
        cred.key_tag = cred_list[2].decode('utf-8')
        cred.credential = cred_list[3].decode('utf-8')
    
        cred.save()
        
        return cred
        
        
        