from opencnab.nucleo.campos import alfa
from opencnab.nucleo.campos import branco
from opencnab.nucleo.campos import numerico
from opencnab.nucleo.datas import data_cnab
from opencnab.bancos.bmp.cnab_400.registros import RegistroTipo1BMP
from opencnab.bancos.bmp.cnab_400.modelos import BoletoBMP
from opencnab.bancos.bmp.cnab_400 import ocorrencias

class HeaderRemessaBMP:

    def __init__(self, codigo_empresa, nome_empresa, data_geracao, sequencial_remessa):
        self.codigo_empresa = codigo_empresa
        self.nome_empresa = nome_empresa
        self.data_geracao = data_geracao
        self.sequencial_remessa = sequencial_remessa

    def gerar(self):
        campos = []

        campos.append(numerico("0", 1))
        campos.append(numerico("1", 1))
        campos.append(alfa("REMESSA", 7))
        campos.append(numerico("01", 2))
        campos.append(alfa("COBRANCA", 15))

        campos.append(numerico(self.codigo_empresa, 20))
        campos.append(alfa(self.nome_empresa, 30))
        campos.append(numerico("274", 3))
        campos.append(alfa("BMP MONEY PLUS", 15))
        campos.append(data_cnab(self.data_geracao))
        campos.append(branco(8))
        campos.append(alfa("MX", 2))
        campos.append(numerico(self.sequencial_remessa, 7))
        campos.append(branco(277))
        campos.append(numerico("1", 6))

        linha = "".join(campos)
        return linha


# trailer (registro tipo 9) e a ultima linha do arquivo
# sem ele o banco rejeita a remessa inteira
class TrailerRemessaBMP:

    def __init__(self, sequencial_registro):
        self.sequencial_registro = sequencial_registro

    def gerar(self):
        campos = []

        campos.append(numerico("9", 1))                              #001-001 identificacao do registro
        campos.append(branco(393))                                   #002-394 uso do banco
        campos.append(numerico(self.sequencial_registro, 6))         #395-400 sequencial do registro

        linha = "".join(campos)
        return linha


# um comando e um registro sobre titulo que o banco ja conhece, entao vai sem
# os dados do pagador: o manual manda zerar tudo que nao muda e o banco acha o
# titulo pelo nosso numero
# especie e aceite tambem vao zerados e em branco porque so valem no registro
# que cria o titulo
def montar_comando(ocorrencia, nosso_numero, valor, numero_documento="", vencimento=None):
    comando = BoletoBMP(
        numero_documento=numero_documento,
        nosso_numero=nosso_numero,
        valor=valor,
        vencimento=vencimento,
        nome_pagador="",
        documento_pagador="",
        especie="0",
        aceite="",
        condicao_emissao="",
        debito_automatico="",
        ocorrencia=ocorrencia
    )

    return comando


# monta o arquivo de remessa inteiro
# a ordem e sempre header, um registro tipo 1 por titulo e o trailer
# o sequencial comeca em 1 no header e vai somando ate o trailer
# o mesmo arquivo leva titulos novos e comandos sobre titulos ja registrados
class ArquivoRemessaBMP:

    def __init__(self, codigo_empresa, nome_empresa, data_geracao, sequencial_remessa):
        self.codigo_empresa = codigo_empresa
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

    # prorroga o titulo, o caso de quem pede mais prazo para pagar
    def alterar_vencimento(self, nosso_numero, valor, novo_vencimento, numero_documento=""):
        comando = montar_comando(ocorrencias.ALTERACAO_DE_VENCIMENTO, nosso_numero, valor, numero_documento, novo_vencimento)
        self.boletos.append(comando)

        return comando

    def alterar_valor(self, nosso_numero, novo_valor, numero_documento=""):
        comando = montar_comando(ocorrencias.ALTERACAO_DE_VALOR, nosso_numero, novo_valor, numero_documento)
        self.boletos.append(comando)

        return comando

    def mandar_protestar(self, nosso_numero, valor, numero_documento=""):
        comando = montar_comando(ocorrencias.PEDIDO_DE_PROTESTO, nosso_numero, valor, numero_documento)
        self.boletos.append(comando)

        return comando

    # o layout separa sustar o protesto e baixar o titulo de sustar e continuar
    # cobrando, entao sao dois comandos diferentes
    def sustar_protesto_e_baixar(self, nosso_numero, valor, numero_documento=""):
        comando = montar_comando(ocorrencias.SUSTAR_PROTESTO_E_BAIXAR, nosso_numero, valor, numero_documento)
        self.boletos.append(comando)

        return comando

    def sustar_protesto_e_manter(self, nosso_numero, valor, numero_documento=""):
        comando = montar_comando(ocorrencias.SUSTAR_PROTESTO_E_MANTER, nosso_numero, valor, numero_documento)
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

    def gerar(self):
        if len(self.boletos) == 0:
            raise Exception("Remessa sem boletos")

        linhas = []

        header = HeaderRemessaBMP(self.codigo_empresa, self.nome_empresa, self.data_geracao, self.sequencial_remessa)
        linhas.append(header.gerar())

        sequencial = 1

        for boleto in self.boletos:
            sequencial = sequencial + 1
            registro = RegistroTipo1BMP(boleto, sequencial)
            linhas.append(registro.gerar())

        sequencial = sequencial + 1
        trailer = TrailerRemessaBMP(sequencial)
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
