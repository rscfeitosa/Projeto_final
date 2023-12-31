from django import forms
from django.contrib.auth.models import User
from . import models


class ClienteForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = '__all__'
        exclude = ('cliente','usuario')

class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha'
    )

    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmação senha'
    )    


    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario

    class Meta:
        model = models.User
        fields = ('first_name','last_name','username','password','password2','email')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        usuario_data = cleaned.get('username') 
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')
        email_data =cleaned.get('email')           
        

        usuario_db=User.objects.filter(username=usuario_data)
        email_db=User.objects.filter(username=email_data).first()

        error_msg_user_existe = "Usuario já existe"
        error_msg_email_existe = "email já existe"
        error_msg_pasword_match = "Senhas não conferem"
        error_msg_pasword_short = "sua senha precisa no minimo de 6 caracteres"
        error_msg_required_field = "Campo obrigatório "

        #User LOgado
        if self.usuario:
            if usuario_db:
                if usuario_data != usuario_db.username:
                    if usuario_db:
                        validation_error_msgs['username']= error_msg_user_existe
            if email_db:            
                if email_data != email_db.email:
                    validation_error_msgs['email'] = error_msg_email_existe

            if password_data:        
                if password_data != password2_data:
                    validation_error_msgs['password']= error_msg_pasword_match   
                    validation_error_msgs['password2']= error_msg_pasword_match 
                if len(password_data)<6:
                    validation_error_msgs['password'] = error_msg_pasword_short    



            
        #user não logado
        else:
            if usuario_db:
                validation_error_msgs['username']= error_msg_user_existe
            if email_db:
                validation_error_msgs['email'] = error_msg_email_existe

            if not password_data:
                validation_error_msgs['password'] = error_msg_required_field
            
            if not password2_data:
                validation_error_msgs['password2'] = error_msg_required_field
     
            if password_data != password2_data:
                validation_error_msgs['password']= error_msg_pasword_match   
                validation_error_msgs['password2']= error_msg_pasword_match 
                
            if len(password_data)<6:
                validation_error_msgs['password'] = error_msg_pasword_short    


        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))


