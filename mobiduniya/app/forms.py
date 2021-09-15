from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, UsernameField,PasswordChangeForm,PasswordResetForm
from django.forms import fields, models, widgets
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth import password_validation

class CustomerRegistrationForm(UserCreationForm):
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control input-style'}))
    password2=forms.CharField(label='Confirm Password (again)',widget=forms.PasswordInput(attrs={'class':'form-control input-style'}))
    email=forms.CharField(required=True,widget=forms.EmailInput(attrs={'class':'form-control input-style'}))

    class Meta:
        model=User
        fields=['username','email','password1','password2']
        labels={'email':'Email'}
        widgets={'username':forms.TextInput(attrs={'class':'form-control input-style'})}

class LoginForm(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control input-style'}))
    password=forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control input-style'}))

class MyPasswordChangeForm(PasswordChangeForm):
    old_password=forms.CharField(label=_("Old Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control input-style'}))
    new_password1=forms.CharField(label=_("New Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control input-style'}),help_text=password_validation.password_validators_help_text_html())
    new_password2=forms.CharField(label=_("Confirm New Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control input-style'}))

class MyPasswordResetForm(PasswordResetForm):
    email=forms.EmailField(label=_("Email"),max_length=50,widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control input-style'}))
        
        
