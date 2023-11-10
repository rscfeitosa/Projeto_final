from django.shortcuts import render
from django.views.generic import ListView
from django.views   import View
from django.http import HttpResponse

from . import models
from . import forms



class BaseCliente(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        if self.request.user.is_authenticated:

            self.contexto ={
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user,
                    ),
                'clienteform': forms.ClienteForm(
                    data=self.request.POST or None
                    )
            }

        else:
            self.contexto ={
                'userform': forms.UserForm(data=self.request.POST or None),
                'clienteform': forms.ClienteForm(data=self.request.POST or None)
            }

        self.renderizar = render(self.request,self.template_name,self.contexto )

    def get(self, *args, **kwargs):
        return self.renderizar


class Criar(BaseCliente):
    def post(self, *args, **kwargs):
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