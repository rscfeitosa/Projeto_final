from django.shortcuts import render, get_list_or_404, redirect
from django.views.generic import ListView
from django.views   import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import copy
from django.contrib import messages
from . import models
from . import forms



class BaseCliente(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.carrinho = copy.deepcopy(self.request.session.get('carrinho',{}))#copiando carrinho para o perfil do user

        self.cliente = None

        if self.request.user.is_authenticated: #checando o User
            self.cliente = models.Cliente.objects.filter(cliente=self.request.user).first()

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

        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'


        self.renderizar = render(self.request,self.template_name,self.contexto )

    def get(self, *args, **kwargs):
        return self.renderizar


class Criar(BaseCliente):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.clienteform.is_valid():
            messages.error(
                self.request,
                'Existem erros no formulário de cadastro. Verifique se todos '
                'os campos foram preenchidos corretamente.'
            )
            return self.renderizar
        
        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        #user logado
        if self.request.user.is_authenticated:
            usuario = get_list_or_404(User, username=self.request.user.username)
            usuario.username = username

            if password:
                usuario.set_password(password)
            
            usuario.email =email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()

            if not self.cliente:
                self.clienteform.cleaned_data['usuario'] = usuario
                cliente = models.Cliente(**self.clienteform.cleaned_data)
                cliente.save()
            else:
                cliente = self.clienteform.save(commit=False)
                cliente.usuario= usuario
                cliente.save()


         

        #user não logado (novo)
        else:
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            cliente = self.clienteform.save(commit=False)
            cliente.cliente= usuario
            cliente.save()

        if password:
            autentica = authenticate(self.request, username=usuario, password=password)
        
        if autentica:
            login(self.request, user=usuario)



        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()

        messages.success(
            self.request,
            'Seu cadastro foi criado ou atualizado com sucesso.'
        )
        messages.success(
            self.request,
            'Você fez login e pode concluir sua compra.'
        )

        return redirect('cliente:criar')
        return self.renderizar



class Atualizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse ('ATUALIZAR')


class Login(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        
        if not username or not password:
            messages.erro(
            self.request,
            'Usuario ou senha invalidos.'
            )
            return redirect('cliente:criar')
        usuario = authenticate (self.request, username=username, password=password)

        if not usuario:
            messages.erro(
            self.request,
            'Usuario ou senha invalidos.'
            )
            return redirect('cliente:criar')
        
        
        login(self.request, user=usuario)
        messages.success(
        self.request,
        'Login realizado com sucesso'
        )
        return redirect ('produto:carrinho')



class Logout(View):
    def get(self, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('carrinho'))

        logout(self.request)

        self.request.session['carrinho'] = carrinho
        self.request.session.save()

        return redirect('produto:lista')