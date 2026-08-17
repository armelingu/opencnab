# OpenCNAB

**Biblioteca Python open source para gerar e ler arquivos CNAB 400 e CNAB 240 de cobrança bancária.**

Crie arquivos de remessa de boletos para o seu banco em poucas linhas de Python,
sem depender de serviço pago, sem taxa por boleto e sem ficar preso à API
proprietária de um único banco.

*Python library for Brazilian bank exchange files (CNAB / FEBRABAN) used for
boleto registration and payment reconciliation.*

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Licença](https://img.shields.io/badge/licen%C3%A7a-MIT-green)
![Testes](https://img.shields.io/badge/testes-249%20passando-brightgreen)
![Dependências](https://img.shields.io/badge/depend%C3%AAncias-nenhuma-lightgrey)

---

> ### Atenção para quem já usa o BMP: a remessa mudou na 0.8.0
>
> O registro de detalhe do BMP gravava os campos **uma posição à frente** do que
> o layout CNAB 400 define, a partir da posição 083. A ocorrência ia em 110-111
> em vez de 109-110, e o mesmo deslocamento atingia número do documento,
> vencimento, valor, tipo de inscrição, CPF/CNPJ e nome do pagador.
>
> A partir da `0.8.0` o registro segue o manual, conferido campo a campo nos
> testes. Se você gerava remessa com uma versão anterior e o banco aceitava,
> **confirme com ele antes de enviar o primeiro arquivo novo**, porque o
> conteúdo das linhas mudou.
>
> Na mesma versão, `BoletoBMP` ganhou campos opcionais (espécie, aceite, data de
> emissão, endereço do pagador, entre outros) e `RegistroTipo1BMP` passou a
> receber o boleto inteiro em vez de campo a campo. Quem usava
> `ArquivoRemessaBMP` não precisa mudar nada.

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

Requer Python 3.11 ou superior e nada mais: a biblioteca usa só a biblioteca
padrão do Python, então instalar não arrasta nenhuma dependência para o seu
projeto.

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
from opencnab import ArquivoRemessaBMP
from opencnab import BoletoBMP

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

Para mexer em um boleto que já foi registrado, use os comandos da remessa. O
banco encontra o título pelo **nosso número**:

```python
remessa.pedir_baixa(nosso_numero="2", valor=500.00)
remessa.alterar_vencimento(nosso_numero="3", valor=800.00, novo_vencimento=date(2026, 10, 30))
remessa.alterar_valor(nosso_numero="3", novo_valor=999.99)
remessa.mandar_protestar(nosso_numero="4", valor=990.00)
remessa.sustar_protesto_e_baixar(nosso_numero="4", valor=990.00)
remessa.sustar_protesto_e_manter(nosso_numero="4", valor=990.00)
remessa.conceder_abatimento(nosso_numero="5", valor=700.00, valor_abatimento=70.00)
remessa.cancelar_abatimento(nosso_numero="5", valor=700.00, valor_abatimento=70.00)
```

## Lendo o retorno do banco

O retorno é o arquivo que o banco devolve informando o que aconteceu com cada
título. É com ele que você dá baixa automática no contas a receber:

```python
from opencnab import ler_retorno_bmp

retorno = ler_retorno_bmp("retorno.ret")

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

## Trocando de banco: Itaú

Cada banco tem sua própria classe, mas o modo de usar é o mesmo. No Itaú a conta
e a carteira entram no arquivo, e o dígito verificador da conta é calculado
automaticamente:

```python
from datetime import date
from opencnab import ArquivoRemessaItau
from opencnab import BoletoItauCobranca

remessa = ArquivoRemessaItau(
    agencia="1234",
    conta="56789",
    carteira="109",
    documento_empresa="12.345.678/0001-95",
    nome_empresa="MINHA EMPRESA LTDA",
    data_geracao=date(2026, 8, 10),
    sequencial_remessa=1
)

remessa.adicionar_boleto(BoletoItauCobranca(
    numero_documento="NF001",
    nosso_numero="12345678",
    valor=1250.55,
    vencimento=date(2026, 9, 15),
    data_emissao=date(2026, 8, 10),
    nome_pagador="José Antônio da Silva",
    documento_pagador="123.456.789-01"
))

remessa.salvar("remessa.rem")
```

A leitura do retorno segue a mesma interface do BMP, com a tabela de ocorrências
do Itaú já traduzida:

```python
from opencnab import ler_retorno_itau

retorno = ler_retorno_itau("retorno.ret")

for titulo in retorno.pagos():
    print(titulo.nosso_numero, titulo.valor_pago, titulo.data_credito)
```

O layout do Itaú segue o manual oficial de cobrança em 400 posições. Vale saber
que o nosso número aparece em três posições diferentes do arquivo de retorno; a
biblioteca lê a que vem acompanhada do dígito verificador.

### Instruções, juros, desconto e endereço

O exemplo acima registra a cobrança do jeito mais simples. Quando você precisa
mandar o banco protestar, cobrar juros de atraso ou conceder desconto, é só
preencher os campos opcionais do título:

```python
from datetime import date
from opencnab import BoletoItauCobranca
from opencnab import EnderecoPagador
from opencnab.bancos.itau.cnab_400 import instrucoes

boleto = BoletoItauCobranca(
    numero_documento="NF001",
    nosso_numero="12345678",
    valor=1250.55,
    vencimento=date(2026, 9, 15),
    data_emissao=date(2026, 8, 10),
    nome_pagador="José Antônio da Silva",
    documento_pagador="123.456.789-01",

    endereco_pagador=EnderecoPagador(
        logradouro="Rua das Flores, 123",
        bairro="Centro",
        cep="01310-100",
        cidade="São Paulo",
        uf="SP"
    ),

    juros_por_dia=0.42,
    data_mora=date(2026, 9, 16),

    valor_desconto=50.00,
    desconto_ate=date(2026, 9, 10),

    instrucao_1=instrucoes.PROTESTAR_DIAS_CORRIDOS,
    dias_da_instrucao=15
)
```

As instruções têm nome em vez de código solto, então você escreve
`instrucoes.PROTESTAR_DIAS_CORRIDOS` e não `"34"`. A lista completa está em
`opencnab/bancos/itau/cnab_400/instrucoes.py`.

Vale preencher o endereço mesmo sendo opcional: **é pelo CEP do pagador que o
Itaú decide qual agência vai cobrar o título**, e é esse endereço que sai
impresso no boleto.

A biblioteca recusa três combinações que o banco rejeitaria ou entenderia
errado: instrução com prazo sem informar a quantidade de dias, protestar e não
protestar no mesmo título, e desconto sem a data limite para concedê-lo.

### Cancelando, prorrogando e protestando

Registrar o boleto é só o começo. Depois vem o cliente que pede mais prazo, a
nota emitida errada que precisa ser cancelada e o título que venceu e não foi
pago. Tudo isso é comandado pelo mesmo arquivo de remessa, mudando a ocorrência
do registro.

O banco encontra o título pelo **nosso número**, então é só ele e o valor que
você precisa informar:

```python
remessa = ArquivoRemessaItau(...)

# cancelar um boleto: o banco baixa o título e para de cobrar
remessa.pedir_baixa(nosso_numero="11111111", valor=500.00)

# o cliente pagou direto na sua conta, então o boleto no banco não faz mais sentido
remessa.baixar_por_pagamento_direto(nosso_numero="22222222", valor=800.00)

# prorrogar para quem pediu mais prazo
remessa.alterar_vencimento(
    nosso_numero="33333333",
    valor=990.00,
    novo_vencimento=date(2026, 10, 30)
)

# protestar 10 dias depois do vencimento, e sustar o protesto se ele pagar
remessa.mandar_protestar(nosso_numero="44444444", valor=700.00, dias=10)
remessa.sustar_protesto(nosso_numero="44444444", valor=700.00)

# conceder um desconto depois que o título já foi registrado
remessa.conceder_abatimento(nosso_numero="55555555", valor=300.00, valor_abatimento=30.00)
remessa.dispensar_juros(nosso_numero="55555555", valor=300.00)

remessa.salvar("remessa.rem")
```

Títulos novos e comandos convivem no mesmo arquivo, na ordem em que você os
adiciona. Os códigos de ocorrência ficam em
`opencnab/bancos/itau/cnab_400/ocorrencias.py`.

Duas observações do manual que valem lembrar: no protesto, `dias=0` faz o Itaú
protestar dois dias corridos após o vencimento; e um comando só é aceito antes
de o protesto começar — se já estiver em andamento, suste primeiro e comande
depois, o que pode ir no mesmo arquivo.

## Gerando o código de barras e a linha digitável

O que o cliente enxerga no boleto: o código de barras que o caixa lê e a linha
digitável que ele digita quando o leitor falha.

```python
from datetime import date
from opencnab import gerar_codigo_barras
from opencnab import gerar_linha_digitavel
from opencnab import formatar_linha_digitavel

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

Para os bancos já implementados você não precisa montar o campo livre na mão:

```python
from datetime import date
from opencnab import BoletoItau

boleto = BoletoItau(
    agencia="1234",
    conta="56789",
    carteira="109",
    nosso_numero="12345678",
    valor=1250.55,
    vencimento=date(2026, 9, 15)
)

print(boleto.gerar_codigo_barras())
print(boleto.gerar_linha_digitavel_formatada())
```

O Itaú calcula dois dígitos verificadores próprios dentro do campo livre: um para
o nosso número e outro para a conta, ambos em módulo 10. A biblioteca cuida disso.

## Recursos

- Arquivo de remessa completo em CNAB 400 (cabeçalho, títulos e trailer)
- Leitura do arquivo de retorno, com códigos de ocorrência traduzidos
- Código de barras de 44 posições e linha digitável de 47, no padrão FEBRABAN
- Campo livre do boleto do Itaú, com os dois dígitos verificadores que ele exige
- Remessa e retorno do Itaú conforme o manual oficial de 400 posições
- Instruções de protesto, juros de atraso, desconto e abatimento no Itaú
- Baixa, prorrogação, protesto e abatimento de títulos já registrados, nos dois bancos
- Endereço do pagador, usado pelo Itaú para definir a agência cobradora
- Fator de vencimento com suporte aos dois ciclos (antes e depois de 22/02/2025)
- Separação automática dos títulos liquidados, para baixa no contas a receber
- Valores monetários com `Decimal`, sem perder centavos por arredondamento
- Identificação automática de CPF e CNPJ do pagador
- Campos alfanuméricos limpos e garantidos em ASCII, como o banco exige
- Geração de "nosso número" com dígito verificador
- Cálculo de dígito verificador nos módulos 10 e 11
- Formatação de campos, datas e valores no padrão CNAB

## Bancos e layouts suportados

| Banco | Código | Remessa CNAB 400 | Retorno CNAB 400 | Boleto |
|---|---|---|---|---|
| BMP Money Plus | 274 | Sim | Sim | Genérico |
| Itaú | 341 | Sim | Sim | Sim |

O layout CNAB 400 usado segue o padrão de mercado derivado do Bradesco (CBR643),
que é adotado por vários bancos médios. Isso facilita adicionar novos bancos:
na maioria dos casos muda pouca coisa além do código e do nome do banco.

Na coluna Boleto, "genérico" quer dizer que o código de barras é gerado, mas você
precisa montar o campo livre das 25 posições conforme o manual do seu banco.

## Roadmap

- [x] Remessa CNAB 400 para BMP
- [x] Leitura do arquivo de retorno, para baixa automática de contas a receber
- [x] Código de barras e linha digitável do boleto
- [x] Campo livre do boleto do Itaú
- [x] Remessa e retorno do Itaú em CNAB 400
- [x] Comandos de baixa, prorrogação e protesto sobre títulos já registrados
- [x] Registro de detalhe do BMP conferido posição a posição contra o manual
- [ ] Suporte a CNAB 240
- [ ] Novos bancos: Bradesco, Santander, Banco do Brasil, Caixa, Sicoob, Inter

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
- No registro de detalhe do BMP, as posições de 002 a 070 continuam em branco.
  Aí ficam campos como a identificação da empresa no banco, que alguns bancos
  exigem além do que já vai no cabeçalho. Confira com o seu antes de enviar.
- Fora o Itaú, o campo livre do código de barras precisa ser montado por você,
  porque cada banco define as 25 posições de um jeito.
- O dígito do "nosso número" usa a regra que devolve `0`; alguns bancos usam a
  letra `P` em um dos casos.
- Ao ler o retorno, confira o total recebido contra o extrato na primeira vez,
  para garantir que as posições batem com o arquivo do seu banco.
- O layout do Itaú foi escrito a partir do manual oficial de cobrança em 400
  posições e é conferido posição a posição nos testes, mas ainda não foi validado
  contra um arquivo processado pelo banco de verdade. Faça um envio de teste
  antes de usar em produção.
- No Itaú, o registro opcional de multa (tipo 2) e o de rateio de crédito
  (tipo 4) ainda não são gerados. Multa percentual diferente da cadastrada na
  conta depende desse registro.

## Glossário rápido

- **CNAB**: padrão de arquivo texto de posição fixa usado na troca de informações
  entre empresas e bancos, definido pela FEBRABAN.
- **Remessa**: arquivo que a empresa envia ao banco para registrar boletos.
- **Retorno**: arquivo que o banco devolve informando pagamentos e ocorrências.
- **Nosso número**: identificador do título no banco, definido pela empresa.
- **Pagador**: quem deve pagar o boleto (antigamente chamado de sacado).

## Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE).
