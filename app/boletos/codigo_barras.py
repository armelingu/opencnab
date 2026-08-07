from datetime import date
from app.nucleo.campos import numerico
from app.nucleo.valores import valor_cnab
from app.nucleo.modulo11 import calcular_digito_codigo_barras

# o fator de vencimento conta os dias ate o vencimento a partir de uma data base
# a contagem antiga comecou em 07/10/1997 e estourou o limite 9999 em 21/02/2025
# por isso a FEBRABAN reiniciou o fator em 1000 no dia 22/02/2025
DATA_BASE = date(1997, 10, 7)
DATA_REINICIO = date(2025, 2, 22)


def calcular_fator_vencimento(vencimento):
    if vencimento < DATA_BASE:
        raise Exception("Vencimento anterior a data base do fator de vencimento")

    if vencimento < DATA_REINICIO:
        diferenca = vencimento - DATA_BASE
        fator = diferenca.days
    else:
        diferenca = vencimento - DATA_REINICIO
        fator = 1000 + diferenca.days

    if fator > 9999:
        raise Exception("Fator de vencimento passou de 9999 e precisa de nova data base")

    return numerico(fator, 4)


# o codigo de barras tem 44 posicoes:
# 001-003 banco, 004-004 moeda, 005-005 digito geral, 006-009 fator de vencimento,
# 010-019 valor e 020-044 campo livre, que cada banco monta do seu jeito
def gerar_codigo_barras(codigo_banco, valor, vencimento, campo_livre):
    banco = numerico(codigo_banco, 3)
    moeda = "9"
    fator = calcular_fator_vencimento(vencimento)
    valor_texto = valor_cnab(valor, 10)
    livre = numerico(campo_livre, 25)

    # o digito geral e calculado sobre as 43 posicoes, sem ele mesmo
    sem_digito = banco + moeda + fator + valor_texto + livre
    digito_geral = calcular_digito_codigo_barras(sem_digito)

    codigo = banco + moeda + str(digito_geral) + fator + valor_texto + livre

    return codigo
