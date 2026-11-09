# Arquitetura

O OpenCNAB é uma biblioteca Python para gerar remessas, ler retornos e montar
códigos de barras e linhas digitáveis de boletos. Usa somente a biblioteca
padrão do Python em execução. As dependências de desenvolvimento ficam no
extra `dev` do `pyproject.toml`.

## Organização

| Caminho | Responsabilidade |
|---|---|
| `opencnab/nucleo/` | Formatação de campos, datas, valores, documentos e cálculos de módulo 10 e 11 |
| `opencnab/boletos/` | Código de barras, fator de vencimento e linha digitável genéricos |
| `opencnab/bancos/bmp/cnab_400/` | Modelos, registros, remessa, retorno e ocorrências do BMP |
| `opencnab/bancos/itau/boleto.py` | Campo livre e dígitos verificadores próprios do Itaú |
| `opencnab/bancos/itau/cnab_400/` | Modelos, registros, remessa, retorno, ocorrências e instruções do Itaú |
| `opencnab/__init__.py` | Imports curtos da API pública |
| `tests/` | Testes dos cálculos, posições dos campos e fluxos completos |

As regras compartilhadas ficam no núcleo. As diferenças de cada banco ficam
em seu próprio diretório, separadas também pelo layout. Atualmente, os dois
bancos implementam CNAB 400; CNAB 240 ainda não está implementado.

## Geração de remessa

O usuário cria um `ArquivoRemessaBMP` ou `ArquivoRemessaItau` e adiciona títulos
com `adicionar_boleto`. Os dados de cada título ficam em `BoletoBMP` ou
`BoletoItauCobranca`, classes simples com atributos definidos no construtor.

Os métodos como `pedir_baixa` e `alterar_vencimento` montam comandos usando o
mesmo modelo de título, com a ocorrência correspondente. Comandos e títulos
novos ficam na mesma lista e são gravados na ordem de inclusão.

Ao chamar `gerar()`, a remessa monta o header, um registro de detalhe por
título ou comando e o trailer. Cada registro concatena os campos na ordem do
layout, usando `campos.append` e comentários com as posições do manual.
O resultado é um texto com linhas de 400 posições separadas por CRLF.

`salvar(caminho)` gera esse texto e grava em ASCII, preservando o CRLF.
As funções do núcleo removem acentos, preenchem espaços e zeros e formatam
datas e valores antes da montagem dos registros.

## Leitura de retorno

`ArquivoRetornoBMP` e `ArquivoRetornoItau` recebem o conteúdo do arquivo em
texto. O método `ler()` identifica os tipos de registro, lê o header e
transforma cada detalhe em um título de retorno. Cada chamada refaz a lista
de títulos para evitar duplicação em leituras repetidas.

Os campos são extraídos por fatias da linha, com as posições do layout
comentadas ao lado. Campos opcionais de valor em branco viram `Decimal("0.00")`
e datas em branco ou zeradas viram `None`.

`pagos()` seleciona os títulos pelas ocorrências de pagamento de cada banco.
`total_pago()` soma os valores pagos desses títulos usando `Decimal`.
Os atalhos `ler_retorno_bmp` e `ler_retorno_itau` abrem o arquivo em Latin-1
e já executam a leitura.

## Boletos e valores

As funções genéricas montam o código de barras de 44 posições e a linha
digitável de 47 posições. `BoletoItau` acrescenta as regras do campo livre
do Itaú. Ele é separado de `BoletoItauCobranca`, que representa o título
enviado na remessa.

`valor_cnab` converte a entrada com `Decimal(str(valor))`, arredonda os
centavos com `ROUND_HALF_UP` e verifica o tamanho do campo. Valores negativos
ou não finitos são recusados. `valor_de_cnab` faz o caminho contrário e
devolve `Decimal`.

## Como continuar o código

Mantenha nomes em português, variáveis intermediárias claras e cálculos
escritos em etapas. Use classes simples, imports individuais e comentários
que expliquem a regra bancária. Nos registros, preserve a montagem em ordem
e a identificação das posições.

Os testes seguem o mesmo estilo: funções de apoio pequenas, exemplos
concretos, variável `resultado` e verificações diretas com `assert`. Mudanças
de comportamento precisam de testes que reproduzam o problema ou confiram
a nova regra. Os testes de posição devem usar valores esperados explícitos.

Para desenvolver, instale com `python -m pip install -e ".[dev]"` e execute
`python -m pytest -q`. O GitHub Actions executa a suíte em Python 3.11, 3.12
e 3.13 nos PRs e pushes para `develop` e `main`.

Consulte também [bancos suportados](bancos_suportados.md) e [roadmap](roadmap.md).
