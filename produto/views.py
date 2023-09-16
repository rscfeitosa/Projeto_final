from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name='produtos'
    paginate_by = 3


class DetalheProdutos(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name='produto'
    slug_url_kwarg = 'slug'


class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer =self.request.META.get('HTTP_REFERER', reverse ('produto:lista'))
        prod_id = self.request.GET.get('vid')

        if not prod_id:
            messages.error(
            self.request,
            'Produto Não Existe'
            )
            return redirect(http_referer)
        prod= get_object_or_404(models.Variacao, id=prod_id)

        if not self.request.session.get('carrinho'):
            self.request.session["carrinho"] = {}
            self.request.session.save()
        
        carrinho = self.request.session['carrinho']

        if prod_id in carrinho:
            pass
        else:
            pass

        return HttpResponse (f'{prod.produto} {prod.nome}')


class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse ('REMOVER')


class Carrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse ('CARRINHO')



class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse ('FIM')