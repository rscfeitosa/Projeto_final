from django.template import Library
from utils import utils 

register = Library()


@register.filter
def formatar_preco(val):
    return utils.formatar_preco(val)

@register.filter
def cart_totalqtd(carrinho):
    return utils.cart_totalqtd(carrinho)