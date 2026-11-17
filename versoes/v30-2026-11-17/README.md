# Carteira Reversa — v30 (17/11/2026)

**Versão recomendada após conferência com dados reais.**

- [Abrir HTML v30 corrigido](Carteira_Reversa_Gerencial_v30_Logica_Conciliada.html)
- [Relatório completo de correções e conciliação](RELATORIO_CORRECOES_CARTEIRA_REVERSA_V30.md)
- [Relatório anterior (v29)](../v29-2026-11-16/HOMOLOGACAO_REAL_ORDER_ESTOQUE_2026-11-17.md)

**O que mudou:** importação progressiva de Order.zip com CSV grande e preenchimento NUL; recorte explícito de vencimento (todos/semana/intervalo); CAD Cód_Prod → segunda coluna Cod S4 (`Cod S4_2`) → Malha SKU SAP; indexação de chaves para acelerar; Comercial divergente não qualificado; resumo Excel e e-mail coerentes com recorte.

**Validação real em navegador (Order.zip + BASE_ESTOQUE 16.11.xlsx):** 95.548 chaves, 94.604 completas em CX, Atualizada 35.430.192,70 CX, Marcado 1.608.284 CX, Sem remessa 1.301.033 CX, Faturado 19.317.396 CX, Pendente calculado **13.203.479,70 CX**, exatamente iguais à auditoria independente do universo completo.

**Semana 16 a 22/11/2026:** 8.805 chaves, 8.704 completas, Pendente calculado de 484.615,87 CX. Carros potenciais de 24 PLT por origem: BRCH 302, BR09 125, BRDF 73, BR23 59, BR15 42, BR13 18, BR16 9. **Não somar fábricas alternativas.**

**Pontos pendentes:** 5.799 chaves ASCD/ASVD mistas, 944 chaves incompletas/não conversíveis, 3 chaves com Comercial divergente e ausência de coluna independente de Pendente na Order.

**Uso:** abrir HTML local no Chrome/Edge e importar Order.zip e BASE_ESTOQUE 16.11.xlsx. Para reproduzir totais gerais, escolha **Todos os vencimentos** e mantenha todas as redes selecionadas. Para conferir a semana, escolha **Semana do vencimento** com referência 17/11/2026. A análise de D1 indica potencial de cobertura, não reserva nem expedição confirmada.

**Nota de privacidade:** o repositório é público. Não disponibilizar novas bases com dados comerciais sensíveis como anexos públicos.
