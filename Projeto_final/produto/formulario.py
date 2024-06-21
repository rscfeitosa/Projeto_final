from django.forms import ModelForm
from produto.models import Produto, Variacao

# Create the form class.
class ProdutoForm(ModelForm):
    class Meta:
        model = Produto
        fields = ["nome", "descricao_curta", "desricao_longa","imagem", "preco_marketing", "preco_marketing_promocional","tipo"]

class VariacaoForm(ModelForm):
    class Meta:
        model = Variacao
        fields = ["produto","nome","preco","estoque"]
