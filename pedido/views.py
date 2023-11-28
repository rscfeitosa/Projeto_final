from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views   import View
from django.http import HttpResponse
from django.contrib import messages


class Pagar(View):
     template_name = 'pedido/pagar.html'


     def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            pass

        contexto = {

        }


        return render(self.request, self.template_name, contexto)


class SalvarPedido(View):
    def get(self, *args, **kwargs):
        return HttpResponse ('FECHAR PEDIDO')


class Detalhe(View):
    def get(self, *args, **kwargs):
        return HttpResponse ('DETALHE')



