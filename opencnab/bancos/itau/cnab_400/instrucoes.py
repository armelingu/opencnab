# instrucoes de cobranca do Itau (nota 11 do manual de 400 posicoes)
# sao os comandos que a empresa manda junto com o titulo, dizendo ao banco
# o que fazer quando o pagador atrasa
SEM_INSTRUCAO = "00"

PROTESTAR = "09"
NAO_PROTESTAR = "10"
PROTESTAR_DIAS_CORRIDOS = "34"
PROTESTAR_DIAS_UTEIS = "35"
PROTESTO_FINS_FALIMENTARES = "42"
SUJEITO_A_PROTESTO = "43"

DEVOLVER_APOS_05_DIAS = "02"
DEVOLVER_APOS_10_DIAS = "06"
DEVOLVER_APOS_15_DIAS = "07"
DEVOLVER_APOS_20_DIAS = "08"
DEVOLVER_APOS_30_DIAS = "03"
DEVOLVER_APOS_XX_DIAS = "92"

NAO_RECEBER_APOS_05_DIAS = "19"
NAO_RECEBER_APOS_10_DIAS = "20"
NAO_RECEBER_APOS_15_DIAS = "21"
NAO_RECEBER_APOS_30_DIAS = "24"
NAO_RECEBER_APOS_VENCIMENTO = "39"
NAO_RECEBER_APOS_XX_DIAS = "91"

DISPENSAR_JUROS = "47"
CONCEDER_DESCONTO_APOS_VENCIMENTO = "38"
IMPORTANCIA_POR_DIA_DE_ATRASO = "44"

DESCRICOES = {
    "00": "Sem instrucao",
    "02": "Devolver apos 5 dias do vencimento",
    "03": "Devolver apos 30 dias do vencimento",
    "05": "Receber conforme instrucoes no proprio titulo",
    "06": "Devolver apos 10 dias do vencimento",
    "07": "Devolver apos 15 dias do vencimento",
    "08": "Devolver apos 20 dias do vencimento",
    "09": "Protestar",
    "10": "Nao protestar",
    "19": "Nao receber apos 5 dias do vencimento",
    "20": "Nao receber apos 10 dias do vencimento",
    "21": "Nao receber apos 15 dias do vencimento",
    "24": "Nao receber apos 30 dias do vencimento",
    "34": "Protestar apos xx dias corridos do vencimento",
    "35": "Protestar apos xx dias uteis do vencimento",
    "38": "Conceder desconto mesmo apos o vencimento",
    "39": "Nao receber apos o vencimento",
    "42": "Protesto para fins falimentares",
    "43": "Sujeito a protesto se nao for pago no vencimento",
    "44": "Importancia por dia de atraso a partir de uma data",
    "47": "Dispensar juros e comissao de permanencia",
    "91": "Nao receber apos xx dias do vencimento",
    "92": "Devolver apos xx dias do vencimento",
}

# instrucoes marcadas com a observacao (A) do manual: o banco so sabe o que
# fazer se a empresa disser em quantos dias, nas posicoes 392 a 393
INSTRUCOES_QUE_PEDEM_DIAS = ["34", "35", "91", "92"]

# o manual proibe mandar protesto e negativacao no mesmo titulo, e mandar
# protestar junto com nao protestar e uma contradicao que o banco nao resolve
INSTRUCOES_DE_PROTESTO = ["09", "34", "35", "42", "43"]


def descrever_instrucao(codigo):
    if codigo in DESCRICOES:
        return DESCRICOES[codigo]

    return "Instrucao desconhecida"


def pede_quantidade_de_dias(codigo):
    if codigo in INSTRUCOES_QUE_PEDEM_DIAS:
        return True

    return False


def e_instrucao_de_protesto(codigo):
    if codigo in INSTRUCOES_DE_PROTESTO:
        return True

    return False
