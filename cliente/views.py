from django.shortcuts import render, get_list_or_404
from django.views.generic import ListView
from django.views   import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import copy

from . import models
from . import forms



class BaseCliente(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.carrinho = copy.deepcopy(self.request.session.get('carrinho',{}))#copiando carrinho para o perfil do user

        self.perfil = None

        if self.request.user.is_authenticated: #checando o User
            self.perfil = models.Cliente.objects.filter(usuario=self.request.user).first()
            self.contexto ={
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user,
                    ),
                'clienteform': forms.ClienteForm(
                    data=self.request.POST or None,
                    instance=self.cliente
                    )
            }

        else:
            self.contexto ={
                'userform': forms.UserForm(data=self.request.POST or None),
                'clienteform': forms.ClienteForm(data=self.request.POST or None)
            }


        self.userform=self.contexto['userform']
        self.clienteform = self.contexto['clienteform']



        self.renderizar = render(self.request,self.template_name,self.contexto )

    def get(self, *args, **kwargs):
        return self.renderizar


class Criar(BaseCliente):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            return self.renderizar
        
        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        #user logado
        if self.request.user.is_authenticated:
            usuario = get_list_or_404(User, username=self.request.user.username)
            #usuario.username = username

            if password:
                usuario.set_password(password)
            
            usuario.email =email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()

            pass

        #user não logado (novo)
        else:
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.clienteform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        if password:
            autentica = authenticate(self.request, username=usuario, password=password)
        
        if autentica:
            login(self.request, user=usuario)



        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()

        return self.renderizar



class Atualizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse ('ATUALIZAR')


class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse ('LOGIN')


class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse ('LOGOUT')