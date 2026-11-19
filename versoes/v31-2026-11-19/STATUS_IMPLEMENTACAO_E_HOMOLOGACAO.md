# Carteira Reversa v31 — Entrega técnica e situação da homologação

Data: 19/11/2026. Base preservada: `v30-2026-11-17/Carteira_Reversa_Gerencial_v30_Logica_Conciliada.html`.

## Entrega
- `Carteira_Reversa_Gerencial_v31_Homologacao_Integrada.html` — painel HTML com as bibliotecas Excel/ZIP embarcadas da v30, novas áreas VD, CDD para VD e Envio/PDF.
- Modificações adicionais: Fill Rate de Volume com faturado + carro com remessa em pontos principais da aplicação legada; Fill Rate de Itens com qualquer movimento positivo; seleção Rede/EG; importação manual independente da Order/Estoque; visualização de carros e saldo por origem; exportação Excel gerencial v31; relatório cliente A4 horizontal por impressão do navegador; rascunho Outlook via mailto sem anexos.
- Estoque D1 e Grade CD são consultados por Cliente EG; D1 é fixo da fonte ativa, sem desconto entre clientes.
- Alerta: a aba antiga da v30 ainda oferece funcionalidades de compatibilidade; priorizar as abas **Qualificação v31** e **Envio e PDF v31** para os resultados novos.

## Verificação realizada
- Recuperação do HTML de 747 kB do repositório via conexão GitHub.
- Compilação sintática, com JavaScript parser, dos quatro blocos `<script>` do HTML após a alteração: **sem erros sintáticos**.
- Verificação de presença dos novos componentes de navegação, importação, qualificações, CDD, Excel e PDF.
- Foram feitas atualizações incrementais e versionadas em commits GitHub.

## Não homologado (bloqueadores para aprovação final)
1. **Bases reais**: a Order.zip e BASE_ESTOQUE precisam ser executadas juntas no navegador nesta v31. Não foi feita a reconciliação numérica com os arquivos reais nesta entrega.
2. **Otimização**: a formação implementada prioriza carros de 24 PLT, preenche até 28 após fechar carros, respeita limite por SKU/origem e Cliente EG, mas utiliza **heurística gulosa**. Não há prova de que ela maximiza globalmente o número de carros para todos os arranjos de múltiplas origens. Não homologar este requisito como ótimo matemático.
3. **Cobertura CD**: verificar múltiplas linhas e duplicatas da Grade CD em cada CDD e o de/para de clientes ASVD com exemplos reais.
4. **Pedido misto**: chaves com ASCD e ASVD sem atribuição inequívoca ainda são assinaladas; não fazer rateios presumidos entre canais.
5. **PDF**: a versão HTML usa **Imprimir / Salvar como PDF** do navegador. É preciso conferir paginação, tabela por EG, composição visual e sigilo de informações no PDF efetivamente salvo.
6. **Outlook**: o botão cria rascunho por `mailto:` com campos texto. **Não envia nem anexa PDF automaticamente**. Integração corporativa real depende da infraestrutura e autorização de TI.
7. **Conciliação e UX**: verificar performance com toda a Order, filtros, unidade de medida, resultado de todas as 58 regras e consistência das antigas abas com o novo motor.

## Aceite
Status: **VERSÃO IMPLEMENTADA PARA TESTES — NÃO HOMOLOGADA COM DADOS REAIS**.

Critérios para liberação: conciliar chaves, movimentos e Fill Rates com Order; comprovar CAD/S4/Malha/estoque SP; demonstrar max formação de carros por Cliente EG e origem, sem duplicações; reconciliar buckets; comparar HTML/Excel/PDF; conferir segurança e envio somente sob aprovação.
