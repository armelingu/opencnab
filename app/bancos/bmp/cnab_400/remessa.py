from app.nucleo.campos import alfa
from app.nucleo.campos import branco
from app.nucleo.campos import numerico
from app.nucleo.datas import data_cnab
from app.bancos.bmp.cnab_400.registros import RegistroTipo1BMP

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


# monta o arquivo de remessa inteiro
# a ordem e sempre header, um registro tipo 1 por boleto e o trailer
# o sequencial comeca em 1 no header e vai somando ate o trailer
class ArquivoRemessaBMP:

    def __init__(self, codigo_empresa, nome_empresa, data_geracao, sequencial_remessa):
        self.codigo_empresa = codigo_empresa
        self.nome_empresa = nome_empresa
        self.data_geracao = data_geracao
        self.sequencial_remessa = sequencial_remessa
        self.boletos = []

    def adicionar_boleto(self, boleto):
        self.boletos.append(boleto)

    def gerar(self):
        if len(self.boletos) == 0:
            raise Exception("Remessa sem boletos")

        linhas = []

        header = HeaderRemessaBMP(self.codigo_empresa, self.nome_empresa, self.data_geracao, self.sequencial_remessa)
        linhas.append(header.gerar())

        sequencial = 1

        for boleto in self.boletos:
            sequencial = sequencial + 1
            registro = RegistroTipo1BMP(boleto.numero_documento, boleto.nosso_numero, boleto.valor, boleto.vencimento, boleto.nome_pagador, boleto.documento_pagador, sequencial)
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
