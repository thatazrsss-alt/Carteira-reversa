# Carteira Reversa — Gerencial v29 (16/11/2026)

**Homologação com estoque real:** [conferir parecer da BASE_ESTOQUE 16.11 (17/11/2026)](HOMOLOGACAO_ESTOQUE_REAL_2026-11-17.md) e [evidências da execução no GitHub Actions](https://github.com/thatazrsss-alt/Carteira-reversa/actions/runs/44083836035). Malha/CAD, SKU/fábrica, de-para e grades CD conferidos com dados reais; Order operacional não encontrada no repositório, portanto indicadores por pedido ainda não homologados.


**Parecer de homologação 17/11/2026:** [abrir relatório de testes e bloqueios](HOMOLOGACAO_2026-11-17.md) — homologação funcional parcial; bases reais ainda não reconciliadas.

**[Parecer de homologação técnica v29](HOMOLOGACAO_v29_2026-11-16.md)** — cenários controlados aprovados; homologação operacional com Order e estoque reais ainda pendente.

**Versão base:** v28 preservada. **Painel:** [Abrir HTML v29](Carteira_Reversa_Gerencial_v29_Conciliacao_Formacao_Origem.html).

## Motor e cruzamentos revisados

| Etapa | Chave e regra |
|---|---|
| Order | Pedido ERP + EG Cliente + SKU EG; inicial HL/PLT/CX por cabeçalho nomeado, **uma entrada por chave**; criação mais antiga como captação |
| Movimentos | Atualizada, Marcado (= Carro com Remessa), Carro sem Remessa, Faturado, somados por movimento; **não somar Marcado com outro cabeçalho de Carro com Remessa** |
| Pendente CX | Soma por linha de Atualizada − Marcado − Carro sem Remessa − Faturado; ausências/erros de coluna permanecem não calculados |
| Fill rate | Faturado CX / Original CX, 0–100% na visualização, com alerta para excesso bruto; Marcado não equivale a Faturado |
| CAD | EG → SAP exclusivamente no cruzamento de Malha; caixas por pallet por SKU, sem conversão fictícia; fatores conflitantes bloqueados |
| Malha | Destino Comercial + SKU SAP → origens VD autorizadas |
| Estoque VD | SKU EG + mesma origem/fábrica; D1 em PLT, comparado a Pendente CX / CAD |
| CDD | Loja/EG → DeParaCDD; SKU EG sem último dígito → Grade desse CDD; estoque em CX, sem confundir com VD |
| Produção | Origem + SKU EG + data prevista; NÃO soma ao estoque disponível nem constitui volume faturável |
| Formação VD | Soma apenas SKUs qualificados **na mesma origem**, limitada ao D1 de cada SKU inclusive entre vários pedidos; 1 carro potencial = 24 PLT; origens alternativas explicitadas |
| Atendimento | SKU considerado atendido apenas com pendente zerado **e** movimento positivo em Marcado/Faturado; parciais separados; cobertura calculada somente para pendentes |
| Exportações | Cliente: recorte por rede sem saldos internos; interno: Conciliação, Origens VD, Formação VD, com código/nome de origem e Pendente PLT |

## Conciliação e alertas novos

- Se **Marcado** e **Carro com Remessa** estiverem simultaneamente presentes e divergirem, a ocorrência é sinalizada (não somar ambos).
- Se Marcado + Faturado exceder Atualizada no mesmo movimento, sinaliza **possível sobreposição**; não modifica silenciosamente a fórmula oficial.
- A aba interna **Conciliação** inclui fechamento dos movimentos (conforme a fórmula), diferença informativa entre Original/Faturado/Pendente, número de conflitos de Marcado/Remessa e número de suspeitas de sobreposição.
- O saldo original não é inferido por colunas em posições fixas U/V/W. Quando não existe cabeçalho reconhecível, requer mapeamento; a quantidade original em CX só pode ser convertida de PLT se o fator CAD for único e validado.
- Faturado não substitui indiscriminadamente uma coluna de “quantidade atendida”.

## Testes estruturais executados

- Compilação sintática dos scripts principais: **aprovada**.
- Formação de 25 PLT de dois SKUs, mesma fábrica, resulta em **1 carro potencial**.
- D1 de um mesmo SKU usado por dois pedidos na mesma origem é contabilizado **uma única vez**, limitado ao estoque.
- D1 zerado não gera carro; SKU elegível em duas fábricas é marcado como **alternativa**, não estoque somável.

## Limites e homologação

Os testes acima usam cenários controlados. A **Order real e o BASE_ESTOQUE real completos não foram homologados** nesta execução. A formação é potencial (não reserva, não despacho, não garantia). Estoque pode estar comprometido em pedidos fora do filtro; as alternativas de origem não podem ser somadas para afirmar atendimento. Posições e unidades não identificadas devem bloquear estimativas, não gerar zeros fictícios.

Valide especialmente: cabeçalhos reais de Marcado / Carro com Remessa / Faturado, sobreposição temporal entre movimentos, alternativas de origem e fatores CAD por SKU.
