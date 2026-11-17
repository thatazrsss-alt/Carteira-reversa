# Carteira Reversa v29 — reconciliação e conferência das fontes (17/11/2026)

**Parecer: reconciliação operacional bloqueada por indisponibilidade dos registros tabulares reais neste acesso. NÃO HOMOLOGADO.**

## Fontes efetivamente verificadas

| Fonte | Evidência obtida | Status |
|---|---|---|
| `BASE_ESTOQUE 16.11.xlsx` (GitHub, raiz) | Arquivo existente, 4.469.103 bytes, SHA Git `81293008fd9c1e716d173f81f68c2f938f22cda4` | Conteúdo binário não acessível pelos leitores integrados nesta execução |
| `analise-carteira-reversa (15).zip` (GitHub, raiz) | Arquivo existente, 371.192 bytes; diretório interno listado diretamente | **Não foi identificada uma Order operacional real neste pacote** |
| Order/Pedidos/Pendente real | Nenhum arquivo independente localizável nas buscas de arquivos do projeto / repositório | Fonte obrigatória ausente |
| Gerencial v29 HTML | Código textual acessado, compilado e auditado | Revisão de lógica sem confronto das bases reais |

### Conteúdo confirmado do ZIP v15

O ZIP contém `SKILL.md`, arquivos `references/auditoria_e_conferencias.md`, `references/regras_calculo.md`, `references/layout_excel.md`, scripts Python (`calculo.py`, `modelo_painel.py`, `test_calculo.py`, etc.), `assets/previa_painel.png`, **`assets/exemplo_entrada.xlsx`** e **`assets/exemplo_saida.xlsx`**.

O único workbook de entrada no ZIP tem nome **exemplo_entrada.xlsx** (aprox. 50 KB descompactados), não há workbook chamado Order nem qualquer arquivo identificado como extração real vigente de pedidos. Não é correto tratá-lo como prova de reconciliação operacional sem inspecionar seus dados e confirmar sua proveniência.

## Cruzamentos inspecionados no HTML v29

| Controle | Regra presente no código | Limitação da conclusão |
|---|---|---|
| Entrada original | Chave Pedido ERP + EG Cliente + SKU EG, entrada original única | Sem valores reais para conferência de duplicados |
| Movimentações | Pendente calculado pela soma por linha de Atualizada − Carro com remessa (= Marcado) − Carro sem remessa − Faturado | Precisa validar se as colunas da Order representam movimentos exclusivos ou saldos cumulativos |
| Pendente da fonte | Implementado `pendingVsSourceDelta` entre Pendente calculado e Pendente informado na Order | Sem coluna real acessível não é possível calcular o delta |
| Fill rate | Faturado CX / Original CX com teto visual 100%; bruto não é modificado | Não confere valores reais sem Order |
| CAD | SKU EG → SAP na Malha, fator CX/PLT para conversão | Não foi possível verificar de/para e fatores reais |
| Malha | Chave Comercial + SAP → origem elegível | Sem linhas reais para validar casamento / cobertura |
| Estoque fábrica | SKU EG + fábrica, com estoque VD em D1 PLT | Sem linhas reais para detectar conflitos, duplicação ou faltantes |
| CD | CDD via DPAR da loja, grade do CDD em CX | Sem linhas reais para conferir CDD e SKUs |
| Produção | Data por SKU EG e origem, sem somar volume futuro | A regra foi inspecionada, não as datas reais |
| Formação de carro | Por mesma origem, `floor(PLT qualificados / 24)`, limite compartilhado D1 por SKU dentro da origem | É potencial, não reserva nem prova de capacidade agregada entre fábricas |

## Testes controlados disponíveis

A inspeção funcional anterior registrou 27 testes controlados aprovados: formação de 25 PLT → 1 carro, estoque compartilhado limitado por SKU/origem, ausência de estoque, CAD reconhecida, itens atendidos, movimentações e saldos. Esses testes são **sintéticos** e não substituem confronto com a extração real.

**Atenção metodológica:** `movementDelta` é uma identidade aritmética calculada com os próprios movimentos; tende a zero por construção. A validação independente relevante é `pendingVsSourceDelta`, calculado contra a coluna de pendente da Order, além de evidência do significado temporal de Marcado e Faturado.

## Resultado objetivo da tentativa de reconciliação

- **Pedidos reais conciliados:** N/D — nenhuma Order operacional confirmada foi lida.
- **SKUs reais conciliados:** N/D.
- **Divergência total de Pendente (CX):** N/D.
- **Diferença Marcado x Carro com Remessa:** N/D.
- **Fill rate real:** N/D.
- **Cobertura real D1 VD/CD:** N/D.
- **Pallets qualificados e carros por origem:** N/D.

**Não substituir N/D por zero.** Sem a base real, qualquer número informado seria inventado.

## Evidência que desbloqueia o fechamento

Disponibilizar os bytes dos arquivos **Order operacional real** e **BASE_ESTOQUE 16.11.xlsx** como anexos acessíveis, ou permitir execução em ambiente com acesso real de leitura a ambos. A partir daí, produzir tabela por Pedido ERP + EG Cliente + SKU EG e por origem/SKU com: original, atualizado, marcado, sem remessa, faturado, pendente calculado, pendente da fonte, diferença, fator CAD, pendente PLT, D1, qualificação e carros potenciais de 24 PLT.

Esta conferência não publica dados de cliente ou pedido em um repositório público.
