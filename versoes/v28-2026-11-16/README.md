# Carteira Reversa — Gerencial v28

Visual e motor baseados na v27 do Website Builder.

## Novidades
- **Marcado** = **Carro com Remessa**, contado uma vez por movimento. Pendente (CX) = soma por linha de Atualizada − Marcado − Carro sem Remessa − Faturado; a quantidade original U/V/W permanece única pela chave Pedido ERP + EG Cliente + SKU EG.
- Por pedido/EG/canal, **itens atendidos / total** conta SKUs com pendente igual a zero; **itens com cobertura / total** conta SKUs com pendente positivo coberto pelo estoque encontrado.
- VD: CAD EG → SAP para a Malha (Comercial + SAP), D1 por origem; estoque VD e Produção em EG. Pendente PLT = Pendente CX / CX por pallet da CAD.
- Formação VD por origem: potencial qualificado PLT limitado ao D1 por SKU na **mesma fábrica**. Carro potencial de 24 PLT; não somar fábricas diferentes. A análise **não representa reserva de estoque nem promessa de entrega**.
- Código + **nome da origem**, data de produção de quatro colunas, e qualificação resumida por pedido. Sem concatenar estados de SKUs diferentes como se fossem um único status.
- Excel de cliente: três abas e nenhum saldo de estoque D1 ou grade. Excel interno: Conciliação, Origens VD e **Formação VD**, com quantidades técnicas.
- Shibata separado em CD Shibata (VD) e Lojas Shibata (CD); busca com multisseleção de redes e crivo de validade inclusivo preservados.

## Validação
- JavaScript verificado pelo Node.
- Chromium com demonstração e cenário de dois SKUs, 25 PLT potencialmente qualificados em uma única origem: 1 carro potencial de 24 PLT.
- Order com Marcado 5 + 15, faturado 10 + 20, atualizada 100 + 50: Marcado 20, Faturado 30, Pendente 100 e Original 100 sem duplicar; captação na menor criação.
- Geração e releitura dos Excel externo (3 abas) e interno (6 abas), layout das tabelas e confirmação de ausência de saldos de estoque no e-mail/Excel externo.

**Limite:** dados demonstrativos/controlados. A Order e BASE_ESTOQUE reais completas não foram homologadas com esta versão.

[Notion — regras oficiais](https://app.notion.com/p/41a16626f20281d7ba6ef718c354a96f)
