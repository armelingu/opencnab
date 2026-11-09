# Bancos e layouts suportados

O suporte atual é de cobrança em CNAB 400. A biblioteca gera os arquivos
localmente; a transmissão ao banco e a homologação ficam com quem a utiliza.

| Banco | Código | Remessa 400 | Retorno 400 | Campo livre do boleto | CNAB 240 |
|---|---|---|---|---|---|
| BMP Money Plus | 274 | Implementado | Implementado | Informado pelo usuário | Planejado |
| Itaú | 341 | Implementado | Implementado | Implementado | Planejado |

## BMP Money Plus

`ArquivoRemessaBMP` gera header, detalhes tipo 1 e trailer. `BoletoBMP`
recebe os dados dos títulos, incluindo os campos opcionais de emissão,
endereço, instruções, juros, desconto, IOF, abatimento e mensagens.

Os comandos disponíveis são baixa, alteração de vencimento, alteração de
valor, protesto, sustação de protesto com baixa ou manutenção em carteira,
concessão de abatimento e cancelamento de abatimento.

`ArquivoRetornoBMP` lê os dados da empresa e dos títulos, traduz ocorrências
e permite selecionar pagamentos e somar os valores recebidos.

O layout segue o padrão de mercado derivado do Bradesco, usado pela
implementação do BMP. As posições 002–070 do detalhe ainda vão em branco.
Confira as exigências do contrato e do manual do banco antes do primeiro envio.
O cálculo do nosso número usa módulo 11 com os casos especiais retornando zero.

O código de barras genérico pode ser usado com o código 274, mas o usuário
precisa informar o campo livre conforme a regra de sua carteira.

## Itaú

`ArquivoRemessaItau` gera header, detalhes tipo 1 e trailer. Cada detalhe
inclui agência, conta, carteira e documento da empresa. `BoletoItauCobranca`
recebe os dados do título; `EnderecoPagador` reúne seu endereço.

Os comandos disponíveis são baixa, baixa por pagamento direto, alteração
de vencimento, protesto, sustação de protesto, concessão e cancelamento de
abatimento e dispensa de juros. O módulo `ocorrencias` contém também códigos
que ainda não possuem métodos próprios na remessa.

O módulo `instrucoes` reúne os códigos de cobrança. A geração valida prazo
obrigatório, conflito entre protestar e não protestar e desconto sem data
limite. Instruções de cobrança e ocorrências da remessa têm funções distintas.

`ArquivoRetornoItau` lê os títulos, dados da empresa, tarifas, descontos,
abatimentos e outros créditos. A seleção de pagamentos usa a tabela própria
de ocorrências do Itaú.

`BoletoItau` monta o campo livre, o código de barras e a linha digitável,
calculando os dígitos de agência com conta e do nosso número.

Os registros opcionais de multa tipo 2 e rateio de crédito tipo 4 ainda
não são gerados. A implementação tem testes de posições e um ciclo de
remessa e retorno simulado, mas isso não substitui a homologação com o banco.

Os manuais CNAB 400 e CNAB 240 de setembro de 2026, fornecidos para a
continuidade do projeto, são as referências para novas conferências. Seu
recebimento não significa que toda a implementação já foi revisada contra
essa edição. O manual CNAB 240 não se aplica aos campos do CNAB 400.

## Outros bancos

Bradesco, Santander, Banco do Brasil, Caixa, Sicoob e Inter estão no roadmap.
Compartilhar posições com outro layout não estabelece suporte a um banco.
Cada implementação precisa conferir as regras do manual correspondente,
ter testes próprios e passar pela homologação exigida pelo banco.

Veja os exemplos de uso no [README](../README.md) e as próximas entregas no
[roadmap](roadmap.md).
