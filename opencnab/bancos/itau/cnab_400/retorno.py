from decimal import Decimal
from opencnab.nucleo.datas import data_de_cnab
from opencnab.nucleo.valores import valor_de_cnab

# codigos de ocorrencia do retorno do Itau e o que cada um significa
# para quem esta conciliando (nota 17 do manual de cobranca 400 posicoes)
OCORRENCIAS = {
    "02": "Entrada confirmada",
    "03": "Entrada rejeitada",
    "04": "Alteracao de dados, nova entrada",
    "05": "Alteracao de dados, baixa",
    "06": "Liquidacao normal",
    "07": "Liquidacao parcial",
    "08": "Liquidacao em cartorio",
    "09": "Baixa simples",
    "10": "Baixa por ter sido liquidado",
    "11": "Titulo em ser, so no retorno mensal",
    "12": "Abatimento concedido",
    "13": "Abatimento cancelado",
    "14": "Vencimento alterado",
    "15": "Baixa rejeitada",
    "16": "Instrucao rejeitada",
    "17": "Alteracao de dados rejeitada",
    "18": "Cobranca contratual, instrucao rejeitada ou pendente",
    "19": "Confirmacao de instrucao de protesto",
    "20": "Confirmacao de sustacao de protesto",
    "21": "Confirmacao de instrucao de nao protestar",
    "23": "Titulo enviado a cartorio",
    "24": "Instrucao de protesto rejeitada ou sustada",
    "25": "Alegacao do pagador",
    "26": "Tarifa de aviso de cobranca",
    "27": "Tarifa de extrato de posicao",
    "28": "Tarifa de relacao das liquidacoes",
    "29": "Tarifa de manutencao de titulos vencidos",
    "30": "Debito mensal de tarifas",
    "32": "Baixa por ter sido protestado",
    "33": "Custas de protesto",
    "34": "Custas de sustacao",
    "35": "Custas de cartorio distribuidor",
    "36": "Custas de edital",
    "37": "Tarifa de emissao de boleto",
    "38": "Tarifa de instrucao",
    "39": "Tarifa de ocorrencias",
    "40": "Tarifa mensal de emissao de boleto",
    "41": "Debito mensal de tarifas, extrato de posicao",
    "42": "Debito mensal de tarifas, outras instrucoes",
    "43": "Debito mensal de tarifas, manutencao de titulos vencidos",
    "44": "Debito mensal de tarifas, outras ocorrencias",
    "45": "Debito mensal de tarifas, protesto",
    "46": "Debito mensal de tarifas, sustacao de protesto",
    "47": "Baixa com transferencia para desconto",
    "48": "Custas de sustacao judicial",
    "51": "Tarifa mensal de entradas de bancos correspondentes",
    "52": "Tarifa mensal de baixas na carteira",
    "53": "Tarifa mensal de baixas em bancos correspondentes",
    "54": "Tarifa mensal de liquidacoes na carteira",
    "55": "Tarifa mensal de liquidacoes em bancos correspondentes",
    "56": "Custas de irregularidade",
    "57": "Instrucao cancelada",
    "59": "Baixa por credito em conta corrente pelo SISPAG",
    "60": "Entrada rejeitada de carne",
    "61": "Tarifa de emissao de aviso de movimentacao de titulos",
    "62": "Debito mensal de tarifa de aviso de movimentacao de titulos",
    "63": "Titulo sustado judicialmente",
    "64": "Entrada confirmada com rateio de credito",
    "65": "Pagamento com cheque, aguardando compensacao",
    "69": "Cheque devolvido",
    "71": "Entrada registrada, aguardando avaliacao",
    "72": "Baixa por credito pelo SISPAG sem titulo correspondente",
    "73": "Confirmacao de entrada na cobranca simples",
    "76": "Cheque compensado",
}

# ocorrencias que significam dinheiro entrando na conta
# o 07 e liquidacao parcial, entao entra so o valor que o pagador quitou
OCORRENCIAS_DE_PAGAMENTO = ["06", "07", "08", "10", "59", "76"]


def descrever_ocorrencia(codigo):
    if codigo in OCORRENCIAS:
        return OCORRENCIAS[codigo]

    return "Ocorrencia desconhecida"


# na gravacao somos rigorosos, mas na leitura precisamos ser tolerantes
# o Itau manda o campo em branco quando o valor nao se aplica
def valor_do_retorno(texto):
    if texto.strip() == "":
        return Decimal("0.00")

    return valor_de_cnab(texto)


def data_do_retorno(texto):
    if texto.strip() == "":
        return None

    return data_de_cnab(texto)


# cada linha de detalhe do retorno vira um titulo
class TituloRetornoItau:

    def __init__(self, nosso_numero, digito_nosso_numero, carteira, numero_documento, ocorrencia, data_ocorrencia, vencimento, valor_titulo, valor_pago, juros_mora, tarifa, abatimento, desconto, outros_creditos, data_credito, nome_pagador, codigo_liquidacao, sequencial_registro):
        self.nosso_numero = nosso_numero
        self.digito_nosso_numero = digito_nosso_numero
        self.carteira = carteira
        self.numero_documento = numero_documento
        self.ocorrencia = ocorrencia
        self.data_ocorrencia = data_ocorrencia
        self.vencimento = vencimento
        self.valor_titulo = valor_titulo
        self.valor_pago = valor_pago
        self.juros_mora = juros_mora
        self.tarifa = tarifa
        self.abatimento = abatimento
        self.desconto = desconto
        self.outros_creditos = outros_creditos
        self.data_credito = data_credito
        self.nome_pagador = nome_pagador
        self.codigo_liquidacao = codigo_liquidacao
        self.sequencial_registro = sequencial_registro

    def descricao(self):
        return descrever_ocorrencia(self.ocorrencia)

    def foi_pago(self):
        if self.ocorrencia in OCORRENCIAS_DE_PAGAMENTO:
            return True

        return False


# le uma linha de detalhe (registro tipo 1) do arquivo de retorno do Itau
# o nosso numero aparece em tres lugares no layout: 063-070, 086-093 e 127-134
# usamos o de 086-093 porque e o que vem acompanhado do digito verificador
def ler_titulo(linha):
    if len(linha) != 400:
        raise Exception("Linha de retorno precisa ter 400 posicoes")

    carteira = linha[82:85]                        #083-085 numero da carteira
    nosso_numero = linha[85:93]                    #086-093 nosso numero
    digito_nosso_numero = linha[93:94]             #094-094 digito do nosso numero
    ocorrencia = linha[108:110]                    #109-110 codigo da ocorrencia
    data_ocorrencia = linha[110:116]               #111-116 data da ocorrencia
    numero_documento = linha[116:126]              #117-126 numero do documento
    vencimento = linha[146:152]                    #147-152 data de vencimento
    valor_titulo = linha[152:165]                  #153-165 valor do titulo
    tarifa = linha[175:188]                        #176-188 tarifa de cobranca
    abatimento = linha[227:240]                    #228-240 abatimento concedido
    desconto = linha[240:253]                      #241-253 desconto concedido
    valor_pago = linha[253:266]                    #254-266 valor lancado em conta
    juros_mora = linha[266:279]                    #267-279 juros de mora e multa
    outros_creditos = linha[279:292]               #280-292 outros creditos
    data_credito = linha[295:301]                  #296-301 data do credito
    nome_pagador = linha[324:354]                  #325-354 nome do pagador
    codigo_liquidacao = linha[392:394]             #393-394 meio pelo qual foi liquidado
    sequencial_registro = linha[394:400]           #395-400 sequencial do registro

    titulo = TituloRetornoItau(
        nosso_numero,
        digito_nosso_numero,
        carteira,
        numero_documento.strip(),
        ocorrencia,
        data_do_retorno(data_ocorrencia),
        data_do_retorno(vencimento),
        valor_do_retorno(valor_titulo),
        valor_do_retorno(valor_pago),
        valor_do_retorno(juros_mora),
        valor_do_retorno(tarifa),
        valor_do_retorno(abatimento),
        valor_do_retorno(desconto),
        valor_do_retorno(outros_creditos),
        data_do_retorno(data_credito),
        nome_pagador.strip(),
        codigo_liquidacao,
        sequencial_registro
    )

    return titulo


# le o arquivo de retorno inteiro
# o header traz os dados da empresa e cada registro tipo 1 vira um titulo
class ArquivoRetornoItau:

    def __init__(self, texto):
        self.texto = texto
        self.agencia = ""
        self.conta = ""
        self.nome_empresa = ""
        self.codigo_banco = ""
        self.data_geracao = None
        self.data_credito = None
        self.titulos = []

    def ler(self):
        linhas = self.texto.splitlines()

        for linha in linhas:
            if len(linha) == 0:
                continue

            tipo_registro = linha[0:1]

            if tipo_registro == "0":
                self.ler_header(linha)

            if tipo_registro == "1":
                self.titulos.append(ler_titulo(linha))

        return self.titulos

    def ler_header(self, linha):
        if len(linha) != 400:
            raise Exception("Header de retorno precisa ter 400 posicoes")

        if linha[1:2] != "2":
            raise Exception("Arquivo nao e um retorno")

        self.agencia = linha[26:30]                          #027-030 agencia da empresa
        self.conta = linha[32:37]                            #033-037 conta da empresa
        self.nome_empresa = linha[46:76].strip()             #047-076 nome da empresa
        self.codigo_banco = linha[76:79]                     #077-079 codigo do banco
        self.data_geracao = data_do_retorno(linha[94:100])   #095-100 data de geracao
        self.data_credito = data_do_retorno(linha[113:119])  #114-119 data do credito

    def total_pago(self):
        total = Decimal("0.00")

        for titulo in self.titulos:
            if titulo.foi_pago():
                total = total + titulo.valor_pago

        return total

    def pagos(self):
        lista = []

        for titulo in self.titulos:
            if titulo.foi_pago():
                lista.append(titulo)

        return lista


# abre o arquivo de retorno do disco e ja faz a leitura
# usamos latin-1 porque o banco ainda manda acento em nome de pagador
def ler_arquivo_retorno(caminho):
    origem = open(caminho, "r", encoding="latin-1", newline="")
    texto = origem.read()
    origem.close()

    arquivo = ArquivoRetornoItau(texto)
    arquivo.ler()

    return arquivo
