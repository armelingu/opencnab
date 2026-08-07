import unicodedata


# o arquivo CNAB so aceita caracteres da tabela ASCII
# 1. o NFD separa a letra do acento (ex.: "Á" vira "A" + acento solto)
# 2. jogamos fora o acento solto e ficamos so com a letra
# 3. o que ainda sobrar fora do ASCII vira espaco
def remover_acentos(valor):
    texto_separado = unicodedata.normalize("NFD", str(valor))

    novo = ""

    for caractere in texto_separado:
        if unicodedata.combining(caractere) == 0:
            if ord(caractere) > 127:
                novo += " "
            else:
                novo += caractere

    return novo


def numerico(valor, tamanho):
    valor = str(valor)

    novo = ""

    for c in valor:
        if c.isdigit():
            novo += c

    if len(novo) > tamanho:
        raise Exception("Valor muito grande")

    while len(novo) < tamanho:
        novo = "0" + novo

    return novo


def alfa(valor, tamanho):
    valor = remover_acentos(valor).upper()

    if len(valor) > tamanho:
        valor = valor[0:tamanho]

    while len(valor) < tamanho:
        valor += " "

    return valor


def branco(tamanho):
    txt = ""

    for i in range(tamanho):
        txt += " "

    return txt


def zeros(tamanho):
    txt = ""

    for i in range(tamanho):
        txt += "0"

    return txt