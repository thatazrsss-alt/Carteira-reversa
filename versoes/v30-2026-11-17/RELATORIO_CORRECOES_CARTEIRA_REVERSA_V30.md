# Carteira Reversa v30 — Correção de lógica e conferência real

**Data:** 17/11/2026  
**Fontes validadas:** `Order.zip` (CSV interno da extração de 16/11/2026 às 17h30) e `BASE_ESTOQUE 16.11.xlsx` do GitHub.  
**Status:** Conciliação do motor de importação e de movimentos **aprovada no universo testado**. Homologação operacional **parcial**, com exceções e restrições de estoque registradas.

## 1. Problemas da v29 identificados e corrigidos

1. **Limite do ZIP insuficiente:** a importação bloqueava o CSV real de ~140 MB descompactados. A v30 processa o conteúdo progressivamente, com limite ajustado e sem carregar tudo como uma única string.
2. **Final do CSV com caracteres `NUL`:** a extração contém aproximadamente 62,7 milhões de caracteres de preenchimento nulo após as linhas úteis. São ignorados sem criar um pedido fictício nem interromper o leitor.
3. **Filtro de vencimento implícito:** a v29 excluía, por padrão, os pedidos anteriores à data de referência. A v30 inicia com **todos os vencimentos** e oferece filtros explícitos: todos, a partir da data, semana (segunda a domingo) ou intervalo.
4. **Mapeamento incorreto da CAD:** a chave EG oficial é `CAD.Cód_Prod`; a Malha cruza pelo **segundo** cabeçalho `Cod S4` da CAD (exposto como `Cod S4_2` depois da desambiguação de colunas repetidas), não pelo primeiro `Cod S4` nem por `Cod_SAP`.
5. **Performance da consolidação:** campos não existentes, incluindo `Pendente` independente, eram pesquisados repetidamente por linha, e algumas consultas faziam varreduras completas da CAD. Agora o mapeamento de colunas é cacheado e as chaves numéricas são indexadas.
6. **Tipo Pedido e unidades:** chaves unívocas ASCD/ASVD usam CD/VD; chaves mistas não recebem estoque automaticamente. Unidades DZ/UN/PC sem conversão comprovada permanecem não homologadas.
7. **Comercial divergente:** 3 chaves possuem código comercial inconsistente entre movimentos; a v30 impede a qualificação VD automática nesses casos e exibe alerta específico.
8. **Resumo Excel e e-mail:** totais de itens atendidos seguem `serviceStatus()` em vez de considerar todo pendente zero como atendido. O resumo Excel mostra o recorte de vencimento, e o assunto de e-mail na semana usa a data final (ou vencimento escolhido manualmente).
9. **Dependência externa:** o leitor de XLSX passou a usar as bibliotecas já embutidas no HTML; o teste passou sem bibliotecas remotas.

## 2. Validação no navegador com as duas bases reais

O HTML corrigido foi executado no Chromium, carregando os dois arquivos completos. Foram identificadas a Order mais 11 abas da base de estoque, com **zero falhas de importação** e **zero erros JavaScript de página** durante a conferência.

| Indicador | HTML v30 | Auditoria independente | Resultado |
|---|---:|---:|---|
| Chaves Pedido ERP + Cliente EG + SKU EG | 95.548 | 95.548 | Bate |
| Chaves com movimentos completos e conversíveis em CX | 94.604 | 94.604 | Bate |
| Quantidade atualizada (CX) | 35.430.192,70 | 35.430.192,70 | Bate |
| Marcado / Carro com remessa (CX) | 1.608.284,00 | 1.608.284,00 | Bate |
| Carro sem remessa (CX) | 1.301.033,00 | 1.301.033,00 | Bate |
| Faturado (CX) | 19.317.396,00 | 19.317.396,00 | Bate |
| **Pendente calculado (CX)** | **13.203.479,70** | **13.203.479,70** | **Bate** |

**Fórmula:** `Pendente = Atualizada − Carro com Remessa − Carro sem Remessa − Faturado`. A extração não possui um Pendente oficial independente; o resultado é uma reconciliação da fórmula, não atestado de uma fonte externa.

**Canais:** 82.805 chaves ASCD; 6.944 ASVD; 5.799 mistas. **944 chaves** não dispõem de movimentos completos ou unidade convertível em CX.

### Recorte semanal demonstrado

Com referência de 17/11/2026 e opção **Semana do vencimento** (16 a 22/11/2026), o HTML encontrou **8.805 chaves**, sendo **8.704 completas**, e calculou **484.615,87 CX de Pendente**, o mesmo resultado independente. O assunto do e-mail usa **22/11/2026** quando não substituído manualmente.

### Formação VD por fábrica — potencial não reservado

| Centro VD | Carros inteiros potenciais de 24 PLT | PLT qualificados no HTML |
|---|---:|---:|
| 324-VD / BRCH | 302 | 7.257,62 |
| 893-VD / BR09 | 125 | 3.007,71 |
| 424-VD / BRDF | 73 | 1.759,17 |
| 952-VD / BR23 | 59 | 1.425,10 |
| 892-VD / BR15 | 42 | 1.013,33 |
| 781-VD / BR13 | 18 | 445,45 |
| 260-VD / BR16 | 9 | 224,99 |

Os carros inteiros potenciais individuais correspondem aos da auditoria original. O volume BR09 ficou **13 PLT menor** do que o ensaio anterior porque a versão atual **bloqueia a origem de uma chave com comercial contraditório** em vez de escolher arbitrariamente uma das fábricas. A mesma chave já não contribui indevidamente para BRCH. Esta é uma exclusão conservadora, documentada, não correção silenciosa de estoque.

**Atenção:** esses valores são de todos os vencimentos e representam cenários independentes por fábrica; **não são carros programados, reserva de D1 nem volumes que possam ser somados entre origens alternativas**.

## 3. Como comparar os mesmos números no HTML

1. Abra `Carteira_Reversa_Gerencial_v30_Logica_Conciliada.html` em navegador atualizado, preferencialmente Chrome ou Edge.
2. Carregue **simultaneamente** `Order.zip` e `BASE_ESTOQUE 16.11.xlsx`.
3. Confira o diagnóstico: **12 tabelas**, **95.548 chaves** consolidadas. Confira os avisos, principalmente unidades não convertíveis e comerciais divergentes.
4. Para comparar com os totais acima, use **Todos os vencimentos**, sem recorte de rede ou data de captação. Não compare totais de uma rede/semana com o total geral de todos os pedidos.
5. Para verificar a semana de 16 a 22/11, selecione **Semana do vencimento** e referência **17/11/2026**. Compare apenas as **8.704 chaves completas em CX**.
6. Para revisar estoques, o filtro de canal deve respeitar ASVD/ASCD/MISTO e as fábricas alternativas não podem ser somadas como se a mesma demanda fosse atendida duas vezes.

## 4. O que ainda impede homologação irrestrita

- **5.799 chaves ASCD/ASVD mistas** exigem regra operacional de atribuição ou segregação de movimentos; seu saldo não pode ser atribuído inteiro a VD ou CD automaticamente.
- **944 chaves** com movimentos incompletos ou sem conversão oficial de unidade.
- **3 chaves** com Comercial divergente dentro da mesma chave; uma ASVD afeta o cenário potencial VD e permanece sem alocação automática.
- A fonte não fornece **Pendente oficial independente** para confronto do saldo calculado.
- A validação dos valores de estoque é de **cobertura potencial** por SKU/origem; não existe confirmação de reserva, expedição ou faturamento futuro.
- A exibição e exportação dependem dos filtros de rede, validade e captação; confira sempre o recorte antes de interpretar números.

**Conclusão:** o problema de lógica da v29 foi reproduzido e corrigido na **v30**; a conferência de importação, saldos e formação potencial passou com as bases reais. A versão é apropriada para **conferência gerencial com alertas**, não para declarar atendimento/expedição confirmados nos casos pendentes.