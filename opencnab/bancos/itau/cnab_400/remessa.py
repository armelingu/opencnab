from opencnab.nucleo.campos import alfa
from opencnab.nucleo.campos import branco
from opencnab.nucleo.campos import numerico
from opencnab.nucleo.campos import zeros
from opencnab.nucleo.datas import data_cnab
from opencnab.bancos.itau.boleto import calcular_dac_conta
from opencnab.bancos.itau.cnab_400.registros import RegistroTipo1Itau
from opencnab.bancos.itau.cnab_400.modelos import BoletoItauCobranca
from opencnab.bancos.itau.cnab_400 import ocorrencias

CODIGO_BANCO = "341"

NOME_BANCO = "BANCO ITAU SA"


# header (registro tipo 0) e a primeira linha do arquivo
class HeaderRemessaItau:

    def __init__(self, agencia, conta, nome_empresa, data_geracao, sequencial_remessa):
        self.agencia = agencia
        self.conta = conta
        self.nome_empresa = nome_empresa
        self.data_geracao = data_geracao
        self.sequencial_remessa = sequencial_remessa

    def gerar(self):
        dac_conta = calcular_dac_conta(self.agencia, self.conta)

        campos = []

        campos.append(numerico("0", 1))                  #001-001 identificacao do registro
        campos.append(numerico("1", 1))                  #002-002 tipo de operacao, 1 = remessa
        campos.append(alfa("REMESSA", 7))                #003-009 literal de remessa
        campos.append(numerico("01", 2))                 #010-011 codigo do servico
        campos.append(alfa("COBRANCA", 15))              #012-026 literal do servico
        campos.append(numerico(self.agencia, 4))         #027-030 agencia da empresa
        campos.append(zeros(2))                          #031-032 complemento de registro
        campos.append(numerico(self.conta, 5))           #033-037 conta da empresa
        campos.append(dac_conta)                         #038-038 digito da agencia com a conta
        campos.append(branco(8))                         #039-046 complemento de registro
        campos.append(alfa(self.nome_empresa, 30))       #047-076 nome da empresa
        campos.append(numerico(CODIGO_BANCO, 3))         #077-079 codigo do banco
        campos.append(alfa(NOME_BANCO, 15))              #080-094 nome do banco
        campos.append(data_cnab(self.data_geracao))      #095-100 data de geracao do arquivo
        campos.append(branco(294))                       #101-394 complemento de registro
        campos.append(numerico(self.sequencial_remessa, 6)) #395-400 sequencial do registro

        linha = "".join(campos)

        if len(linha) != 400:
            raise Exception("Header do Itau saiu com " + str(len(linha)) + " posicoes em vez de 400")

        return linha


# trailer (registro tipo 9) e a ultima linha do arquivo
# sem ele o banco rejeita a remessa inteira
class TrailerRemessaItau:

    def __init__(self, sequencial_registro):
        self.sequencial_registro = sequencial_registro

    def gerar(self):
        campos = []

        campos.append(numerico("9", 1))                       #001-001 identificacao do registro
        campos.append(branco(393))                            #002-394 complemento de registro
        campos.append(numerico(self.sequencial_registro, 6))  #395-400 sequencial do registro

        linha = "".join(campos)

        if len(linha) != 400:
            raise Exception("Trailer do Itau saiu com " + str(len(linha)) + " posicoes em vez de 400")

        return linha


# um comando e um registro sobre titulo que o banco ja conhece, entao vai sem
# os dados do pagador: o manual manda zerar tudo que nao muda e o banco acha o
# titulo pelo nosso numero
# especie e aceite tambem vao zerados e em branco porque so valem no registro
# que cria o titulo
def montar_comando(ocorrencia, nosso_numero, valor, numero_documento="", vencimento=None):
    comando = BoletoItauCobranca(
        numero_documento=numero_documento,
        nosso_numero=nosso_numero,
        valor=valor,
        vencimento=vencimento,
        data_emissao=None,
        nome_pagador="",
        documento_pagador="",
        especie="00",
        aceite="",
        ocorrencia=ocorrencia
    )

    return comando


# monta o arquivo de remessa inteiro
# a ordem e sempre header, um registro tipo 1 por titulo e o trailer
# o sequencial comeca em 1 no header e vai somando ate o trailer
# o mesmo arquivo leva titulos novos e comandos sobre titulos ja registrados
class ArquivoRemessaItau:

    def __init__(self, agencia, conta, carteira, documento_empresa, nome_empresa, data_geracao, sequencial_remessa):
        self.agencia = agencia
        self.conta = conta
        self.carteira = carteira
        self.documento_empresa = documento_empresa
        self.nome_empresa = nome_empresa
        self.data_geracao = data_geracao
        self.sequencial_remessa = sequencial_remessa
        self.boletos = []

    def adicionar_boleto(self, boleto):
        self.boletos.append(boleto)

    # pede ao banco para baixar o titulo, que e como se cancela um boleto ja
    # registrado. o banco para de cobrar e o titulo sai da carteira
    def pedir_baixa(self, nosso_numero, valor, numero_documento=""):
        comando = montar_comando(ocorrencias.PEDIDO_DE_BAIXA, nosso_numero, valor, numero_documento)
        self.boletos.append(comando)

        return comando

    # usado quando o pagador ja pagou direto para a empresa e o boleto no banco
    # precisa ser baixado para nao continuar sendo cobrado
    def baixar_por_pagamento_direto(self, nosso_numero, valor, numero_documento=""):
        comando = montar_comando(ocorrencias.BAIXA_POR_PAGAMENTO_DIRETO, nosso_numero, valor, numero_documento)
        self.boletos.append(comando)

        return comando

    # prorroga o titulo, o caso de quem pede mais prazo para pagar
    def alterar_vencimento(self, nosso_numero, valor, novo_vencimento, numero_documento=""):
        comando = montar_comando(ocorrencias.ALTERACAO_DE_VENCIMENTO, nosso_numero, valor, numero_documento, novo_vencimento)
        self.boletos.append(comando)

        return comando

    # manda protestar um titulo vencido
    # o prazo em dias conta a partir do vencimento; com zero o Itau protesta
    # dois dias corridos depois de vencer
    def mandar_protestar(self, nosso_numero, valor, dias=0, numero_documento=""):
        comando = montar_comando(ocorrencias.PROTESTAR, nosso_numero, valor, numero_documento)
        comando.dias_da_instrucao = dias
        self.boletos.append(comando)

        return comando

    def sustar_protesto(self, nosso_numero, valor, numero_documento=""):
        comando = montar_comando(ocorrencias.SUSTAR_PROTESTO, nosso_numero, valor, numero_documento)
        self.boletos.append(comando)

        return comando

    # abatimento e um desconto concedido depois que o titulo ja foi registrado
    def conceder_abatimento(self, nosso_numero, valor, valor_abatimento, numero_documento=""):
        comando = montar_comando(ocorrencias.CONCESSAO_DE_ABATIMENTO, nosso_numero, valor, numero_documento)
        comando.valor_abatimento = valor_abatimento
        self.boletos.append(comando)

        return comando

    def cancelar_abatimento(self, nosso_numero, valor, valor_abatimento, numero_documento=""):
        comando = montar_comando(ocorrencias.CANCELAMENTO_DE_ABATIMENTO, nosso_numero, valor, numero_documento)
        comando.valor_abatimento = valor_abatimento
        self.boletos.append(comando)

        return comando

    def dispensar_juros(self, nosso_numero, valor, numero_documento=""):
        comando = montar_comando(ocorrencias.DISPENSA_DE_JUROS, nosso_numero, valor, numero_documento)
        self.boletos.append(comando)

        return comando

    def gerar(self):
        if len(self.boletos) == 0:
            raise Exception("Remessa sem boletos")

        linhas = []

        header = HeaderRemessaItau(self.agencia, self.conta, self.nome_empresa, self.data_geracao, self.sequencial_remessa)
        linhas.append(header.gerar())

        sequencial = 1

        for boleto in self.boletos:
            sequencial = sequencial + 1
            registro = RegistroTipo1Itau(self.agencia, self.conta, self.carteira, self.documento_empresa, boleto, sequencial)
            linhas.append(registro.gerar())

        sequencial = sequencial + 1
        trailer = TrailerRemessaItau(sequencial)
        linhas.append(trailer.gerar())

        # o padrao CNAB separa os registros com CRLF
        arquivo = "\r\n".join(linhas)

        return arquivo

    def salvar(self, caminho):
        arquivo = self.gerar()

        destino = open(caminho, "w", encoding="ascii", newline="")
        destino.write(arquivo)
        destino.close()

        return caminho
