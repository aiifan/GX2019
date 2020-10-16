from django import forms

class NameForm(forms.Form):
    name = forms.CharField(label='You name', max_length=100)
    passwd = forms.CharField(label='password', widget=forms.PasswordInput)