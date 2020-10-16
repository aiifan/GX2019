from django import forms

class NameForm(forms.Form):
    name = froms.CharField(label='html_name',max_length=100)
    