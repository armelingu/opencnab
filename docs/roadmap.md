# Roadmap

Este documento organiza a continuidade do projeto. Os itens concluídos
representam código integrado em `develop`; uma versão publicada depende
da entrega correspondente em `main` e de sua tag.

## Correções

- [x] Recusar valores monetários negativos, NaN e infinitos na geração.
- [x] Evitar duplicação de títulos e total pago ao repetir a leitura de retorno.
- [ ] Integrar a correção do sequencial do header Itaú, conferida na página 21
  do manual CNAB 400 de setembro de 2026. A alteração está na branch
  `fix/itau-sequencial-header` e mantém o parâmetro existente na API.

## Melhorias e testes

- [x] Cobrir os campos opcionais do detalhe BMP, incluindo sua combinação
  e o truncamento de textos sem deslocamento dos campos seguintes.
- [x] Cobrir tamanhos máximos e estouros dos campos numéricos e monetários,
  truncamento de textos, tamanhos inválidos de documentos e datas inexistentes.
- [ ] Fortalecer a leitura dos retornos: identificação do banco, ordem dos
  registros e estrutura do arquivo. Definir a compatibilidade antes de tornar
  a leitura mais restritiva, preservando campos opcionais em branco.
- [ ] Conferir as regras já implementadas do Itaú contra a edição de setembro
  de 2026, separando cada diferença confirmada em uma correção com teste.

## Novas funcionalidades

- [ ] Implementar o registro tipo 2 de multa do Itaú CNAB 400, conforme o
  manual atual, com validações, posições e sequência dos registros testadas.
- [ ] Ampliar os métodos de comando das remessas para as ocorrências já
  catalogadas, conferindo os campos exigidos por cada operação.
- [ ] Adicionar outro banco em CNAB 400. Escolher o banco e reunir seu
  manual antes de implementar remessa e retorno.
- [ ] Iniciar CNAB 240. Definir banco, serviço e versão do layout da primeira
  entrega; para o Itaú, usar o manual de setembro de 2026 como referência.

## Documentação

- [x] Descrever a arquitetura e o caminho dos dados na geração e na leitura.
- [x] Documentar os bancos suportados, funcionalidades e limites atuais.
- [x] Organizar o roadmap por tipo de entrega.
- [x] Preencher os exemplos executáveis de geração de remessa e leitura de
  retorno, usando dados fictícios e instruções de execução.

## Automação

- [x] Executar a suíte no GitHub Actions em Python 3.11, 3.12 e 3.13.
- [ ] Definir as verificações obrigatórias de merge nas configurações do
  repositório, depois de conferir as regras existentes.

## Critérios de entrega

Cada entrega precisa ter um objetivo definido, seguir o estilo do projeto
e incluir testes para mudanças de comportamento. Quando houver diferença
de layout, registre o manual e a posição que justificam a alteração.

Os commits podem ser incrementais dentro da mesma branch. O PR reúne a
entrega completa, explica o comportamento resultante e informa os testes
executados. Consulte o [fluxo de desenvolvimento](desenvolvimento.md).
