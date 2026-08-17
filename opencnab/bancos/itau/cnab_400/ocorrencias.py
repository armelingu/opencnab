# ocorrencias do arquivo de remessa do Itau (nota 6 do manual de 400 posicoes)
# a ocorrencia diz ao banco o que fazer: registrar um titulo novo ou comandar
# alguma coisa sobre um titulo que ja esta registrado
ENTRADA = "01"
PEDIDO_DE_BAIXA = "02"
CONCESSAO_DE_ABATIMENTO = "04"
CANCELAMENTO_DE_ABATIMENTO = "05"
ALTERACAO_DE_VENCIMENTO = "06"
ALTERACAO_DO_USO_DA_EMPRESA = "07"
PROTESTAR = "09"
NAO_PROTESTAR = "10"
PROTESTO_FINS_FALIMENTARES = "11"
SUSTAR_PROTESTO = "18"
ALTERACAO_DE_OUTROS_DADOS = "31"
BAIXA_POR_PAGAMENTO_DIRETO = "34"
CANCELAMENTO_DE_INSTRUCAO = "35"
ALTERAR_VENCIMENTO_E_SUSTAR_PROTESTO = "37"
DISPENSA_DE_JUROS = "47"

DESCRICOES = {
    "01": "Entrada de titulo",
    "02": "Pedido de baixa",
    "04": "Concessao de abatimento",
    "05": "Cancelamento de abatimento",
    "06": "Alteracao de vencimento",
    "07": "Alteracao do uso da empresa",
    "09": "Protestar",
    "10": "Nao protestar",
    "11": "Protesto para fins falimentares",
    "18": "Sustar o protesto",
    "31": "Alteracao de outros dados",
    "34": "Baixa por ter sido pago diretamente ao beneficiario",
    "35": "Cancelamento de instrucao",
    "37": "Alteracao de vencimento e sustacao do protesto",
    "47": "Beneficiario solicita dispensa de juros",
}

# so a entrada registra um titulo novo, o resto e comando sobre titulo que o
# banco ja conhece, e nesses o layout manda zerar os campos que nao mudam
COMANDOS = ["02", "04", "05", "06", "07", "09", "10", "11", "18", "31", "34", "35", "37", "47"]


def descrever_ocorrencia(codigo):
    if codigo in DESCRICOES:
        return DESCRICOES[codigo]

    return "Ocorrencia desconhecida"


def e_comando(codigo):
    if codigo in COMANDOS:
        return True

    return False
