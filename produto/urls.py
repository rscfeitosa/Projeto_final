from django.urls import path
from . import views
from produto.views import cadastro, adicionarproduto, conexao, detalheproduto, edit, update, delete, estoque
from django.conf import settings
from django.conf.urls.static import static


app_name= 'produto'

urlpatterns =[
    path('', views.ListaProdutos.as_view(), name='lista'),
    path('<slug>', views.DetalheProdutos.as_view(), name='detalhe'),
    path('adicionaraocarrinho/', views.AdicionarAoCarrinho.as_view(), name='adicionaraocarrinho'),
    path('removerdocarrinho/', views.RemoverDoCarrinho.as_view(), name='removerdocarrinho'),
    path('carrinho/', views.Carrinho.as_view(), name='carrinho'),
    path('resumodacompra/', views.ResumoDaCompra.as_view(), name='resumodacompra'),
    path('cadastro/', cadastro,name='cadastro'),
    path('adicionarproduto/', adicionarproduto, name='adicionarproduto'),
    path('detalheproduto/<int:pk>/',detalheproduto,name='detalheproduto'),
    path('conexao/', conexao,name='conexao'),
    path('estoque/<int:pk>/', estoque,name='estoque'),
    path('edit/<int:pk>/',edit,name='edit'),
    path('update/<int:pk>/',update,name='update'),
    path('delete/<int:pk>/',delete,name='delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)