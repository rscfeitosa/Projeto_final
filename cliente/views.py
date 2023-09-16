from django.shortcuts import render
from django.views.generic import ListView
from django.views   import View
from django.http import HttpResponse


class Criar(View):
    def get(self, *args, **kwargs):
        return HttpResponse ('CRIAR')


class Atualizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse ('ATUALIZAR')


class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse ('LOGIN')


class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse ('LOGOUT')