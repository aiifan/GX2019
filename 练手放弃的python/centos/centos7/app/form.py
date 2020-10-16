from django import forms


class serverform(forms.Form):
    serverip = forms.GenericIPAddressField(label='ip', widget=forms.TextInput(attrs={'placeholder':'ip addr'}))
    serverport = forms.IntegerField(label="端口", initial=22)
    serveruser = forms.CharField(label="用户", initial='root', widget=forms.TextInput(attrs={'placeholder':'user'}))
    serverpwd = forms.CharField(label='密码',widget=forms.PasswordInput(attrs={'placeholder':'password'}))

