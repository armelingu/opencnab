from opencnab.nucleo.modulo11 import calcular_digito_verificador

def gerar_nosso_numero(numero, carteira="109"):
    numero = str(numero)
    novo_numero = ""
    for caractere in numero:
        if caractere.isdigit():
            novo_numero += caractere

    if len(novo_numero) > 11:
        raise Exception("Nosso Número não pode ter mais de 11 posições")

    while len(novo_numero) < 11:
        novo_numero = "0" + novo_numero

    numero_para_calculo = str(carteira) + novo_numero
    digito_verificador = calcular_digito_verificador(numero_para_calculo)
    nosso_numero_completo = novo_numero + "-" + str(digito_verificador)

    return nosso_numero_completo