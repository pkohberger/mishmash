from django import forms


class NoSpacesCharField(forms.CharField):
    def validate(self, value):
        # Use the parent's handling of required fields, etc.
        super(NoSpacesCharField, self).validate(value)

        if value and value.strip() == '':
            raise forms.ValidationError(u"You must provide more than just whitespace.")
            
    def clean(self, value):
        value = super(forms.CharField, self).clean(value)
        if not value is None:
            value = value.strip()
        
        return value
        

class ConfirmationForm(forms.Form):
    confirm = forms.BooleanField(label='Are you sure you want to do this?', required=False)
    
class FileUploadForm(forms.Form):
    csv_file = forms.FileField(label="Select the file to upload", required=True)

