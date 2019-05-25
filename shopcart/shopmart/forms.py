from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime,time
from shopmart.models import *


class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())


    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': ' input100'})
        self.fields['last_name'].widget.attrs.update({'class': ' input100'})
        self.fields['email'].widget.attrs.update({'class': ' input100'})
        self.fields['password'].widget.attrs.update({'class': ' input100'})
        self.fields['confirm_password'].widget.attrs.update({'class': ' input100'})

    def clean_confirm_password(self):
        d = self.cleaned_data
        if d.get('password') != d.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match")
        if len(d.get('password')) < 6:
            raise forms.ValidationError("The passwords should must be at least 6 character long")
        return d.get('confirm_password')

    def clean_email(self):
        try:
            User.objects.get(username=self.cleaned_data.get('email'))
            raise forms.ValidationError("User with this email already exists")
        except User.DoesNotExist:
            return self.cleaned_data.get('email')

    def save(self, *args, **kwargs):

        d = self.cleaned_data
        u_dict = {
            'username': d.get('email'),
            'first_name': d.get('first_name'),
            'last_name': d.get('last_name'),
            'email': d.get('email'),
            'last_login': datetime.datetime.now(),
        }
        u = User.objects.create(**u_dict)
        u.set_password(d.get('password'))
        u.save()


        buyer_dict = {
            'user': u,
        }
       # buyer = Buyer.objects.create(**buyer_dict)
        return u
