# deixa no documento so os numeros, tirando ponto, barra e traco
def somente_numeros(documento):
    documento = str(documento)

    novo = ""

    for caractere in documento:
        if caractere.isdigit():
            novo += caractere

    return novo


# o CNAB identifica quem esta pagando pelo tipo de inscricao
# 01 = CPF (11 digitos) e 02 = CNPJ (14 digitos)
def tipo_inscricao(documento):
    documento_limpo = somente_numeros(documento)

    if len(documento_limpo) == 11:
        return "01"

    if len(documento_limpo) == 14:
        return "02"

    raise Exception("Documento precisa ter 11 digitos para CPF ou 14 para CNPJ")


# nos comandos enviados sobre um titulo que ja esta registrado o banco nao
# pede os dados do pagador, e o layout manda preencher o campo com zeros
def tipo_inscricao_ou_zeros(documento):
    documento_limpo = somente_numeros(documento)

    if documento_limpo == "":
        return "00"

    return tipo_inscricao(documento)
