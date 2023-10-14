from django.urls import path
from . import views
from produto.views import cadastro, adicionarproduto, conexao, detalheproduto
from django.conf import settings
from django.conf.urls.static import static


app_name= 'produto'

urlpatterns =[
    path('', views.ListaProdutos.as_view(), name='lista'),
    path('<slug>', views.DetalheProdutos.as_view(), name='detalhe'),
    path('adicionaraocarrinho/', views.AdicionarAoCarrinho.as_view(), name='adicionaraocarrinho'),
    path('removerdocarrinho/', views.RemoverDoCarrinho.as_view(), name='removerdocarrinho'),
    path('carrinho/', views.Carrinho.as_view(), name='carrinho'),
    path('finalizar/', views.Finalizar.as_view(), name='finalizar'),
    path('cadastro/', cadastro,name='cadastro'),
    path('adicionarproduto/', adicionarproduto, name='adicionarproduto'),
    path('detalheproduto/<int:pk>/',detalheproduto,name='detalheproduto'),
    path('conexao/', conexao,name='conexao'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)