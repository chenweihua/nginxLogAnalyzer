from django.contrib.auth.forms import AuthenticationForm 
from django import forms

'''
In this file we define our form, we have two form, 
one for document upload, and second form allow user 
to write his own regex, that will be used during analyzing process!
'''

class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))