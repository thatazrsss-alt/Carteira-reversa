# Homologação real das fontes de estoque — Carteira Reversa v29

> **ATUALIZAÇÃO POSTERIOR EM 17/11/2026:** a Order.zip foi localizada no repositório e reconciliada com a BASE_ESTOQUE. Este documento é histórico e suas referências à ausência da Order estão superadas. Consulte o [parecer de homologação real mais recente](HOMOLOGACAO_REAL_ORDER_ESTOQUE_2026-11-17.md). O status permanece **parcial**, com exceções documentadas.

**Data da execução:** 17/11/2026
**Escopo:** BASE_ESTOQUE 16.11.xlsx lida diretamente no repositório pelo GitHub Actions, com cruzamentos de dados efetivos entre CAD, Malha, Estoque Fábricas, grades CD, DeParaCDD e Produção.

**Parecer:** **HOMOLOGAÇÃO DAS FONTES E CHAVES DE ESTOQUE: PARCIALMENTE APROVADA COM EXCEÇÕES.** **HOMOLOGAÇÃO DA CARTEIRA POR PEDIDO: BLOQUEADA POR AUSÊNCIA DA ORDER OPERACIONAL REAL.**

**Execução do GitHub Actions:** https://github.com/thatazrsss-alt/Carteira-reversa/actions/runs/44083836035

O artefato **evidencia-estoque-v29** dessa execução contém os JSON de inventário, cruzamentos, de-para, exceções da Malha e compatibilidade das grades CD. Não foram utilizados valores de Order fictícia para afirmar resultados de clientes.

## 1. Inventário real

| Aba / conjunto | Linhas de dados |
|---|---:|
| CAD | 9.347 |
| Malha | 6.484 |
| Estoque Fábricas | 10.745 |
| Produção | 1.821 |
| DeParaCDD | 32 |
| Grade CDD Louveira | 481 |
| Grade CDD Diadema | 385 |
| Grade CDD Guarulhos | 393 |
| Grade CDD Suzano | 381 |
| Grade CDD Taubaté | 336 |
| Grade CDD São José | 338 |
| **Total de linhas nas 11 abas** | **30.743** |

O total de 30.743 reúne linhas de fontes diferentes; não equivale a 30.743 pedidos ou SKUs distintos.

## 2. CAD × Malha × Estoque Fábricas

| Validação | Evidência real | Parecer |
|---|---:|---|
| CAD: SKUs EG distintos (`Cód_Prod`) | 9.345 | Base reconhecida |
| CAD: SKUs EG com fatores CX/PLT conflitantes | 0 | Aprovado no grão testado |
| Malha: linhas | 6.484 | Fonte reconhecida |
| `SKU SAP` Malha × **`Cod_SAP` CAD** | 13/6.484 | **CHAVE INCORRETA PARA ESTA MALHA** |
| `SKU SAP` Malha × **`Cod S4` CAD** | **6.472/6.484** | **CHAVE CORRETA PARA ESTA BASE; CORRIGIDA NO HTML V29** |
| Linhas da Malha sem `Cod S4` correspondente | **12** | Exceção de cadastro |
| Malha com EG correspondente e par SKU–BR da mesma fábrica na base D1 | **6.462/6.484** | Cruzamento positivo, sem garantir estoque |
| Linhas da Malha sem par SKU–fábrica | **22** | 12 sem CAD; 10 sem mesmo par SKU–fábrica |
| Malha com par SKU–fábrica e **D1 positivo** | **6.019/6.484** | Presença de saldo, **não cobertura dos pedidos** |
| Estoque Fábricas: SKUs PCA distintos | 902 | **902/902 presentes na CAD `Cód_Prod`** |
| Estoque: pares únicos SKU PCA + Orig. S4 | 10.745 | Não houve repetição dessa chave no inventário |
| Estoque: pares SKU/fábrica com D1 positivo | 3.375 | Não representa reserva |
| Estoque: D1 negativo | **331** | Todos atributo `ESTOQUE FINAL`; não usar como disponível |
| Estoque: D1 zero | 7.039 | Sem saldo positivo para o cenário D1 |

**Importante:** 6.019 linhas da Malha com D1 positivo não significam 6.019 cargas nem que 92,8% do volume pedido será atendido. Os mesmos SKUs e saldos podem aparecer em várias autorizações/destinos. A alocação e a formação de carro exigem Pendente PLT por Pedido ERP + EG Cliente + SKU.

## 3. De-para e nomes das fábricas

A base apresentou **40 pares distintos e consistentes Orig. S4 (BR) ↔ Orig. PCA**, com **zero conflitos BR/PCA**. Dois registros têm descrição explícita de CDD e foram excluídos da descoberta automática de centros VD. Para análise VD, ficaram **38 origens cadastráveis**, incluindo as 9 que já estavam no HTML e **29 adicionadas automaticamente** pela v29 a partir dos dados reais.

A correspondência foi testada sobre os 40 pares extraídos do arquivo; 38/38 origens não-CDD passaram na verificação de código BR e centro PCA, sem colisões. Nomes reais (coluna `Fábrica`) são reutilizados sem inventar descrições. BRs sem origem identificada continuam sujeitos a validação.

## 4. Estoque CD / grades

A regra **SKU EG sem último dígito verificador ↔ CodigoProduto** da grade foi testada contra o catálogo real:

| Grade de CDD | Itens | Compatíveis com CAD | Não localizados |
|---|---:|---:|---:|
| Louveira | 481 | 481 | 0 |
| Diadema | 385 | 385 | 0 |
| Guarulhos | 393 | 393 | 0 |
| Suzano | 381 | 381 | 0 |
| Taubaté | 336 | 330 | **6** |
| São José | 338 | 337 | **1** |
| **Total** | **2.314** | **2.307** | **7** |

Nenhum saldo `SaldoDisponivel` negativo foi identificado nas seis grades. O DeParaCDD contém 32 registros distribuídos em cinco CDDs; a ausência de uma loja vinculada a determinado CDD nesse de-para não prova erro da grade desse centro.

## 5. Produção

A aba Produção possui 1.821 linhas e **279 SKUs distintos em `COD_PROD`**. Desses, **270 constam na CAD** pela chave EG literal e **9 não constam**. A coluna `PRODUÇÃO` é uma informação de data, não uma quantidade de pallets adicionável ao D1; `ESTOQUE` nessa fonte não deve substituir o saldo oficial em estoque.

## 6. Ajustes de código aplicados à v29

1. Reconhecimento automático dos cabeçalhos reais `Cód_Prod`, `Fábrica Origem SAP` e `Nome Fábrica Origem SAP`.
2. Para a CAD deste arquivo, a chave da Malha passou a usar `Cod S4` em vez de `Cod_SAP`.
3. De-para de fábrica **dinâmico e validado** por `Orig. S4` + `Orig. PCA` + `Fábrica`, com verificação de conflitos, sem misturar CDD com VD.
4. Em Estoque Fábricas, o produto é SKU PCA/EG, o saldo é D1 em PLT e a formação de carros deve permanecer por **mesma origem**, limitada a disponibilidade real do SKU.
5. A distinção entre presença de estoque e cobertura total de pendente continua obrigatória.

## 7. Pendências que impedem homologação total

- **Order/Pendente operacional real não existe entre os arquivos independentes localizados no GitHub.** O ZIP original v15 contém exemplo de entrada/saída, scripts e instruções, não uma Order vigente identificada.
- Sem a Order real, não é possível conciliar **Marcado = Carro com Remessa**, Faturado, Quantidade Atualizada, Pendente por movimento, Fill Rate de pedidos, cobertura efetiva ou potenciais carros de 24 PLT por cliente.
- Exceções reais de dados a tratar ou justificar: **12** linhas Malha com SKU SAP sem CAD `Cod S4`; mais **10** sem par SKU–fábrica; **7** itens de grade CD não encontrados na CAD sem dígito; **9** SKUs de Produção não encontrados na CAD; **331** saldos D1 negativos.
- As 443 linhas de Malha cujo SKU–fábrica existe, mas não tem D1 positivo, não configuram falha de chave; apenas não demonstram disponibilidade D1. Não devem ser declaradas atendíveis.
- Ainda é necessária execução ponta a ponta da importação HTML e de suas exportações com os arquivos operacionais completos para aprovação de uso em produção.

## Conclusão

A execução sobre a **BASE_ESTOQUE 16.11.xlsx real** comprovou a compatibilidade de 6.472/6.484 linhas da Malha com a coluna correta da CAD; 6.462/6.484 linhas com par EG–fábrica; 2.307/2.314 itens das grades CD com a CAD; e de-para consistente das fábricas. A v29 foi corrigida com essas evidências.

**Status final:** validação de fontes e cruzamentos de estoque **parcialmente aprovada com exceções documentadas**; reconciliação e homologação numérica por pedido **não efetuadas** por falta da Order operacional real.

**Não usar testes ou dados de exemplo como comprovação de faturamento/atendimento de pedidos reais.**
