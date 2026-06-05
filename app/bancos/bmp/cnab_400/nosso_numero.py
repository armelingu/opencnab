def gerar_nosso_numero(numero):
    numero = str(numero)

    novo_numero = ""

    for caractere in numero:
        if caractere.isdigit():
            novo_numero += caractere

    if len(novo_numero) > 11:
        raise Exception(
            "Nosso Número não pode ter mais de 11 posições"
        )

    while len(novo_numero) < 11:
        novo_numero = "0" + novo_numero

    return novo_numero