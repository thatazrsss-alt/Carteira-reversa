# Homologação com dados reais — Order + BASE_ESTOQUE 16.11
**Execução: 17/11/2026 • Código do painel: v29 • Status: PARCIALMENTE HOMOLOGADO COM PENDÊNCIAS MATERIAIS**

> Este parecer substitui os relatórios anteriores que registravam ausência da Order. A Order foi localizada como `Order.zip` no repositório, dentro da qual existe a extração `2026.11.16_17.30 ExportReportOrderItem.csv`.

**Fontes:** `Order.zip` (CSV operacional, 127.057 registros, 65 colunas) e `BASE_ESTOQUE 16.11.xlsx` (CAD, Malha, Estoque Fábricas, Produção, DeParaCDD e 6 grades CD).

**Execução reproduzível:** [GitHub Actions — auditoria final e artefatos CSV](https://github.com/thatazrsss-alt/Carteira-reversa/actions/runs/44090608561). **Script:** [reconciliar_order_v29.py](../../scripts/reconciliar_order_v29.py).

## 1. Granularidade e integridade da Order

| Controle | Contagem |
|---|---:|
| Linhas CSV | 127.057 |
| Chaves distintas `Pedido ERP + Cliente EG + SKU EG` | 95.548 |
| Chaves que ocorrem em mais de uma linha | 18.612 |
| Movimentações adicionais depois da primeira linha das chaves | 31.025 |
| Registros descartados por chave incompleta | 484 |
| Chaves com quatro movimentos completos e unidade CX homologável | **94.604** |
| Chaves ainda não convertíveis/incompletas | **944** |

A entrada Original (HL/PLT/CX) é selecionada uma vez pela menor Data de Criação, com desempate por vencimento. Todas as movimentações de linhas válidas com a mesma chave são acumuladas, sem somar repetidamente o Original. Os 944 casos incompletos não recebem saldo inventado.

A `Unidade` observada contém CX, DZ, UN, PC e vazios; as três últimas categorias não são interpretadas como CX sem fator oficial de conversão.

## 2. Reconciliação independente dos movimentos — CX

| Componente | CX |
|---|---:|
| Quantidade atualizada | 35.430.192,70 |
| Carro com remessa **(= Marcado)** | 1.608.284,00 |
| Carro sem remessa | 1.301.033,00 |
| Faturado `Qtd. Faturada` | 19.317.396,00 |
| **Pendente calculado** | **13.203.479,70** |
| Original selecionado (comparador do Fill Rate, universo completo) | 39.031.102,66 |

**Fórmula:** Pendente = Atualizada − Carro com remessa − Carro sem remessa − Faturado.

**Limitação crucial:** a Order não contém coluna independente `Pendente`. O fechamento aritmético entre os quatro componentes confirma a implementação da fórmula, **mas não constitui conferência externa contra um saldo oficial**. Marcado é o próprio Carro com remessa; não são dois movimentos. Quantidades CX não devem ser descritas como número de carros distintos.

### Situação dos itens

| Classificação de chave SKU/pedido | Chaves |
|---|---:|
| Pendente zero, com atendimento indicado por movimentos | **58.147** |
| Pendente zero, porém atendimento não comprovado | **23.220** |
| Atendimento parcial com saldo pendente | **1.167** |
| Saldo pendente, sem remessa/faturamento | **12.070** |
| Não validadas em CX / incompletas | **944** |
| **Total** | **95.548** |

“Atendimento indicado por movimentos” não é comprovante de entrega física, que exigiria uma confirmação logística ou fiscal oficial. Pendente zero isoladamente não é atendimento.

## 3. Risco crítico — chaves ASCD/ASVD mistas

| Universo | Chaves | Pendente calculado CX (quando completo) |
|---|---:|---:|
| ASCD inequívoco | 82.805 (81.973 completas) | 403.853,83 |
| ASVD inequívoco | 6.944 (6.921 completas) | 5.977.387,87 |
| **ASCD + ASVD na mesma chave** | **5.799 (5.710 completas)** | **6.822.238,00** |

Dentro das 5.799 chaves mistas:
- **4.416** possuem apenas um Tipo Pedido não cancelado, sendo 3.170 ASCD e 1.246 ASVD. O pendente dessas chaves soma 4.432.917 CX. Esse é um **candidato à investigação**, não autorização automática para classificar todo o saldo como o tipo não cancelado.
- **448** contêm ambos os tipos não cancelados, com 2.367.991 CX de pendente.
- **935** não têm tipo não cancelado, com 21.330 CX de pendente.
- **1.303** chaves mistas apresentam pendente positivo.

**Decisão de homologação:** manter a chave oficial, preservar os movimentos e **não atribuir automaticamente os 6,82 milhões de CX a CD ou VD**. A v29 foi ajustada para usar `Tipo Pedido` quando inequívoco e sinalizar `MISTO`. A atribuição de chaves mistas requer regra de negócio ou inspeção das linhas.

## 4. Outros alertas comprovados

| Exceção | Chaves | Pendente CX dessas chaves* |
|---|---:|---:|
| Sem DeParaCDD entre as lojas ASCD | 72.273 | 384.770,83 |
| Original HL/PLT/CX divergente entre registros da chave | 3.540 | 3.706.599,00 |
| SKU não localizado na grade do CDD definido | 1.885 | 2.565,00 |
| Movimentação/unidade não convertível em CX | 944 | N/D |
| Faturado acumulado superior ao Original selecionado | 707 | 98.026,00 |
| Malha sem relação Comercial + SKU SAP elegível (ASVD) | 228 | 224.775,00 |
| Rede divergente entre registros da chave | 49 | 203,00 |
| Comercial divergente entre registros da chave | 3 | 14.872,00 |

\* **Motivos sobrepostos:** os volumes não devem ser somados para estimar um total exclusivo.

Sem DeParaCDD significa fora da cobertura do de-para de **32 clientes** incluído na base; pode ser uma limitação de escopo, e não cadastro errado. As **52.018 linhas com status Cancelada** estão preservadas no histórico de movimentações conforme a regra vigente, mas a semântica operacional dos cancelamentos continua relevante para interpretação.

## 5. Fonte VD — CAD, Malha, estoque D1 e formação

- Das **6.944 chaves ASVD inequívocas**, 6.940 encontram SKU EG na CAD; 6.716 têm Malha por Comercial + SAP (com par SKU/fábrica presente); 6.526 localizam pelo menos uma origem com D1 positivo.
- A chave correta comprovada é `Order.SKU EG → CAD.Cód_Prod → CAD.Cod S4 → Malha.SKU SAP`, com `Malha.Destino Comercial` compatível com `Order.Cód. Comercial`, chegando à fábrica `Fábrica Origem SAP`.
- O estoque fábrica corresponde a `Orig. S4 + Sku PCA/EG`, D1 em PLT; **não se soma D1 de centros diferentes para dizer que um pedido cabe em um carro**.
- O estoque da fonte identificou **331 D1 negativos**, que não se tornam volume disponível.

Formação potencial por fábrica em **todo o horizonte do extrato**, considerando apenas chaves inequívocas ASVD, pendentes positivas e fator CAD válido:

| Fábrica | Pendente potencial PLT | Qualificado PLT (D1 limitado por SKU) | Carros potenciais de 24 PLT |
|---|---:|---:|---:|
| BRCH | 12.191,43 | 7.257,62 | 302 |
| BR09 | 3.020,71 | 3.020,71 | 125 |
| BRDF | 7.428,65 | 1.759,17 | 73 |
| BR23 | 2.619,94 | 1.425,10 | 59 |
| BR15 | 1.553,10 | 1.013,33 | 42 |
| BR13 | 2.112,00 | 445,45 | 18 |
| BR16 | 603,55 | 224,99 | 9 |

**Não somar os carros potenciais entre origens.** O mesmo SKU pode aparecer em mais de uma fábrica; não houve reserva/otimização global de alocação, nem filtro de vencimento para essa tabela. Os valores não são programação operacional de expedição.

## 6. CD — cobertura condicional da grade

- Das **82.805 chaves exclusivamente ASCD**, 10.532 têm CDD identificado via DeParaCDD, e 8.647 localizam o SKU na grade apropriada (incluindo chaves sem pendente).
- Existem **970 chaves com pendente positivo e grade individual suficiente** e **93 com grade individual parcial**, dentro da metodologia adotada. Isso não significa reserva de estoque: SKUs comuns a vários pedidos competem pelo mesmo saldo.
- A tabela de cobertura agregada por CDD/SKU está no Excel resumo e no JSON. A base tem apenas 32 clientes no DeParaCDD, portanto não é válido extrapolar a cobertura a toda a carteira ASCD.

## 7. Semana de vencimento 16/11 a 22/11/2026 (cenário auditado)

| Tipo | Chaves completas com vencimento na semana | Pendente CX |
|---|---:|---:|
| ASCD | 7.335 | 64.759,00 |
| ASVD | 824 | 328.244,87 |
| Misto | 545 | 91.612,00 |
| **Total** | **8.704** | **484.615,87** |

A semana foi usada como recorte de verificação, **não presumida como seleção do usuário no HTML**. Outros períodos devem usar Data de Vencimento da mesma entrada original, com filtragem coerente.

## 8. Ajustes no HTML v29 e status dos testes

A v29 foi corrigida para reconhecer:
1. `Qtd. Faturada` como Faturado — não confundir com `Qtd. Atendida`.
2. `Unidade` real e **não converter DZ/UN/PC automaticamente em CX**.
3. `Nome Cliente SAP` como identificação legível de cliente.
4. `Tipo Pedido=ASCD/ASVD` como canal quando unívoco; `MISTO` fica sem qualificação automática.
5. `Cod S4` da CAD para relacionar `SKU SAP` da Malha; de-para de origens automático a partir de BR/PCA no Estoque Fábricas (correções anteriores).

O código JavaScript foi compilado e submetido a testes controlados de mapeamento. **Ainda não foi executado um teste visual completo do HTML no navegador com todos os 140 MB da Order.** A conciliação numérica foi feita de forma independente com o script Python executado no GitHub Actions.

## 9. Evidências

O arquivo da execução `homologacao-order-completa-v29` reúne:
- `conciliacao_por_pedido_cliente_sku.csv` (95.548 chaves, original selecionado, movimentos, pendente, fatores, tipo, estoque/grade e alertas);
- `divergencias_e_pendencias.csv` (80.798 chaves com ao menos um alerta, inclusive falta de DeParaCDD);
- `chaves_tipo_pedido_misto.csv` (5.799 chaves);
- `formacao_por_fabrica.csv`;
- `resumo_reconciliacao.json`, `perfil_order.json` e inventários.

**Parecer final:** os cruzamentos e cálculos de saldo com fontes reais foram realizados; **não liberar homologação irrestrita** antes de tratar principalmente as chaves mistas, as conversões pendentes, o escopo da DPAR e os originais divergentes. O resultado não pode ser classificado como conferido contra um Pendente de fonte porque tal coluna não existe na Order enviada.

**Confidencialidade:** a Order foi incluída em repositório GitHub público. Considerar restringir o acesso ou mover a fonte para armazenamento privado caso contenha dados comerciais sensíveis.
