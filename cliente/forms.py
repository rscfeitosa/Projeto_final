from django import forms
from django.contrib.auth.models import User
from . import models


class ClienteForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = '__all__'
        exclude = ( 'usuario',)

class UserForm(forms.ModelsForm):
    class Meta:
        model = models.User
        fields = ('first_name','last_name','username','password','email')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data