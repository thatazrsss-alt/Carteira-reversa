# Homologação técnica v29 — 17/11/2026

> **ATUALIZAÇÃO POSTERIOR EM 17/11/2026:** a Order.zip foi localizada no repositório e reconciliada com a BASE_ESTOQUE. Este documento é histórico e suas referências à ausência da Order estão superadas. Consulte o [parecer de homologação real mais recente](HOMOLOGACAO_REAL_ORDER_ESTOQUE_2026-11-17.md). O status permanece **parcial**, com exceções documentadas.


**Status: HOMOLOGAÇÃO FUNCIONAL PARCIAL. NÃO HOMOLOGADO COM BASES REAIS COMPLETAS.**

## Fontes localizadas

- HTML v29: `Carteira_Reversa_Gerencial_v29_Conciliacao_Formacao_Origem.html`.
- Estoque: `BASE_ESTOQUE 16.11.xlsx`, 4.469.103 bytes, presente na raiz do repositório. **Arquivo binário não foi aberto para validação nesta execução**.
- Order: **nenhum arquivo operacional completo da Order localizado** nos 21 objetos do repositório GitHub ou na pesquisa de arquivos acessíveis do projeto.
- Arquivo ZIP v15: referência histórica, não substitui Order real e estoque vigente.

## Ensaios do código

**Bloco A — formação/qualificação/itens: 15/15 aprovados.**

1. Origem 892-VD, dois SKUs, 25 PLT qualificados → 1 carro de 24 PLT.
2. SKU presente também em 952-VD → origem alternativa sinalizada; não somar 892 com 952.
3. Duas demandas do mesmo SKU/origem não duplicam D1: demanda 30 PLT, D1 20 → 20 PLT qualificados.
4. Estoque nulo/ausente → nenhum PLT computado.
5. Itens com pendente zero sem movimentação não são considerados atendidos.
6. Pendente com marcação ou faturamento positivo pode ser atendimento parcial.
7. Carro sem remessa não garante item atendido.
8. VD com CAD válido, estoque suficiente → cobertura; sem CAD → não comprova cobertura.
9. VD sem estoque → Sem estoque; CD com grade suficiente → Atende; VD sem fator → Conversão CAD pendente.

**Bloco B — conciliação/quantidades: 12/12 aprovados com cabeçalho de unidade reconhecido.**

- Movimentos simulados: Atualizada 100+50 CX; Marcado 5+15; Faturado 10+20; Carro sem remessa 0 → Atualizada 150, Marcado 20, Faturado 30, Pendente 100. A referência original 100 CX é única, Fill rate 30%.
- Faturado bruto 120 / original 100 → Fill rate visual 100%, sem corrigir faturamento bruto nem esconder pendente negativo.
- Comparação com pendente declarado na fonte detecta diferença de 10 CX.
- Faturado ausente gera pendente não calculado.
- Conversão explícita de 2 PLT atualizado e 1 PLT faturado, CAD 48 CX/PLT → pendente 48 CX. **A Order precisa ter cabeçalho de unidade reconhecido, como “Unidade medida”.** O teste inicial com cabeçalho genérico “Unidade” não converteu, evidenciando risco de identificação de campos.

**Outros controles inspecionados no código**
- Original U/V/W obtido por cabeçalho, não por posição.
- Produção representa data prevista, não quantidade adicionada à cobertura.
- CAD EG → SAP para Malha; estoque VD por SKU EG e origem; CD por CDD e grade.
- Marcado e Carro com Remessa tratados como sinônimos, com alerta para valores divergentes quando ambos aparecem.
- Indicadores de origem são cenários potenciais; não representam reserva nem despacho.

## Matriz de homologação

| Teste | Resultado | Pendência |
|---|---|---|
| Compilação do motor JS e lógica de formação | Aprovado em testes controlados | Validar execução no navegador com bases reais |
| Soma movimentos por SKU e saldo pendente | Aprovado em testes controlados | Conferir lançamentos históricos reais |
| Marcado = Carro com Remessa | Lógica inspecionada | Validar cabeçalhos e semântica da Order |
| Fill rate e limite 100% | Aprovado em testes controlados | Conciliar faturado e original reais |
| CAD CX/PLT e leitura de unidade | Aprovado com cabeçalho reconhecido | Conferir cabeçalho efetivo e fatores duplicados |
| Malha por Comercial + SAP | Inspeção estática | Conferir mapeamentos reais |
| Estoque VD D1 por origem e SKU | Lógica e limites aprovados sinteticamente | Conciliar estoque real por centro/SKU |
| Estoque CD por DPAR e grade | Teste sintético de qualificação | Conferir nomes das lojas, CDD e grade real |
| Produção por data | Regra estática correta | Conferir datas reais por centro e SKU |
| Formação 24 PLT | 15 testes do bloco A aprovados | Conferir compromissos/estoque compartilhado fora do filtro |
| Exportação Excel externo/interno e e-mail | Código inspecionado, sem reexecução real | Conferir arquivos gerados e privacidade por rede |
| Fechamento ponta a ponta | **BLOQUEADO** | Necessários Order real e leitura integral de BASE_ESTOQUE |

## Riscos e recomendações para liberação

**Crítico: ausência da Order real.** Não é possível afirmar resultados ou taxa de divergência real por Pedido ERP + EG Cliente + SKU.

**Crítico: acesso não efetuado ao Excel de estoque real.** O arquivo foi encontrado, mas sua estrutura/conteúdo não foi inspecionada neste ciclo.

**Alto: cabeçalho de unidade do movimento.** Sem identificação explícita de PLT, o sistema adota CX como padrão. Confirmar que a base de pedido sempre usa CX por omissão; se houver PLT com cabeçalho não reconhecido, a conversão ficará incorreta.

**Alto: sobreposição entre Marcado e Faturado.** O alerta compara movimentos específicos, mas a conciliação temporal precisa conferir se quantidades são eventos exclusivos ou snapshots acumulados.

**Médio: classificação de atendimento.** A inferência usa saldo e movimentos. Para comprovar entrega, é necessário evento logístico ou fiscal oficial, além de saldo zero.

**Médio: várias origens.** As formações representam oportunidades independentes; não podem ser somadas como alocação concluída.

## Próxima evidência para homologação definitiva

Disponibilizar a **Order operacional** com movimentos, original, marcado, faturado, pendente, cliente e SKU; permitir leitura da **BASE_ESTOQUE 16.11.xlsx**. Executar confronto real com saída de diferenças por chave, origem e SKU, indicadores de cobertura, saldos e critérios de aceite. Somente após isso emitir status **HOMOLOGADO EM PRODUÇÃO**.

**Parecer:** a v29 passou nos cenários controlados executados. A validação das regras com as bases reais permanece **não concluída**. Não usar este parecer como aprovação dos resultados operacionais.
