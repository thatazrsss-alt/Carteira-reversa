# Carteira Reversa v31 — Conciliação visual e residual VD

Data: 23/11/2026. Construída como evolução da v30, preservada na pasta anterior.

## Atualizações

- Faixas de vencimento: vencidos, 0–3, 4–7, 8–14, 15–21, 22–30, mais de 30 e sem validade.
- Nome de produto: consulta descrição disponível na CAD/Produção/estoque antes da descrição original da Order; não rotular produto com o nome do cliente; quando não encontrado, informar ausência de descrição.
- Formação VD por origem: visualização de elegível em pallets, potencial de carros mínimos de 24 PLT, residual com estoque e complemento necessário, e detalhes de SKU, descrição, saldo D1 e pendência. Os cenários por origens alternativas não são somáveis como garantia operacional.
- Conciliação visual: quantidade atualizada, marcado, sem remessa, faturado e pendente, com investigação da chave e movimentos brutos.
- Cancelados: exclusão do cálculo ativo **somente** quando o campo explícito de status do pedido/item/linha/movimento contém exatamente cancelado/cancelada/cancelled/canceled. Exibição segregada das linhas identificadas. Sem campo inequívoco, sinaliza N/D e não exclui silenciosamente.
- E-mail: instruções do fluxo existente de download .eml com Excel anexo; envio final permanece no aplicativo de e-mail, sujeito a revisão.

## Limites / homologação

**Não homologado com bases reais nesta revisão.** O JavaScript da v31 passou no teste de sintaxe (parse), mas é necessário executar no Chrome/Edge com Order.zip e BASE_ESTOQUE 16.11.xlsx. A v30 é a última versão com auditoria de dados registrada.

O cálculo oficial segue a v30: `Pendente = Σ(Atualizada − Marcado/Carro com remessa − Carro sem remessa − Faturado)`, usando somente movimentos convertíveis para CX. O campo Pendente independente não foi identificado de maneira geral na extração original: igualdade com a própria fórmula não é homologação externa.

**Itens ainda necessários antes da aprovação:**
1. Conferir SONDA pedido 4801420253, SKUs 44099 e 50294, e o comportamento de canal MISTO.
2. Validar na Order real a nomenclatura e semântica do status cancelado, incluindo estornos/substituições.
3. Auditar um SKU com descrição antes incorretamente igual ao cliente e verificar descrição oficial.
4. Auditar cada fábrica com residual; carros de 24 PLT são apenas teto matemático potencial, sem otimização 24–28 PLT com restrições logísticas.
5. Inspecionar visualmente o HTML, testar os filtros, abrir o detalhe por linha, gerar e abrir Excel e rascunho .eml.
6. Validar divergências do Pendente com coluna independente quando houver.

Arquivo principal: [Carteira_Reversa_Gerencial_v31_Concilicao_Visual.html](Carteira_Reversa_Gerencial_v31_Concilicao_Visual.html).

Privacidade: repositório GitHub identificado como público; não incluir novos arquivos com dados comerciais reais neste diretório.
