def formatar_preco(val):
    #print (f'R$ {val:.2f}'.replace('.', ','))
    return  (f'R$ {val:.2f}'.replace('.', ','))

def cart_totalqtd(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])

def cart_totals(carrinho):
    return sum(
        [
            item.get('preco_quantitativo_promocional')
            if item.get('preco_quantitativo_promocional')
            else item.get('preco_quantitativo') or item.get('preco_unitario') 
            for item
            in carrinho.values()
        ]
    )
