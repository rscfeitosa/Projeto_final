from django.shortcuts import render, redirect, reverse, get_object_or_404 
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models
from produto.formulario import ProdutoForm
from produto.models import Produto

from pprint import pprint



class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name='produtos'
    paginate_by = 8
    


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
        prod_estoque = prod.estoque
        produto = prod.produto

        produto_id = produto.id
        produto_nome = produto.nome
        prod_nome = prod.nome or ''
        preco_unitario = prod.preco
        preco_unitario_promocional = prod.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''


        if prod.estoque <1:
            messages.error(
                self.request,
                "Estoque Insuficiente"
            )
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session["carrinho"] = {}
            self.request.session.save()
        
        carrinho = self.request.session['carrinho']

        if prod_id in carrinho:
            quantidade_carrinho = carrinho[prod_id]['quantidade']
            quantidade_carrinho += 1

            if prod_estoque < quantidade_carrinho:
                messages.warning(
                self.request,
                f"Estoque Insuficiente pra {quantidade_carrinho}x  no "
                f'produto "{produto_nome}" .Adicionamos {prod_estoque}x ' 
                f' no seu carrinho '
            )
            quantidade_carrinho = prod_estoque

            carrinho[prod_id]['quantidade'] = quantidade_carrinho
            carrinho[prod_id] ['preco_quantitativo'] = preco_unitario *  quantidade_carrinho
            carrinho[prod_id] ['preco_quantitativo_promocional'] = preco_unitario_promocional *  quantidade_carrinho





        else:
            carrinho[prod_id]={
                'produto_id'   : produto_id,
                'produto_nome' : produto_nome,
                'prod_nome' : prod_nome,
                'prod_id' : prod_id,
                'preco_unitario' : preco_unitario,
                'preco_unitario_promocional' : preco_unitario_promocional,
                'preco_quantitativo_promocional ' : preco_unitario_promocional,
                'quantidade' : 1,
                'slug' : slug,
                'imagem' : imagem, }

        self.request.session.save()

        messages.success(
        self.request,
        f' Produto {produto_nome} {prod_nome} adicionado com sucesso ao carrinho'
        f'Quantidade de produto adicionado {carrinho[prod_id]["quantidade"]}'
        )
        return redirect(http_referer)



class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse ('REMOVER')


class Carrinho(View):
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho',{})
        }
        return render(self.request, 'produto/carrinho.html', contexto)



class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse ('FIM')
    

def cadastro(request):
   data = {}
   data['db'] = Produto.objects.all()
   return render (request, "produto/homecadastro.html", data)

def adicionarproduto(request):
   data={}
   data['formulario'] = ProdutoForm()
   return render (request, "produto/formulario.html", data)

def conexao(request):
   if request.method == 'POST':
    produto = ProdutoForm(request.POST,request.FILES or None)
    if produto.is_valid():
        produto.save()
        return redirect ('produto:cadastro')
    else:
        return HttpResponse ('ERRO DE CORXÃO')
 

def detalheproduto(request, pk):
   data={}
   data['db'] = Produto.objects.get(pk=pk)
   return render (request, 'produto/detalheproduto.html', data)

def edit(request, pk):
   data={}
   data['db'] = Produto.objects.get(pk=pk)
   data['formulario'] = ProdutoForm(instance=data['db'])
   return render (request, "produto/formulario.html", data)

def update(request, pk):
    data={}
    data['db'] = Produto.objects.get(pk=pk)
    if request.method == 'POST':
        produto = ProdutoForm(request.POST,request.FILES or None, instance=data['db'])
        if produto.is_valid():
            produto.save()
            return redirect ('produto:cadastro')
    else:
        return HttpResponse ('ERRO DE CORXÃO')

def delete(requeste, pk):
    db = Produto.objects.get(pk=pk)
    db.delete()
    return redirect ('produto:cadastro')