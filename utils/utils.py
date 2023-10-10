def formatar_preco(val):
    return f' R${val:.2f}'.replace('.', ',')

def cart_totalqtd(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])