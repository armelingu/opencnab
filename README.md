# OpenCNAB

**Biblioteca Python open source para gerar e ler arquivos CNAB 400 e CNAB 240 de cobrança bancária.**

Crie arquivos de remessa de boletos para o seu banco em poucas linhas de Python,
sem depender de serviço pago, sem taxa por boleto e sem ficar preso à API
proprietária de um único banco.

*Python library for Brazilian bank exchange files (CNAB / FEBRABAN) used for
boleto registration and payment reconciliation.*

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Licença](https://img.shields.io/badge/licen%C3%A7a-MIT-green)
![Testes](https://img.shields.io/badge/testes-103%20passando-brightgreen)

---

## Por que este projeto existe

Toda empresa brasileira que emite boleto registrado precisa trocar arquivos CNAB
com o banco: um arquivo de **remessa** para registrar os títulos e um arquivo de
**retorno** para saber quem pagou.

Na prática, quem precisa fazer isso hoje tem três caminhos ruins: usar uma
biblioteca antiga e sem manutenção, pagar por boleto emitido, ou integrar a API
proprietária de cada banco e ficar refém dela. O OpenCNAB existe para ser a
quarta opção: código aberto, sem custo por boleto e com o mesmo modelo de uso
para qualquer banco.

## Instalação

Requer Python 3.11 ou superior.

```bash
git clone https://github.com/armelingu/opencnab.git
cd opencnab
pip install .
```

Para desenvolver:

```bash
pip install -e ".[dev]"
```

## Começando

Gerar um arquivo de remessa completo, pronto para enviar ao banco:

```python
from datetime import date
from opencnab.bancos.bmp.cnab_400.remessa import ArquivoRemessaBMP
from opencnab.bancos.bmp.cnab_400.modelos import BoletoBMP

remessa = ArquivoRemessaBMP(
    codigo_empresa="123",
    nome_empresa="MINHA EMPRESA LTDA",
    data_geracao=date(2026, 6, 5),
    sequencial_remessa=1
)

remessa.adicionar_boleto(BoletoBMP(
    numero_documento="NF001",
    nosso_numero="1",
    valor=150.70,
    vencimento=date(2026, 6, 30),
    nome_pagador="José Antônio da Conceição",
    documento_pagador="123.456.789-01"
))

remessa.adicionar_boleto(BoletoBMP(
    numero_documento="NF002",
    nosso_numero="2",
    valor=2500.00,
    vencimento=date(2026, 7, 15),
    nome_pagador="Padaria São João Ltda",
    documento_pagador="12.345.678/0001-99"
))

remessa.salvar("remessa.rem")
```

A biblioteca cuida dos detalhes que costumam gerar rejeição no banco: monta o
cabeçalho e o trailer, numera o sequencial de cada linha, identifica
automaticamente se o pagador é CPF ou CNPJ, remove acentos dos nomes, formata
datas e valores no padrão CNAB e garante que toda linha tenha exatamente 400
posições.

## Lendo o retorno do banco

O retorno é o arquivo que o banco devolve informando o que aconteceu com cada
título. É com ele que você dá baixa automática no contas a receber:

```python
from opencnab.bancos.bmp.cnab_400.retorno import ler_arquivo_retorno

retorno = ler_arquivo_retorno("retorno.ret")

for titulo in retorno.pagos():
    print(titulo.nosso_numero, titulo.numero_documento, titulo.valor_pago)

print("Total creditado:", retorno.total_pago())
```

Cada título traz o código de ocorrência já traduzido, o valor originalmente
cobrado, o valor efetivamente pago, juros, despesas e a data do crédito em
conta:

```python
for titulo in retorno.titulos:
    print(titulo.ocorrencia, titulo.descricao(), titulo.foi_pago())

# 06 Liquidacao normal True
# 02 Entrada confirmada False
```

Valores monetários voltam como `Decimal`, então você pode somar e comparar sem
risco de erro de arredondamento.

## Gerando o código de barras e a linha digitável

O que o cliente enxerga no boleto: o código de barras que o caixa lê e a linha
digitável que ele digita quando o leitor falha.

```python
from datetime import date
from opencnab.boletos.codigo_barras import gerar_codigo_barras
from opencnab.boletos.linha_digitavel import gerar_linha_digitavel
from opencnab.boletos.linha_digitavel import formatar_linha_digitavel

codigo = gerar_codigo_barras(
    codigo_banco="274",
    valor=150.70,
    vencimento=date(2026, 6, 30),
    campo_livre="1234567890123456789012345"
)

linha = gerar_linha_digitavel(codigo)

print(codigo)                          # 44 posições
print(formatar_linha_digitavel(linha)) # 27491.23457 67890.123457 ...
```

O cálculo do fator de vencimento já contempla o reinício definido pela FEBRABAN:
a contagem iniciada em 07/10/1997 atingiu o limite de 9999 em 21/02/2025, e a
partir de 22/02/2025 o fator voltou a 1000. Boletos com vencimento antes e
depois dessa virada são calculados corretamente.

O campo livre são as 25 posições que cada banco define do seu jeito, geralmente
combinando carteira, nosso número, agência e conta.

## Recursos

- Arquivo de remessa completo em CNAB 400 (cabeçalho, títulos e trailer)
- Leitura do arquivo de retorno, com códigos de ocorrência traduzidos
- Código de barras de 44 posições e linha digitável de 47, no padrão FEBRABAN
- Fator de vencimento com suporte aos dois ciclos (antes e depois de 22/02/2025)
- Separação automática dos títulos liquidados, para baixa no contas a receber
- Valores monetários com `Decimal`, sem perder centavos por arredondamento
- Identificação automática de CPF e CNPJ do pagador
- Campos alfanuméricos limpos e garantidos em ASCII, como o banco exige
- Geração de "nosso número" com dígito verificador
- Cálculo de dígito verificador nos módulos 10 e 11
- Formatação de campos, datas e valores no padrão CNAB

## Bancos e layouts suportados

| Banco | Código | Layout | Remessa | Retorno |
|---|---|---|---|---|
| BMP Money Plus | 274 | CNAB 400 | Sim | Sim |

O layout CNAB 400 usado segue o padrão de mercado derivado do Bradesco (CBR643),
que é adotado por vários bancos médios. Isso facilita adicionar novos bancos:
na maioria dos casos muda pouca coisa além do código e do nome do banco.

## Roadmap

- [x] Remessa CNAB 400 para BMP
- [x] Leitura do arquivo de retorno, para baixa automática de contas a receber
- [x] Código de barras e linha digitável do boleto
- [ ] Publicação no PyPI (`pip install opencnab`)
- [ ] Suporte a CNAB 240
- [ ] Novos bancos: Bradesco, Itaú, Santander, Banco do Brasil, Caixa, Sicoob, Inter

## Testes

```bash
pytest
```

## Como contribuir

Contribuições são bem-vindas, principalmente layouts de bancos que você já usa
em produção.

O projeto usa `main` como branch estável e `develop` como base do
desenvolvimento. Crie sua branch a partir de `develop` no formato
`tipo/escopo-descricao`, por exemplo `feat/itau-remessa-cnab400` ou
`fix/nucleo-valor-cnab-decimal`. Os tipos são `feat`, `fix`, `refactor`, `test`,
`docs` e `hotfix`, e as mensagens de commit usam o mesmo prefixo.

Toda alteração de comportamento deve vir com teste, e a suíte precisa passar
inteira antes do merge.

## Pontos ainda em aberto

Vale conhecer os limites atuais antes de colocar em produção:

- As posições do CNAB 400 seguem o layout de mercado derivado do Bradesco
  (CBR643), que o cabeçalho do BMP reproduz. Convém conferir contra o manual
  oficial do seu banco antes do primeiro envio.
- O campo livre do código de barras precisa ser montado por você, porque cada
  banco define as 25 posições de um jeito. Ainda não há função pronta por banco.
- O dígito do "nosso número" usa a regra que devolve `0`; alguns bancos usam a
  letra `P` em um dos casos.
- Ao ler o retorno, confira o total recebido contra o extrato na primeira vez,
  para garantir que as posições batem com o arquivo do seu banco.

## Glossário rápido

- **CNAB**: padrão de arquivo texto de posição fixa usado na troca de informações
  entre empresas e bancos, definido pela FEBRABAN.
- **Remessa**: arquivo que a empresa envia ao banco para registrar boletos.
- **Retorno**: arquivo que o banco devolve informando pagamentos e ocorrências.
- **Nosso número**: identificador do título no banco, definido pela empresa.
- **Pagador**: quem deve pagar o boleto (antigamente chamado de sacado).

## Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE).
