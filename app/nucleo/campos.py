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
    valor = str(valor).upper()

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