from decimal import Decimal
from decimal import ROUND_HALF_UP

# formata o valor monetario para o formato CNAB
# usamos Decimal e nao float porque float perde centavos
# ex.: 150.70 * 100 em float da 15069.999... e o boleto sairia com 150,69
def valor_cnab(valor, tamanho=13):
    valor_decimal = Decimal(str(valor)) #convertemos em decimal exato
    valor_centavos = valor_decimal * 100 #multiplicamos por 100 para transformar em centavos
    valor_arredondado = valor_centavos.quantize(Decimal("1"), rounding=ROUND_HALF_UP) #tira as casas que sobraram
    valor_inteiro = int(valor_arredondado) #transforma em inteiro
    valor_texto = str(valor_inteiro) #converte em string (texto)
    if len(valor_texto) > tamanho:
        raise Exception("Valor muito grande")
    while len(valor_texto) < tamanho:
        valor_texto = "0" + valor_texto
    return valor_texto


# caminho contrario do valor_cnab, usado na leitura do retorno
# o banco manda o valor em centavos e sem virgula, entao dividimos por 100
def valor_de_cnab(texto):
    texto = str(texto)

    somente_digitos = ""

    for caractere in texto:
        if caractere.isdigit():
            somente_digitos += caractere

    if somente_digitos == "":
        raise Exception("Valor CNAB sem digitos")

    valor_centavos = Decimal(somente_digitos)
    valor_reais = valor_centavos / Decimal(100)

    return valor_reais.quantize(Decimal("0.01"))
