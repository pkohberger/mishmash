from django import forms
from django.forms.utils import ErrorList
from shortcuts.utils import empty
from django.contrib.auth.models import User, Group
from accounts.models import *
from alist.models import *
from annoying.functions import get_object_or_None

class LoginForm(forms.Form):
    email = forms.EmailField(label='', max_length=100, widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),label='',  max_length=100, required=True)

class InviteUserForm(forms.Form):

    fullname = forms.CharField(label='Full Name', max_length=100, required=True)
    email = forms.EmailField(label='Email', required=True)
    phone = forms.CharField(label='Phone', max_length=100, required=True)

    def is_valid(self):

        valid = super(InviteUserForm, self).is_valid()

        if not valid:
            return valid

        user = get_object_or_None(User, email=self.cleaned_data['email'])
        if user is not None:
            self._errors["email"] = ErrorList([u"Email is already associated with an account!"])
            valid = False

        return valid

    def save(self, client_id):
        data = self.cleaned_data

        user = User()
        user.username = data.get('email')
        user.set_password(User.objects.make_random_password())
        user.first_name = data.get('fullname')
        user.email = data.get('email')
        user.is_active = False

        user.save()

        userProfile = UserProfile()
        userProfile.user_id = user.id
        userProfile.client_id = client_id
        userProfile.contact_email = data.get('email')
        userProfile.contact_phone = data.get('phone')
        userProfile.account_admin = False

        userProfile.save()

        return user

class RegisterForm(forms.Form):
    organization_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Organization'}), max_length=100, required=True)
    firstname = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Full Name'}), max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='',  max_length=100, required=True)
    confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),label='',  max_length=100, required=True)
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Email'}), required=True)
    phone = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Phone'}), max_length=100, required=True)

    def is_valid(self):

        valid = super(RegisterForm, self).is_valid()

        if not valid:
            return valid

        if get_object_or_None(ClientProfile, organization_name=self.cleaned_data['organization_name']) is not None:
            self._errors["organization_name"] = ErrorList([u"Organization already exists"])
            valid = False

        if self.cleaned_data['password'] != self.cleaned_data['confirm']:
            self._errors["password"] = ErrorList([u"Passwords do not match"])
            self._errors["confirm"] = ErrorList([u""])
            valid = False

        if get_object_or_None(User, email=self.cleaned_data['email']) is not None or get_object_or_None(ClientProfile, contact_email=self.cleaned_data['email']):
            self._errors["email"] = ErrorList([u"Account with email already exists!"])
            valid = False

        return valid

    def save(self):
        data = self.cleaned_data

        user = User()
        user.username = data.get('email')
        user.set_password(data.get('password'))
        user.first_name = data.get('firstname')
        user.email = data.get('email')
        user.save()

        clientProfile = ClientProfile()
        clientProfile.user_id = user.id
        clientProfile.organization_name = data.get('organization_name')
        clientProfile.contact_phone = data.get('phone')
        clientProfile.contact_email = data.get('email')
        clientProfile.save()

        userProfile = UserProfile()
        userProfile.user_id = user.id
        userProfile.client_id = clientProfile.id
        userProfile.contact_phone = data.get('phone')
        userProfile.contact_email = data.get('email')
        userProfile.save()



        return user.id

class CreateUserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput(),label='Password',  max_length=100, required=True)
    confirm = forms.CharField(widget=forms.PasswordInput(),label='Confirm Password',  max_length=100, required=True)
    firstname = forms.CharField(label='First Name', max_length=100, required=True)
    lastname = forms.CharField(label='Last Name', max_length=100, required=True)
    email = forms.EmailField(label='Email', required=True)

    def is_valid(self):

        valid = super(CreateUserForm, self).is_valid()

        if not valid:
            return valid

        if self.cleaned_data['password'] != self.cleaned_data['confirm']:
            self._errors["password"] = ErrorList([u"Passwords do not match"])
            self._errors["confirm"] = ErrorList([u"Passwords do not match"])
            return False

        return valid

    def save(self):
        data = self.cleaned_data

        user = User()
        user.username = data.get('username')
        user.set_password(data.get('password'))
        user.first_name = data.get('firstname')
        user.last_name = data.get('lastname')
        user.email = data.get('email')

        user.save()

        return user.id

class CreateUserProfileForm(forms.Form):

    prefix = forms.CharField(label='Prefix', max_length=5, required=False)
    middle_name = forms.CharField(label='Middle Name', max_length=100, required=False)
    suffix = forms.CharField(label='Suffix', max_length=5, required=False)
    contact_phone = forms.CharField(label='Contact Phone', max_length=14, required=True)
    contact_email = forms.EmailField(label='Contact Email', required=True)

    def save(self, user_id, client_id):
        data = self.cleaned_data

        userProfile = UserProfile()
        userProfile.user_id = user_id
        userProfile.prefix = data.get('prefix')
        userProfile.middle_name = data.get('middle_name')
        userProfile.suffix = data.get('suffix')
        userProfile.contact_phone = data.get('contact_phone')
        userProfile.contact_email = data.get('contact_email')
        userProfile.client_id = client_id

        userProfile.save()

        return self

class CreateAccountProfileForm(forms.Form):

    organization_name = forms.CharField(label='Organization', max_length=100, required=True)
    organization_phone = forms.CharField(label='Organization Phone', max_length=14, required=True)
    organization_email = forms.EmailField(label='Organization Email', required=True)

    def save(self, user_id):
        data = self.cleaned_data

        userAccountProfile = ClientProfile()
        userAccountProfile.user_profile_id = user_id
        userAccountProfile.organization_name = data.get('organization_name')
        userAccountProfile.contact_phone = data.get('organization_phone')
        userAccountProfile.contact_email = data.get('organization_email')

        userAccountProfile.save()

        return userAccountProfile.id

class EditClientInfoForm(forms.Form):

    name = forms.CharField(label='', max_length=100, required=True)
    email = forms.EmailField(label='Organization Email', required=True)
    phone = forms.CharField(label='Organization Phone', max_length=14, required=True)

    def save(self, commit=True, *args, **kwargs):
        client_id = kwargs.pop('client_id')
        data = self.cleaned_data

        userAccountProfile = ClientProfile.objects.get(id=client_id)

        userAccountProfile.organization_name = data.get('name')
        userAccountProfile.contact_email = data.get('email')
        userAccountProfile.contact_phone = data.get('phone')

        userAccountProfile.save()

        return self

class EditProfileInfoForm(forms.Form):

    name = forms.CharField(label='', max_length=190, required=True)
    phone = forms.CharField(label='', max_length=14, required=True)
    email = forms.EmailField(label='', required=True)

    def is_valid(self):

        valid = super(EditProfileInfoForm, self).is_valid()

        if not valid:
            return valid

        return valid

    def save(self, commit=True, *args, **kwargs):
        user_id = kwargs.pop('user_id')

        data = self.cleaned_data

        userProfile = UserProfile.objects.get(user_id=user_id)

        userProfile.user.first_name = data.get('name')
        userProfile.user.save()

        userProfile.contact_phone = data.get('phone')
        userProfile.contact_email = data.get('email')

        userProfile.save()

        return self

class EditUserForm(forms.Form):
    username = forms.EmailField(label='', max_length=190, required=True)

    def is_valid(self, user_id, username):

        valid = super(EditUserForm, self).is_valid()

        if not valid:
            return valid

        try:
            user = User.objects.exclude(pk=user_id).get(username=username)
        except:
            self._errors["username"] = ErrorList([u"Username already exists"])
            valid == False

        return valid

    def save(self, commit=True, *args, **kwargs):
        user_id = kwargs.pop('user_id')

        data = self.cleaned_data

        user = User.objects.get(pk=user_id)
        user.username = data.get('username')
        user.email = data.get('username')

        user.save()

        print user.username

        return self

class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(),label='Password',  max_length=100, required=True)
    confirm = forms.CharField(widget=forms.PasswordInput(),label='Confirm Password',  max_length=100, required=True)

    def is_valid(self):

        valid = super(ChangePasswordForm, self).is_valid()

        if not valid:
            return valid

        if self.cleaned_data['password'] != self.cleaned_data['confirm']:
            self._errors["password"] = ErrorList([u"Passwords do not match"])
            self._errors["confirm"] = ErrorList([u"Passwords do not match"])
            return False

        return valid

    def save(self, commit=True, *args, **kwargs):
        user_id = kwargs.pop('user_id')

        data = self.cleaned_data

        user = User.objects.get(pk=user_id)
        user.set_password(data.get('password'))

        user.save()

        return self
