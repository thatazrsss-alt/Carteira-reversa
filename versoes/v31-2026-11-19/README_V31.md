# Carteira Reversa v31 — pacote de implementação

**Data:** 19/11/2026  
**Status:** Versão implementada para **homologação técnica**, não homologada em produção.  
**Base:** HTML offline v30 de 17/11/2026, mantido integralmente como fundamento; ajustes v31 acrescentados sem editar/destruir a v30.

## Arquivo principal

`Carteira_Reversa_Gerencial_v31_Homologacao.html`

1. Baixar o arquivo HTML pelo GitHub (**Download raw file**).
2. Abrir no **Microsoft Edge** ou Google Chrome do computador.
3. Em **Bases e redes**, importar **manualmente** `Order.zip` e `BASE_ESTOQUE 16.11.xlsx` na mesma seleção. Não é necessário conectar Outlook ou ChatGPT.
4. Conferir a quantidade de chaves únicas, os avisos da importação e o período de **Validade**; **Captação** é opcional.
5. Em **Análise gerencial**, conferir Fill Rate de Volume e Itens, carros VD por Cliente EG/origem, saldo qualificado sem carga e diferença em PLT para fechar carro.
6. Em **Oportunidades CDD VD** verificar a Grade CD como alternativa gerencial a volumes sem carga VD, sem alterar Fill Rates.
7. Em **Conferência interna** verificar reconciliação e diagnósticos. Para casos ASCD/ASVD mistos, exportar **Excel interno** e analisar a aba `Movimentos ASCD ASVD`.
8. Em **Materiais por rede**, escolher Rede e, opcionalmente, **Cliente EG — Nome**; `Visualizar PDF / Imprimir` abre uma janela de relatório. Usar **Imprimir > Salvar como PDF** no navegador.
9. O Excel do cliente não divulga saldo D1 total. Excel interno inclui auditoria, cobertura CD e oportunidades CDD VD.
10. A prévia de e-mail permite editar texto/destinatários e abrir rascunho no Outlook, **sem anexos automáticos nem disparo**. Anexar o PDF salvo e conferir destinatários antes de enviar.

## Regras funcionais incorporadas

- Chave Pedido ERP + Cliente EG + SKU EG; original único, faturado e marcado em colunas separadas;
- Faturado + Marcado (Carro com remessa) no Fill Rate de Volume;
- Qualquer faturado ou marcado positivo conta uma chave no Fill Rate de Itens, mesmo parcial;
- Validade principal, captação opcional, vencidos permanecem no recorte;
- D1 da base ativa fixo, isolado por Cliente EG;
- SKU EG -> CAD (Cód_Prod) -> segundo Cod S4 -> Malha por Comercial/SAP; diagnóstico S4 ausente;
- Origens SP BR15, BR16, BR23, BRDF, BRCH apenas no fallback sem Malha;
- Grade CD em CX, D1 fábrica em PLT, conversão CAD quando necessária;
- Pallet inteiro separado de fração, bucket `Não qualificado — pallet fracionado`;
- Otimização de 24 a 28 PLT da mesma origem e Cliente EG, com prioridade de **quantidade de carros**; composição por Pedido ERP e SKU;
- Estoque físico D1 e oportunidades qualificadas em indicadores separados;
- Oportunidade adicional no CDD para pendências VD sem carga;
- PDF por Rede com seções por Cliente EG, seleção prévia de EG e exibição visual sem D1 nem auditoria;
- Atualização exclusivamente manual das bases, sem botão GitHub.

## Restrições técnicas a homologar

1. **A versão v31 ainda não foi executada neste ambiente com a Order e a Base de Estoque reais.** As quantidades da v30 não podem ser atribuídas automaticamente à v31.
2. **Busca ótima de carros:** para clientes com múltiplas origens/volumes grandes, a v31 usa busca viável com otimização heurística quando a prova exaustiva é custosa. A aba interna sinaliza necessidade de verificar o ótimo. Não declarar eficiência ótima irrestrita sem T04.
3. **Chaves mistas ASCD/ASVD:** seus movimentos são discriminados por canal no **Excel interno** quando as unidades são conciliáveis; a qualificação automática de estoque por canal continua bloqueada quando a atribuição de pendente não é demonstrável, para não inventar estoque ou duplicar demanda.
4. **PDF:** saída por impressão do navegador (Salvar como PDF), não geração silenciosa de anexo PDF.
5. **Outlook corporativo:** o HTML não envia e-mails nem consegue anexar PDF ao Outlook por conta própria; uma automação real depende de solução local/integração liberada pela TI, depois da homologação.
6. **D1 duplicado entre arquivos:** arquivos de períodos diferentes não devem ser importados simultaneamente como se fossem uma base ativa. Confira a origem e data da base.

## Testes de liberação

Executar e documentar os **T01–T18** descritos na `Carteira_Reversa_v31_Especificacao_Homologacao.md` anteriormente consolidada.

Validar em especial T01–T02 (FR), T03 e T18 (D1 sem duplicidade), T04 (mais carros), T05–T06 (frações/sem carga), T07–T08 (S4/Malha alternativa), T09 (CDD para VD), T10 (Rede/EG/PDF), T12 (filtros sem alterar D1), T14 (CX versus PLT), T15 (consistência Excel/HTML/PDF).

**Somente liberar envio comercial depois de reconciliar resultados com bases reais e fechar as exceções da conferência interna.**
