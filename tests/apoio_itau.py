AGENCIA = "1234"
CONTA = "56789"
CARTEIRA = "109"
CNPJ_EMPRESA = "12.345.678/0001-95"


# monta uma linha de 400 posicoes colocando cada valor na posicao do manual
# recebe uma lista de (posicao_inicial, texto), contando a partir de 1
def montar_linha(pedacos):
    linha = []

    for i in range(400):
        linha.append(" ")

    for posicao_inicial, texto in pedacos:
        indice = posicao_inicial - 1
        for caractere in texto:
            linha[indice] = caractere
            indice = indice + 1

    return "".join(linha)


def montar_header():
    linha = montar_linha([
        (1, "0"),
        (2, "2"),
        (3, "RETORNO"),
        (10, "01"),
        (12, "COBRANCA       "),
        (27, AGENCIA),
        (31, "00"),
        (33, CONTA),
        (38, "7"),
        (47, "MINHA EMPRESA LTDA            "),
        (77, "341"),
        (80, "BANCO ITAU SA  "),
        (95, "100826"),
        (114, "110826"),
        (395, "000001"),
    ])
    return linha


def montar_detalhe(ocorrencia="06", valor_pago="0000000125055", sequencial="000002"):
    linha = montar_linha([
        (1, "1"),
        (2, "02"),
        (4, "12345678000195"),
        (18, AGENCIA),
        (22, "00"),
        (24, CONTA),
        (29, "7"),
        (83, CARTEIRA),
        (86, "12345678"),
        (94, "0"),
        (108, "I"),
        (109, ocorrencia),
        (111, "110826"),
        (117, "NF001     "),
        (127, "12345678"),
        (147, "150926"),
        (153, "0000000125055"),
        (176, "0000000000350"),
        (228, "0000000000000"),
        (241, "0000000000000"),
        (254, valor_pago),
        (267, "0000000000500"),
        (280, "0000000000000"),
        (296, "110826"),
        (325, "JOSE ANTONIO DA SILVA         "),
        (393, "01"),
        (395, sequencial),
    ])
    return linha


def montar_trailer():
    linha = montar_linha([
        (1, "9"),
        (2, "2"),
        (3, "01"),
        (395, "000003"),
    ])
    return linha


def montar_arquivo():
    linhas = []
    linhas.append(montar_header())
    linhas.append(montar_detalhe())
    linhas.append(montar_trailer())
    return "\r\n".join(linhas)
