from app.nucleo.campos import alfa
from app.nucleo.campos import branco
from app.nucleo.campos import numerico
from app.nucleo.datas import data_cnab

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
