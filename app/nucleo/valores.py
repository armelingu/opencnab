# formata o valor monetario para o formato CNAB
def valor_cnab(valor, tamanho=13):
    valor_decimal = float(valor) #convertemos em decimal
    valor_centavos = valor_decimal * 100 #multiplicamos por 100 para transformar em centavos
    valor_inteiro = int(valor_centavos) #transforma em inteiro
    valor_texto = str(valor_inteiro)#converte em string (texto)
    while len(valor_texto) < tamanho:
        valor_texto = "0" + valor_texto
    return valor_texto

