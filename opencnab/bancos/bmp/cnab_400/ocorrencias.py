# ocorrencias do arquivo de remessa no layout CNAB 400 derivado do Bradesco
# a ocorrencia diz ao banco o que fazer: registrar um titulo novo ou comandar
# alguma coisa sobre um titulo que ja esta registrado
ENTRADA = "01"
PEDIDO_DE_BAIXA = "02"
PROTESTO_FINS_FALIMENTARES = "03"
CONCESSAO_DE_ABATIMENTO = "04"
CANCELAMENTO_DE_ABATIMENTO = "05"
ALTERACAO_DE_VENCIMENTO = "06"
ALTERACAO_DO_CONTROLE_DO_PARTICIPANTE = "07"
ALTERACAO_DO_NUMERO_DO_DOCUMENTO = "08"
PEDIDO_DE_PROTESTO = "09"
SUSTAR_PROTESTO_E_BAIXAR = "18"
SUSTAR_PROTESTO_E_MANTER = "19"
ALTERACAO_DE_VALOR = "20"
ALTERACAO_DE_OUTROS_DADOS = "31"

DESCRICOES = {
    "01": "Entrada de titulo",
    "02": "Pedido de baixa",
    "03": "Pedido de protesto falimentar",
    "04": "Concessao de abatimento",
    "05": "Cancelamento de abatimento concedido",
    "06": "Alteracao de vencimento",
    "07": "Alteracao do controle do participante",
    "08": "Alteracao do numero do documento",
    "09": "Pedido de protesto",
    "18": "Sustar protesto e baixar titulo",
    "19": "Sustar protesto e manter em carteira",
    "20": "Alteracao de valor",
    "31": "Alteracao de outros dados",
}

# so a entrada registra um titulo novo, o resto e comando sobre titulo que o
# banco ja conhece, e nesses o layout manda zerar os campos que nao mudam
COMANDOS = ["02", "03", "04", "05", "06", "07", "08", "09", "18", "19", "20", "31"]


def descrever_ocorrencia(codigo):
    if codigo in DESCRICOES:
        return DESCRICOES[codigo]

    return "Ocorrencia desconhecida"


def e_comando(codigo):
    if codigo in COMANDOS:
        return True

    return False
