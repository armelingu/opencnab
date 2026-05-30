# formata o valor monetario para o formato CNAB
def valor_cnab(valor, tamanho=13):
    valor = float(valor) 
    valor = valor * 100
    valor = int(valor)
    texto = str(valor)
    while len(texto) < tamanho:
        texto = "0"+ texto
    return texto