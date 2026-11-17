# Carteira Reversa — Website Builder v27

Atualização do HTML consolidado do Website Builder, preservando a identidade e navegação do original.

## Principais ajustes

- Validade mínima inclusiva: apenas pedidos com vencimento >= data selecionada; recalcula entrada original, faturado, pendente, fill rate, gráficos e exportações.
- Captação = menor data de criação por chave Pedido ERP + EG Cliente + SKU EG; filtro independente de validade.
- Quantidade original usa uma linha da chave, enquanto pendente soma as movimentações; células vazias das colunas existentes de movimentação valem zero. Coluna ausente é problema sinalizado.
- Produção usa ORIGEM, COD_PROD, NOME_PROD e PRODUÇÃO (data). Não exige mais ESTOQUE.
- Estoque VD D1 por origem autorizada pela Malha após CAD EG→SAP; estoque CD por CDD/grade.
- Retiradas as faixas antigas OK/Crítico/Intermediário da qualificação. Atendimento: atende, parcial, sem estoque ou não localizado.
- Shibata separado em CD Shibata (VD) e lojas Shibata (CD) por pedido/EG/fill rate.
- Seleção de redes com busca e multisseleção. Excel cliente sem volume de estoque, Excel interno mantém dados técnicos.

## Validação
Testes executados no Chromium com cenário demonstrativo: filtro de validade alterou entrada, faturado, pendente e fill rate; cabeçalhos de Produção de quatro colunas detectados; Order com duas movimentações e células vazias não retornou N/D; Excel cliente foi gerado com três abas e sem quantidades de D1/grade. Não foi feita homologação com os arquivos operacionais completos.

**Site publicado no Website Builder:** este commit atualiza o código no GitHub, não um deploy hospedado automaticamente. Para refletir no domínio ativo, o site deve ser atualizado/publicado na plataforma de hospedagem.
