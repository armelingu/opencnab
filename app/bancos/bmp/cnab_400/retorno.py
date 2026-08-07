from decimal import Decimal
from app.nucleo.datas import data_de_cnab
from app.nucleo.valores import valor_de_cnab

# codigos de ocorrencia que o banco manda no retorno
# e o que cada um significa para quem esta conciliando
OCORRENCIAS = {
    "02": "Entrada confirmada",
    "03": "Entrada rejeitada",
    "06": "Liquidacao normal",
    "09": "Baixa automatica",
    "10": "Baixa por ter sido liquidado",
    "11": "Titulo em carteira",
    "12": "Abatimento concedido",
    "13": "Abatimento cancelado",
    "14": "Vencimento alterado",
    "15": "Liquidacao em cartorio",
    "16": "Titulo pago em cheque",
    "17": "Liquidacao apos baixa",
    "19": "Confirmacao de instrucao de protesto",
    "20": "Confirmacao de sustacao de protesto",
    "23": "Titulo enviado a cartorio",
    "24": "Instrucao de protesto rejeitada",
    "25": "Protestado e baixado",
    "26": "Instrucao rejeitada",
    "27": "Alteracao de dados confirmada",
    "28": "Debito de tarifas e custas",
    "30": "Alteracao de dados rejeitada",
}

# ocorrencias que significam dinheiro entrando na conta
OCORRENCIAS_DE_PAGAMENTO = ["06", "15", "16", "17"]


def descrever_ocorrencia(codigo):
    if codigo in OCORRENCIAS:
        return OCORRENCIAS[codigo]

    return "Ocorrencia desconhecida"


# na gravacao somos rigorosos, mas na leitura precisamos ser tolerantes
# alguns bancos mandam o campo em branco quando o valor nao se aplica
def valor_do_retorno(texto):
    if texto.strip() == "":
        return Decimal("0.00")

    return valor_de_cnab(texto)


def data_do_retorno(texto):
    if texto.strip() == "":
        return None

    return data_de_cnab(texto)


# cada linha de detalhe do retorno vira um titulo
class TituloRetorno:

    def __init__(self, nosso_numero, numero_documento, ocorrencia, data_ocorrencia, vencimento, valor_titulo, valor_pago, juros_mora, despesas, data_credito, sequencial_registro):
        self.nosso_numero = nosso_numero
        self.numero_documento = numero_documento
        self.ocorrencia = ocorrencia
        self.data_ocorrencia = data_ocorrencia
        self.vencimento = vencimento
        self.valor_titulo = valor_titulo
        self.valor_pago = valor_pago
        self.juros_mora = juros_mora
        self.despesas = despesas
        self.data_credito = data_credito
        self.sequencial_registro = sequencial_registro

    def descricao(self):
        return descrever_ocorrencia(self.ocorrencia)

    def foi_pago(self):
        if self.ocorrencia in OCORRENCIAS_DE_PAGAMENTO:
            return True

        return False


# le uma linha de detalhe (registro tipo 1) do arquivo de retorno
# as posicoes seguem o mesmo layout CNAB 400 usado na remessa
def ler_titulo(linha):
    if len(linha) != 400:
        raise Exception("Linha de retorno precisa ter 400 posicoes")

    nosso_numero = linha[70:81]                    #071-081 nosso numero
    ocorrencia = linha[108:110]                    #109-110 codigo da ocorrencia
    data_ocorrencia = linha[110:116]               #111-116 data da ocorrencia
    numero_documento = linha[116:126]              #117-126 numero do documento
    vencimento = linha[146:152]                    #147-152 data de vencimento
    valor_titulo = linha[152:165]                  #153-165 valor do titulo
    despesas = linha[174:187]                      #175-187 despesas de cobranca
    valor_pago = linha[252:265]                    #253-265 valor pago
    juros_mora = linha[265:278]                    #266-278 juros de mora
    data_credito = linha[295:301]                  #296-301 data do credito
    sequencial_registro = linha[394:400]           #395-400 sequencial do registro

    titulo = TituloRetorno(
        nosso_numero,
        numero_documento.strip(),
        ocorrencia,
        data_do_retorno(data_ocorrencia),
        data_do_retorno(vencimento),
        valor_do_retorno(valor_titulo),
        valor_do_retorno(valor_pago),
        valor_do_retorno(juros_mora),
        valor_do_retorno(despesas),
        data_do_retorno(data_credito),
        sequencial_registro
    )

    return titulo


# le o arquivo de retorno inteiro
# o header traz os dados da empresa e cada registro tipo 1 vira um titulo
class ArquivoRetornoBMP:

    def __init__(self, texto):
        self.texto = texto
        self.codigo_empresa = ""
        self.nome_empresa = ""
        self.codigo_banco = ""
        self.data_geracao = None
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

        self.codigo_empresa = linha[26:46].strip()          #027-046 codigo da empresa
        self.nome_empresa = linha[46:76].strip()            #047-076 nome da empresa
        self.codigo_banco = linha[76:79]                    #077-079 codigo do banco
        self.data_geracao = data_do_retorno(linha[94:100])  #095-100 data de geracao

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
# usamos latin-1 porque alguns bancos ainda mandam acento no retorno
def ler_arquivo_retorno(caminho):
    origem = open(caminho, "r", encoding="latin-1", newline="")
    texto = origem.read()
    origem.close()

    arquivo = ArquivoRetornoBMP(texto)
    arquivo.ler()

    return arquivo
